# Copyright 2012 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Perform various tasks related to updating Portage packages."""

import filecmp
import glob
import os
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, Optional

import portage  # pylint: disable=import-error

from chromite.lib import build_target_lib
from chromite.lib import commandline
from chromite.lib import config_lib
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import depgraph
from chromite.lib import git
from chromite.lib import operation
from chromite.lib import osutils
from chromite.lib import portage_util
from chromite.lib import upgrade_table as utable


oper = operation.Operation("cros_portage_upgrade")

NOT_APPLICABLE = "N/A"
WORLD_TARGET = "world"
UPGRADED = "Upgraded"

# Files that we authored.
CROS_AUTHORED_FILES = {"DIR_METADATA", "METADATA", "OWNERS", "README.md"}


# pylint: disable=attribute-defined-outside-init


class PInfo:
    """Class to accumulate package info during upgrade process.

    This class is basically a formalized dictionary.
    """

    __slots__ = (
        "category",  # Package category only
        # TODO(mtennant): Rename 'cpv' to 'curr_cpv' or similar.
        "cpv",  # Current full cpv (revision included)
        "cpv_cmp_upstream",  # 0 = current, >0 = outdated, <0 = futuristic
        "latest_upstream_cpv",  # Latest (non-stable ok) upstream cpv
        "overlay",  # Overlay package currently in
        "package",  # category/package_name
        "package_name",  # The 'p' in 'cpv'
        "package_ver",  # The 'pv' in 'cpv'
        "slot",  # Current package slot
        "stable_upstream_cpv",  # Latest stable upstream cpv
        "state",  # One of utable.UpgradeTable.STATE_*
        "upgraded_cpv",  # If upgraded, it is to this cpv
        "upgraded_unmasked",  # Boolean. If upgraded_cpv, indicates if unmasked.
        "upstream_cpv",  # latest/stable upstream cpv according to request
        "user_arg",  # Original user arg for this pkg, if applicable
        "version_rev",  # Just revision (e.g. 'r1').  '' if no revision
    )

    # Any deriving classes must maintain this cumulative attribute list.
    __attrlist__ = __slots__

    def __init__(self, **kwargs) -> None:
        """Initialize all attributes to None unless specified in |kwargs|."""
        for attr in self.__attrlist__:
            setattr(self, attr, kwargs.get(attr))

    def __eq__(self, other: Any) -> bool:
        """Equality support.  Used in unittests."""
        if not isinstance(other, type(self)):
            return False

        no_attr = object()
        for attr in self.__attrlist__:
            if getattr(self, attr, no_attr) != getattr(other, attr, no_attr):
                return False

        return True

    def __ne__(self, other: Any) -> bool:
        """Inequality support for completeness."""
        return not self == other


class Upgrader:
    """A class to perform various tasks related to updating Portage packages."""

    PORTAGE_GIT_URL = "%s/external/github.com/gentoo/gentoo.git" % (
        config_lib.GetSiteParams().EXTERNAL_GOB_URL
    )
    GIT_REMOTE = "origin"
    GIT_BRANCH = "master"
    GIT_REMOTE_BRANCH = "%s/%s" % (GIT_REMOTE, GIT_BRANCH)

    UPSTREAM_OVERLAY_NAME = "portage"
    UPSTREAM_TMP_REPO = os.environ.get(constants.SHARED_CACHE_ENVVAR)
    if UPSTREAM_TMP_REPO is not None:
        UPSTREAM_TMP_REPO = "%s/cros_portage_upgrade" % UPSTREAM_TMP_REPO
    else:
        UPSTREAM_TMP_REPO = "/tmp"
    UPSTREAM_TMP_REPO += "/" + UPSTREAM_OVERLAY_NAME

    STABLE_OVERLAY_NAME = "portage-stable"
    CATEGORIES_FILE = "profiles/categories"
    HOST_BOARD = "amd64-host"
    OPT_SLOTS = (
        "amend",
        "force",
        "no_upstream_cache",
        "rdeps",
        "upgrade",
        "upgrade_deep",
        "upstream",
        "unstable_ok",
        "verbose",
        "local_only",
    )

    EQUERY_CMD = "equery"
    EMERGE_CMD = "emerge"
    PORTAGEQ_CMD = "portageq"
    BOARD_CMDS = set([EQUERY_CMD, EMERGE_CMD, PORTAGEQ_CMD])

    __slots__ = (
        "_amend",  # Boolean to use --amend with upgrade commit
        "_args",  # Commandline arguments (all portage targets)
        "_curr_arch",  # Architecture for current board run
        "_curr_board",  # Board for current board run
        "_deps_graph",  # Dependency graph from portage
        "_force",  # Force upgrade even when version already exists
        "_local_only",  # Skip network traffic
        "_missing_eclass_re",  # Regexp for missing eclass in equery
        "_outdated_eclass_re",  # Regexp for outdated eclass in equery
        "_emptydir",  # Path to temporary empty directory
        "_no_upstream_cache",  # Boolean.  Delete upstream cache when done
        "_porttree",  # Reference to portage porttree object
        "_rdeps",  # Boolean, if True pass --root-deps=rdeps
        "_stable_repo",  # Path to portage-stable
        "_stable_repo_categories",  # Categories from profiles/categories
        "_stable_repo_stashed",  # True if portage-stable has a git stash
        "_stable_repo_status",  # git status report at start of run
        "_upgrade",  # Boolean indicating upgrade requested
        "_upgrade_cnt",  # Num pkg upgrades in this run (all boards)
        "_upgrade_deep",  # Boolean indicating upgrade_deep requested
        "_upgraded_packages",  # Upgraded packages.
        "_upstream",  # Path to upstream portage repo
        "_unstable_ok",  # Boolean to allow unstable upstream also
        "_verbose",  # Boolean
    )

    def __init__(self, options) -> None:
        self._args = options.packages

        self._upgrade_cnt = 0
        self._upgraded_packages = []

        self._stable_repo = os.path.join(
            options.srcroot, "third_party", self.STABLE_OVERLAY_NAME
        )
        # This can exist in two spots; the tree, or the cache.

        # Save options needed later.
        for opt in self.OPT_SLOTS:
            setattr(self, "_" + opt, getattr(options, opt, None))

        self._porttree = None
        self._emptydir = None
        self._deps_graph = None

        # Pre-compiled regexps for speed.
        self._missing_eclass_re = re.compile(
            r"(\S+\.eclass) could not be " r"found by inherit"
        )
        self._outdated_eclass_re = re.compile(
            r"Call stack:\n"
            r"(?:.*?\s+\S+,\sline.*?\n)*"
            r".*?\s+(\S+\.eclass),\s+line"
        )

    def _IsInUpgradeMode(self):
        """Return True if running in upgrade mode."""
        return self._upgrade or self._upgrade_deep

    def _SaveStatusOnStableRepo(self) -> None:
        """Get the 'git status' for everything in |self._stable_repo|.

        The results are saved in a dict at self._stable_repo_status where each
        key is a file path rooted at |self._stable_repo|, and the value is the
        status for that file as returned by 'git status -s'. (e.g. 'A' for
        'Added').
        """
        result = self._RunGit(self._stable_repo, ["status", "-s"], stdout=True)
        if result.returncode == 0:
            statuses = {}
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue

                linesplit = line.split()
                (status, path) = linesplit[0], linesplit[1]
                if status == "R":
                    # Handle a rename as separate 'D' and 'A' statuses.
                    # Example line:
                    # R path/to/foo-1.ebuild -> path/to/foo-2.ebuild
                    statuses[path] = "D"
                    statuses[linesplit[3]] = "A"
                else:
                    statuses[path] = status

            self._stable_repo_status = statuses
        else:
            raise RuntimeError(
                'Unable to run "git status -s" in %s:\n%s'
                % (self._stable_repo, result.stdout)
            )

        self._stable_repo_stashed = False

    def _LoadStableRepoCategories(self) -> None:
        """Load |self._stable_repo|/profiles/categories into set."""

        self._stable_repo_categories = set()
        cat_file_path = os.path.join(self._stable_repo, self.CATEGORIES_FILE)
        with open(cat_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    self._stable_repo_categories.add(line)

    def _WriteStableRepoCategories(self) -> None:
        """Write |self._stable_repo_categories| to profiles/categories."""

        categories = sorted(self._stable_repo_categories)
        cat_file_path = os.path.join(self._stable_repo, self.CATEGORIES_FILE)
        with open(cat_file_path, "w", encoding="utf-8") as f:
            f.writelines("\n".join(categories))

        self._RunGit(self._stable_repo, ["add", self.CATEGORIES_FILE])

    def _CheckStableRepoOnBranch(self) -> None:
        """Raise exception if |self._stable_repo| is not on a branch now."""
        result = self._RunGit(self._stable_repo, ["branch"], stdout=True)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                match = re.search(r"^\*\s+(.+)$", line)
                if match:
                    # Found current branch, see if it is a real branch.
                    branch = match.group(1)
                    if branch != "(no branch)":
                        return
                    raise RuntimeError(
                        "To perform upgrade, %s must be on a branch."
                        % self._stable_repo
                    )

        raise RuntimeError(
            "Unable to determine whether %s is on a branch." % self._stable_repo
        )

    def _PkgUpgradeRequested(self, pinfo):
        """Return True if upgrade of pkg in |pinfo| was requested by user."""
        if self._upgrade_deep:
            return True

        if self._upgrade:
            return bool(pinfo.user_arg)

        return False

    @staticmethod
    def _FindBoardArch(board):
        """Return the architecture for a given board name."""
        # Host is a special case
        if board == Upgrader.HOST_BOARD:
            return "amd64"

        # Leverage Portage 'portageq' tool to do this.
        return portage_util.PortageqEnvvar(
            "ARCH", board=board, allow_undefined=True
        )

    @staticmethod
    def _GetPreOrderDepGraphPackage(
        deps_graph, package, pkglist, visited
    ) -> None:
        """Collect packages from |deps_graph| into |pkglist| in pre-order."""
        if package in visited:
            return
        visited.add(package)
        for parent in deps_graph[package]["provides"]:
            Upgrader._GetPreOrderDepGraphPackage(
                deps_graph, parent, pkglist, visited
            )
        pkglist.append(package)

    @staticmethod
    def _GetPreOrderDepGraph(deps_graph):
        """Return packages from |deps_graph| in pre-order."""
        pkglist = []
        visited = set()
        for package in deps_graph:
            Upgrader._GetPreOrderDepGraphPackage(
                deps_graph, package, pkglist, visited
            )
        return pkglist

    @staticmethod
    def _CmpCpv(cpv1, cpv2):
        """Returns standard cmp result between |cpv1| and |cpv2|.

        If one cpv is None then the other is greater.
        """
        if cpv1 is None and cpv2 is None:
            return 0
        if cpv1 is None:
            return -1
        if cpv2 is None:
            return 1
        return portage.versions.pkgcmp(
            portage.versions.pkgsplit(cpv1), portage.versions.pkgsplit(cpv2)
        )

    @staticmethod
    def _GetCatPkgFromCpv(cpv):
        """Returns category/package_name from a full |cpv|.

        If |cpv| is incomplete, may return only the package_name.

        If package_name cannot be determined, return None.
        """
        if not cpv:
            return None

        # Result is None or (cat, pn, version, rev)
        result = portage.versions.catpkgsplit(cpv)
        if result:
            # This appears to be a quirk of portage? Category string == 'null'.
            if result[0] is None or result[0] == "null":
                return result[1]
            return "%s/%s" % (result[0], result[1])

        return None

    @staticmethod
    def _GetVerRevFromCpv(cpv):
        """Returns just the version-revision string from a full |cpv|."""
        if not cpv:
            return None

        # Result is None or (cat, pn, version, rev)
        result = portage.versions.catpkgsplit(cpv)
        if result:
            (version, rev) = result[2:4]
            if rev != "r0":
                return "%s-%s" % (version, rev)
            else:
                return version

        return None

    @staticmethod
    def _GetEbuildPathFromCpv(cpv):
        """Returns the relative path to ebuild for |cpv|."""
        if not cpv:
            return None

        # Result is None or (cat, pn, version, rev)
        result = portage.versions.catpkgsplit(cpv)
        if result:
            # pylint: disable=unpacking-non-sequence
            (cat, pn, _version, _rev) = result
            ebuild = cpv.replace(cat + "/", "") + ".ebuild"
            return os.path.join(cat, pn, ebuild)

        return None

    def _RunGit(self, cwd, command, stdout=None, stderr=None):
        """Runs git |command| (a list of command tokens) in |cwd|.

        This leverages the cros_build_lib.run function. The |stdout| and
        |stderr| arguments are passed to that function.

        Returns a Result object as documented by cros_build_lib.run.
        Most usefully, the result object has a .stdout attribute containing
        the output from the command (if |stdout| was True).
        """
        # This disables the vi-like output viewer for commands like 'git show'.
        extra_env = {"GIT_PAGER": "cat"}
        return git.RunGit(
            cwd,
            command,
            extra_env=extra_env,
            print_cmd=self._verbose,
            stdout=stdout,
            stderr=stderr,
        )

    @staticmethod
    def _SplitEBuildPath(ebuild_path):
        """Split a full ebuild path into (overlay, cat, pn, pv)."""
        (ebuild_path, _ebuild) = os.path.splitext(ebuild_path)
        (ebuild_path, pv) = os.path.split(ebuild_path)
        (ebuild_path, pn) = os.path.split(ebuild_path)
        (ebuild_path, cat) = os.path.split(ebuild_path)
        (ebuild_path, overlay) = os.path.split(ebuild_path)
        return (overlay, cat, pn, pv)

    @staticmethod
    def _GenPortageEnvvars(
        arch, unstable_ok, portdir=None, portage_configroot=None
    ):
        """Returns dictionary of envvars for running portage tools.

        If |arch| is set, then ACCEPT_KEYWORDS will be included and set
        according to |unstable_ok|.

        PORTDIR is set to |portdir| value, if not None.
        PORTAGE_CONFIGROOT is set to |portage_configroot| value, if not None.
        """
        envvars = {}
        if arch:
            if unstable_ok:
                envvars["ACCEPT_KEYWORDS"] = arch + " ~" + arch
            else:
                envvars["ACCEPT_KEYWORDS"] = arch

        if portdir is not None:
            envvars["PORTDIR"] = portdir
            # Since we are clearing PORTDIR, we also have to clear
            # PORTDIR_OVERLAY as most of those repos refer to the "normal"
            # PORTDIR and will dump a lot of warnings if it can't be found.
            envvars["PORTDIR_OVERLAY"] = portdir
        if portage_configroot is not None:
            envvars["PORTAGE_CONFIGROOT"] = portage_configroot

        return envvars

    @staticmethod
    def _EqueryWhich(
        pkg: str,
        envvars: Dict[str, str],
        equery: str = "equery",
        include_masked: bool = False,
    ) -> Optional[tuple]:
        """Run `equery which` with common options."""
        cmd = [equery, "--no-color", "--no-pipe", "which"]
        if include_masked:
            cmd += ["--include-masked"]
        cmd += [pkg]
        result = cros_build_lib.run(
            cmd,
            extra_env=envvars,
            check=False,
            stdout=True,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )
        if result.returncode == 0:
            ebuild_path = result.stdout.strip()
            return Upgrader._SplitEBuildPath(ebuild_path)
        else:
            return None

    def _EqueryBoardWhich(
        self, pkg: str, envvars: Dict[str, str], include_masked: bool = False
    ) -> Optional[tuple]:
        """Run `equery which` (for the board)."""
        return self._EqueryWhich(
            pkg,
            envvars,
            equery=self._GetBoardCmd(self.EQUERY_CMD),
            include_masked=include_masked,
        )

    def _FindUpstreamCPV(self, pkg, unstable_ok=False):
        """Returns latest cpv in |_upstream| that matches |pkg|.

        The |pkg| argument can specify as much or as little of the full CPV
        syntax as desired, exactly as accepted by the Portage 'equery' command.
        To find whether an exact version exists upstream specify the full
        CPV.  To find the latest version specify just the category and package
        name.

        Results are filtered by architecture keyword using |self._curr_arch|.
        By default, only ebuilds stable on that arch will be accepted.  To
        accept unstable ebuilds, set |unstable_ok| to True.

        Returns upstream cpv, if found.
        """
        envvars = self._GenPortageEnvvars(
            self._curr_arch,
            unstable_ok,
            portdir=self._upstream,
            portage_configroot=self._emptydir,
        )

        # Point equery to the upstream source to get latest version for
        # keywords.
        result = self._EqueryWhich(pkg, envvars)
        if not result:
            return result
        (_overlay, cat, _pn, pv) = result
        return os.path.join(cat, pv)

    def _GetBoardCmd(self, cmd):
        """Return the board-specific version of |cmd|, if applicable."""
        if cmd in self.BOARD_CMDS:
            # Host "board" is a special case.
            if self._curr_board != self.HOST_BOARD:
                return "%s-%s" % (cmd, self._curr_board)

        return cmd

    def _AreEmergeable(self, cpvlist):
        """Indicate whether cpvs in |cpvlist| can be emerged on current board.

        This essentially runs emerge with the --pretend option to verify
        that all dependencies for these package versions are satisfied.

        Returns:
            Tuple with two elements:
            [0] True if |cpvlist| can be emerged.
            [1] Output from the emerge command.
        """
        envvars = self._GenPortageEnvvars(self._curr_arch, unstable_ok=False)
        emerge = self._GetBoardCmd(self.EMERGE_CMD)
        cmd = [emerge, "-p"] + ["=" + cpv for cpv in cpvlist]
        result = cros_build_lib.run(
            cmd,
            check=False,
            extra_env=envvars,
            stdout=True,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )

        return (result.returncode == 0, " ".join(cmd), result.stdout)

    def _FindCurrentCPV(self, pkg):
        """Returns current cpv on |_curr_board| that matches |pkg|, or None."""
        envvars = self._GenPortageEnvvars(self._curr_arch, unstable_ok=False)
        result = self._EqueryBoardWhich(pkg, envvars)
        if not result:
            return result
        (_overlay, cat, _pn, pv) = result
        return os.path.join(cat, pv)

    def _SetUpgradedMaskBits(self, pinfo) -> None:
        """Set pinfo.upgraded_unmasked."""
        cpv = pinfo.upgraded_cpv
        envvars = self._GenPortageEnvvars(self._curr_arch, unstable_ok=False)

        equery = self._GetBoardCmd("equery")
        cmd = [equery, "-qCN", "list", "-F", "$mask|$cpv:$slot", "-op", cpv]
        result = cros_build_lib.run(
            cmd,
            check=False,
            extra_env=envvars,
            stdout=True,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )

        output = result.stdout
        if result.returncode:
            raise RuntimeError(
                "equery failed on us:\n %s\noutput:\n %s"
                % (" ".join(cmd), output)
            )

        # Expect output like one of these cases (~ == unstable, M == masked):
        #  ~|sys-fs/fuse-2.7.3:0
        #   |sys-fs/fuse-2.7.3:0
        # M |sys-fs/fuse-2.7.3:0
        # M~|sys-fs/fuse-2.7.3:0
        for line in output.split("\n"):
            mask = line.split("|")[0]
            if len(mask) == 2:
                pinfo.upgraded_unmasked = mask[0] != "M"
                return

        raise RuntimeError(
            "Unable to determine whether %s is stable from equery:\n"
            " %s\noutput:\n %s" % (cpv, " ".join(cmd), output)
        )

    def _VerifyEbuildOverlay(
        self, cpv, expected_overlay, was_overwrite
    ) -> None:
        """Raises exception if ebuild for |cpv| is not from |expected_overlay|.

        Essentially, this verifies that the upgraded ebuild in portage-stable
        is indeed the one being picked up, rather than some other ebuild with
        the same version in another overlay. Unless |was_overwrite| (see below).

        If |was_overwrite| then this upgrade was an overwrite of an existing
        package version (via --force) and it is possible the previous package
        is still in another overlay (e.g. chromiumos-overlay).  In this case,
        the user should get rid of the other version first.
        """
        # Further explanation: this check should always pass, but might not
        # if the copy/upgrade from upstream did not work.  This is just a
        # confidence check.
        envvars = self._GenPortageEnvvars(self._curr_arch, unstable_ok=False)

        result = self._EqueryBoardWhich(cpv, envvars, include_masked=True)
        if not result:
            return
        (overlay, _cat, _pn, _pv) = result
        if overlay != expected_overlay:
            if was_overwrite:
                raise RuntimeError(
                    "Upgraded ebuild for %s is not visible because"
                    " existing ebuild in %s overlay takes precedence\n"
                    "Please remove that ebuild before continuing."
                    % (cpv, overlay)
                )
            else:
                raise RuntimeError(
                    "Upgraded ebuild for %s is not coming from %s:\n"
                    " %s\n"
                    "Please show this error to the build team."
                    % (cpv, expected_overlay, result)
                )

    def _IdentifyNeededEclass(self, cpv):
        """Return eclass that must be upgraded for this |cpv|."""
        # Try to detect two cases:
        # 1) The upgraded package uses an eclass not in local source, yet.
        # 2) The upgraded package needs one or more eclasses to be upgraded too.

        # Use the output of 'equery which'.
        # If a needed eclass cannot be found, then the output will have lines
        # like:
        # * ERROR: app-admin/eselect-1.2.15 failed (depend phase):
        # *   bash-completion-r1.eclass could not be found by inherit()

        # pylint: disable=line-too-long
        # If a needed eclass must be upgraded, the output might have the eclass
        # in the call stack (... used for long paths):
        # * Call stack:
        # *            ebuild.sh, line 2047:  Called source '.../vim-7.3.189.ebuild'
        # *   vim-7.3.189.ebuild, line    7:  Called inherit 'vim'
        # *            ebuild.sh, line 1410:  Called qa_source '.../vim.eclass'
        # *            ebuild.sh, line   43:  Called source '.../vim.eclass'
        # *           vim.eclass, line   40:  Called die
        # * The specific snippet of code:
        # *       die "Unknown EAPI ${EAPI}"
        # pylint: enable=line-too-long

        envvars = self._GenPortageEnvvars(self._curr_arch, unstable_ok=True)

        equery = self._GetBoardCmd(self.EQUERY_CMD)
        cmd = [equery, "--no-color", "--no-pipe", "which", cpv]
        result = cros_build_lib.run(
            cmd,
            check=False,
            extra_env=envvars,
            stdout=True,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
        )

        if result.returncode != 0:
            output = result.stdout.strip()

            # _missing_eclass_re works line by line.
            for line in output.split("\n"):
                match = self._missing_eclass_re.search(line)
                if match:
                    eclass = match.group(1)
                    oper.Notice(
                        "Determined that %s requires %s" % (cpv, eclass)
                    )
                    return eclass

            # _outdated_eclass_re works on the entire output at once.
            match = self._outdated_eclass_re.search(output)
            if match:
                eclass = match.group(1)
                oper.Notice(
                    "Making educated guess that %s requires update of %s"
                    % (cpv, eclass)
                )
                return eclass

        return None

    def _GiveMaskedError(self, upgraded_cpv, emerge_output) -> None:
        """Print error saying that |upgraded_cpv| is masked off.

        See if hint found in |emerge_output| to improve error emssage.
        """

        # Expecting emerge_output to have lines like this:
        #  The following mask changes are necessary to proceed:
        # #required by ... =somecategory/somepackage (some reason)
        # # /.../chromiumos/src/third_party/chromiumos-overlay/profiles\
        # /targets/chromeos/package.mask:
        # >=upgraded_cp
        package_mask = None

        upgraded_cp = Upgrader._GetCatPkgFromCpv(upgraded_cpv)
        regexp = re.compile(
            r"#\s*required by.+=\S+.*\n"
            r"#\s*(\S+/package\.mask):\s*\n"
            "[<>=]+%s" % upgraded_cp
        )

        match = regexp.search(emerge_output)
        if match:
            package_mask = match.group(1)

        if package_mask:
            oper.Error(
                '\nUpgraded package "%s" appears to be masked by a line in\n'
                '"%s"\n'
                "Full emerge output is above. Address mask issue, "
                "then run this again." % (upgraded_cpv, package_mask)
            )
        else:
            oper.Error(
                '\nUpgraded package "%s" is masked somehow (See full '
                "emerge output above). Address that and then run this "
                "again." % upgraded_cpv
            )

    def _PkgUpgradeStaged(self, upstream_cpv):
        """Return True if package upgrade is already staged."""
        ebuild_path = Upgrader._GetEbuildPathFromCpv(upstream_cpv)
        status = self._stable_repo_status.get(ebuild_path, None)
        return status == "A"

    def _AnyChangesStaged(self):
        """Return True if any local changes are staged in stable repo."""
        # Don't count files with '??' status - they aren't staged.
        files = [f for (f, s) in self._stable_repo_status.items() if s != "??"]
        return bool(len(files))

    def _StashChanges(self) -> None:
        """Run 'git stash save' on stable repo."""
        # Only one level of stashing expected/supported.
        self._RunGit(
            self._stable_repo,
            ["stash", "save"],
            stdout=True,
            stderr=subprocess.STDOUT,
        )
        self._stable_repo_stashed = True

    def _UnstashAnyChanges(self) -> None:
        """Unstash any changes in stable repo."""
        # Only one level of stashing expected/supported.
        if self._stable_repo_stashed:
            self._RunGit(
                self._stable_repo,
                ["stash", "pop", "--index"],
                stdout=True,
                stderr=subprocess.STDOUT,
            )
            self._stable_repo_stashed = False

    def _DropAnyStashedChanges(self) -> None:
        """Drop any stashed changes in stable repo."""
        # Only one level of stashing expected/supported.
        if self._stable_repo_stashed:
            self._RunGit(
                self._stable_repo,
                ["stash", "drop"],
                stdout=True,
                stderr=subprocess.STDOUT,
            )
            self._stable_repo_stashed = False

    def _CopyUpstreamPackage(self, upstream_cpv):
        """Upgrades package in |upstream_cpv| to the version in |upstream_cpv|.

        Returns:
            The upstream_cpv if the package was upgraded, None otherwise.
        """
        oper.Notice("Copying %s from upstream." % upstream_cpv)

        # pylint: disable=unpacking-non-sequence
        (cat, pkgname, _version, _rev) = portage.versions.catpkgsplit(
            upstream_cpv
        )
        # pylint: enable=unpacking-non-sequence
        ebuild = upstream_cpv.replace(cat + "/", "") + ".ebuild"
        catpkgsubdir = os.path.join(cat, pkgname)
        pkgdir = os.path.join(self._stable_repo, catpkgsubdir)
        upstream_pkgdir = os.path.join(self._upstream, cat, pkgname)

        # Fail early if upstream_cpv ebuild is not found
        upstream_ebuild_path = os.path.join(upstream_pkgdir, ebuild)
        if not os.path.exists(upstream_ebuild_path):
            # Note: this should only be possible during unit tests.
            raise RuntimeError(
                'Cannot find upstream ebuild at "%s"' % upstream_ebuild_path
            )

        # If pkgdir already exists, remove everything except files we maintain.
        # Note that git will remove a parent directory when it removes
        # the last item in the directory.
        if os.path.exists(pkgdir):
            items = set(
                x
                for x in os.listdir(pkgdir)
                if not x.endswith(".bashrc") and x != "cros"
            )
            items -= CROS_AUTHORED_FILES
            items = [os.path.join(catpkgsubdir, x) for x in items]
            if items:
                args = ["rm", "-rf", "--ignore-unmatch"] + items
                self._RunGit(self._stable_repo, args, stdout=True)
                # Now delete any files that git doesn't know about.
                for item in items:
                    osutils.SafeUnlink(os.path.join(self._stable_repo, item))

        osutils.SafeMakedirs(pkgdir)

        # Grab all non-ebuilds from upstream plus the specific ebuild requested.
        items = os.listdir(upstream_pkgdir)
        for item in items:
            if not item.endswith(".ebuild") or item == ebuild:
                src = os.path.join(upstream_pkgdir, item)
                dst = os.path.join(pkgdir, item)
                if os.path.isdir(src):
                    shutil.copytree(src, dst, symlinks=True)
                else:
                    shutil.copy2(src, dst)

        # Now copy any eclasses that this package requires.
        eclass = self._IdentifyNeededEclass(upstream_cpv)
        while eclass and self._CopyUpstreamEclass(eclass):
            eclass = self._IdentifyNeededEclass(upstream_cpv)

        return upstream_cpv

    def _StabilizeEbuild(self, ebuild_path) -> None:
        """Edit keywords to stablize ebuild at |ebuild_path| on current arch."""
        oper.Notice("Editing %r to mark it stable for everyone" % ebuild_path)

        # Regexp to search for KEYWORDS="...".
        keywords_regexp = re.compile(r'^(\s*KEYWORDS=")[^"]*(")', re.MULTILINE)

        # Read in entire ebuild.
        content = osutils.ReadFile(ebuild_path)

        # Replace all KEYWORDS with "*".
        content = re.sub(keywords_regexp, r"\1*\2", content)

        # Write ebuild file back out.
        osutils.WriteFile(ebuild_path, content)

    def _FixPythonCompat(self, ebuild_path) -> None:
        """Edit PYTHON_COMPAT to cover the python versions used by ChromeOS."""
        oper.Notice(f"Fixing up PYTHON_COMPAT for {ebuild_path!r}")

        # Regexp to search for PYTHON_COMPAT="...".
        python_regexp = re.compile(
            r"^(\s*PYTHON_COMPAT=\()[^)]*(\))", re.MULTILINE
        )

        # Read in entire ebuild.
        content = osutils.ReadFile(ebuild_path)

        # Set PYTHON_COMPAT to "( python3_{8..12} )".
        content = re.sub(python_regexp, r"\1 python3_{8..12} \2", content)

        # Write ebuild file back out.
        osutils.WriteFile(ebuild_path, content)

    def _CopyUpstreamEclass(self, eclass):
        """Upgrades eclass in |eclass| to upstream copy.

        Does not do the copy if the eclass already exists locally and
        is identical to the upstream version.

        Returns:
            True if the copy was done.
        """
        eclass_subpath = os.path.join("eclass", eclass)
        upstream_path = os.path.join(self._upstream, eclass_subpath)
        local_path = os.path.join(self._stable_repo, eclass_subpath)

        if os.path.exists(upstream_path):
            if os.path.exists(local_path) and filecmp.cmp(
                upstream_path, local_path
            ):
                return False
            else:
                oper.Notice("Copying %s from upstream." % eclass)
                osutils.SafeMakedirs(os.path.dirname(local_path))
                shutil.copy2(upstream_path, local_path)
                self._RunGit(self._stable_repo, ["add", eclass_subpath])
                return True

        raise RuntimeError(
            'Cannot find upstream "%s".  Looked at "%s"'
            % (eclass, upstream_path)
        )

    def _GetPackageUpgradeState(self, pinfo):
        """Return state value for package in |pinfo|."""
        # See whether this specific cpv exists upstream.
        cpv = pinfo.cpv
        cpv_exists_upstream = bool(
            cpv and self._FindUpstreamCPV(cpv, unstable_ok=True)
        )

        # The value in pinfo.cpv_cmp_upstream represents a comparison of cpv
        # version and the upstream version, where:
        # 0 = current, >0 = outdated, <0 = futuristic!

        # Convention is that anything not in portage overlay has been altered.
        overlay = pinfo.overlay
        locally_patched = overlay not in (
            NOT_APPLICABLE,
            self.UPSTREAM_OVERLAY_NAME,
            self.STABLE_OVERLAY_NAME,
        )
        locally_duplicated = locally_patched and cpv_exists_upstream

        # Gather status details for this package
        if pinfo.cpv_cmp_upstream is None:
            # No upstream cpv to compare to (although this might include a
            # restriction to only stable upstream versions). This is concerning
            # if the package is coming from 'portage' or 'portage-stable'
            # overlays.
            if locally_patched and pinfo.latest_upstream_cpv is None:
                state = utable.UpgradeTable.STATE_LOCAL_ONLY
            elif not cpv:
                state = utable.UpgradeTable.STATE_UPSTREAM_ONLY
            else:
                state = utable.UpgradeTable.STATE_UNKNOWN
        elif pinfo.cpv_cmp_upstream > 0:
            if locally_duplicated:
                state = utable.UpgradeTable.STATE_NEEDS_UPGRADE_AND_DUPLICATED
            elif locally_patched:
                state = utable.UpgradeTable.STATE_NEEDS_UPGRADE_AND_PATCHED
            else:
                state = utable.UpgradeTable.STATE_NEEDS_UPGRADE
        elif locally_duplicated:
            state = utable.UpgradeTable.STATE_DUPLICATED
        elif locally_patched:
            state = utable.UpgradeTable.STATE_PATCHED
        else:
            state = utable.UpgradeTable.STATE_CURRENT

        return state

    # TODO(mtennant): Generate output from finished table instead.
    def _PrintPackageLine(self, pinfo) -> None:
        """Print a brief one-line report of package status."""
        upstream_cpv = pinfo.upstream_cpv
        if pinfo.upgraded_cpv:
            action_stat = " (UPGRADED)"
        else:
            action_stat = ""

        up_stat = {
            utable.UpgradeTable.STATE_UNKNOWN: " no package found upstream!",
            utable.UpgradeTable.STATE_LOCAL_ONLY: " (exists locally only)",
            utable.UpgradeTable.STATE_NEEDS_UPGRADE: " -> %s" % upstream_cpv,
            utable.UpgradeTable.STATE_NEEDS_UPGRADE_AND_PATCHED: (
                " <-> %s" % upstream_cpv
            ),
            utable.UpgradeTable.STATE_NEEDS_UPGRADE_AND_DUPLICATED: (
                " (locally duplicated) <-> %s" % upstream_cpv
            ),
            utable.UpgradeTable.STATE_PATCHED: " <- %s" % upstream_cpv,
            utable.UpgradeTable.STATE_DUPLICATED: " (locally duplicated)",
            utable.UpgradeTable.STATE_CURRENT: " (current)",
        }[pinfo.state]

        oper.Info(
            "[%s] %s%s%s" % (pinfo.overlay, pinfo.cpv, up_stat, action_stat)
        )

    def _UpgradePackage(self, pinfo):
        """Gathers upgrade status for pkg, performs upgrade if requested.

        The upgrade is performed only if the package is outdated and --upgrade
        is specified.

        The |pinfo| must have the following entries:
        package, category, package_name

        Regardless, the following attributes in |pinfo| are filled in:
        stable_upstream_cpv
        latest_upstream_cpv
        upstream_cpv (one of the above, depending on --stable-only option)
        upgrade_cpv (if upgrade performed)
        """
        cpv = pinfo.cpv
        catpkg = pinfo.package
        pinfo.stable_upstream_cpv = self._FindUpstreamCPV(catpkg)
        pinfo.latest_upstream_cpv = self._FindUpstreamCPV(
            catpkg, unstable_ok=True
        )

        # The upstream version can be either latest stable or latest overall, or
        # specified explicitly by the user at the command line. In the latter
        # case, 'upstream_cpv' will already be set.
        if not pinfo.upstream_cpv:
            if not self._unstable_ok:
                pinfo.upstream_cpv = pinfo.stable_upstream_cpv
            else:
                pinfo.upstream_cpv = pinfo.latest_upstream_cpv

        # Perform the actual upgrade, if requested.
        pinfo.cpv_cmp_upstream = None
        pinfo.upgraded_cpv = None
        if pinfo.upstream_cpv:
            # cpv_cmp_upstream values:
            #   0 = current, >0 = outdated, <0 = futuristic!
            pinfo.cpv_cmp_upstream = Upgrader._CmpCpv(pinfo.upstream_cpv, cpv)

            # Determine whether upgrade of this package is requested.
            if self._PkgUpgradeRequested(pinfo):
                if self._PkgUpgradeStaged(pinfo.upstream_cpv):
                    oper.Notice(
                        "Determined that %s is already staged."
                        % pinfo.upstream_cpv
                    )
                    pinfo.upgraded_cpv = pinfo.upstream_cpv
                elif pinfo.cpv_cmp_upstream > 0:
                    pinfo.upgraded_cpv = self._CopyUpstreamPackage(
                        pinfo.upstream_cpv
                    )
                elif pinfo.cpv_cmp_upstream == 0:
                    if self._force:
                        oper.Notice(
                            "Forcing upgrade of existing %s."
                            % pinfo.upstream_cpv
                        )
                        upgraded_cpv = self._CopyUpstreamPackage(
                            pinfo.upstream_cpv
                        )
                        pinfo.upgraded_cpv = upgraded_cpv
                    else:
                        oper.Warning(
                            "Not upgrading %s; it already exists in source.\n"
                            "To force upgrade of this version specify --force."
                            % pinfo.upstream_cpv
                        )
        elif self._PkgUpgradeRequested(pinfo):
            raise RuntimeError(
                "Unable to find upstream package for upgrading %s." % catpkg
            )

        if pinfo.upgraded_cpv:
            # Deal with keywords now. We always run this logic as we sometimes
            # will stabilizing keywords other than just our own (the unsupported
            # arches).
            self._SetUpgradedMaskBits(pinfo)
            ebuild_path = Upgrader._GetEbuildPathFromCpv(pinfo.upgraded_cpv)
            self._StabilizeEbuild(os.path.join(self._stable_repo, ebuild_path))
            self._FixPythonCompat(os.path.join(self._stable_repo, ebuild_path))

            # Add all new package files to git.
            self._RunGit(self._stable_repo, ["add", pinfo.package])

            # Update profiles/categories.
            self._UpdateCategories(pinfo)

        return bool(pinfo.upgraded_cpv)

    def _UpdateCategories(self, pinfo) -> None:
        """Update profiles/categories to include category in |pinfo|."""

        if pinfo.category not in self._stable_repo_categories:
            self._stable_repo_categories.add(pinfo.category)
            self._WriteStableRepoCategories()

    def _VerifyPackageUpgrade(self, pinfo) -> None:
        """Verify that the upgraded package in |pinfo| passes checks."""
        self._VerifyEbuildOverlay(
            pinfo.upgraded_cpv,
            self.STABLE_OVERLAY_NAME,
            pinfo.cpv_cmp_upstream == 0,
        )

    def _PackageReport(self, pinfo) -> None:
        """Report on whatever was done with package in |pinfo|."""

        pinfo.state = self._GetPackageUpgradeState(pinfo)

        if self._verbose:
            # Print a quick summary of package status.
            self._PrintPackageLine(pinfo)

        # Remember this package for commit summary later on.
        self._upgraded_packages.append(pinfo)

    @staticmethod
    def _ExtractUpgradedPkgs(upgrade_lines):
        """Extracts list of packages from standard commit |upgrade_lines|."""
        # Expecting message lines like this (return just package names):
        # Upgraded sys-libs/ncurses to version 5.7-r7 on amd64, arm, x86
        # Upgraded sys-apps/less to version 441 on amd64, arm
        # Upgraded sys-apps/less to version 442 on x86
        pkgs = set()
        regexp = re.compile(r"^%s\s+\S+/(\S+)\s" % UPGRADED)
        for line in upgrade_lines:
            match = regexp.search(line)
            if match:
                pkgs.add(match.group(1))

        return sorted(pkgs)

    @staticmethod
    def _CreateCommitMessage(upgrade_lines, remaining_lines=None):
        """Create appropriate commit message for upgrades in |upgrade_lines|."""
        message = None
        upgrade_pkgs = Upgrader._ExtractUpgradedPkgs(upgrade_lines)
        upgrade_count = len(upgrade_pkgs)
        upgrade_str = "\n".join(upgrade_lines)
        if upgrade_count < 6:
            message = "%s: upgraded package%s to upstream" % (
                ", ".join(upgrade_pkgs),
                "" if upgrade_count == 1 else "s",
            )
        else:
            message = "Upgraded the following %d packages" % upgrade_count
        message += "\n\n" + upgrade_str + "\n"

        if remaining_lines:
            # Keep previous remaining lines verbatim.
            message += "\n%s\n" % "\n".join(remaining_lines)
        else:
            # The space before <fill-in> (at least for TEST=) fails pre-submit
            # check, which is the intention here.
            message += "\nBUG= <fill-in>"
            message += "\nTEST= <fill-in>"

        return message

    def _AmendCommitMessage(self, upgrade_lines):
        """Create commit message combining |upgrade_lines| with last commit."""
        # First get the body of the last commit message.
        git_cmd = ["show", "-s", "--format=%b"]
        result = self._RunGit(self._stable_repo, git_cmd, stdout=True)
        body = result.stdout

        remaining_lines = []
        # Extract the upgrade_lines of last commit.  Everything after the
        # empty line is preserved verbatim.
        # Expecting message body like this:
        # Upgraded sys-libs/ncurses to version 5.7-r7 on amd64, arm, x86
        # Upgraded sys-apps/less to version 441 on amd64, arm, x86
        #
        # BUG=chromium-os:20923
        # TEST=trybot run of chromiumos-sdk
        before_break = True
        for line in body.split("\n"):
            if not before_break:
                remaining_lines.append(line)
            elif line:
                if re.search(r"^%s\s+" % UPGRADED, line):
                    upgrade_lines.append(line)
                else:
                    # If the lines in the message body are not in the expected
                    # format simply push them to the end of the new commit
                    # message body, but left intact.
                    oper.Warning(
                        "It looks like the existing commit message "
                        "that you are amending was not generated by\n"
                        "this utility.  Appending previous commit "
                        "message to newly generated message."
                    )
                    before_break = False
                    remaining_lines.append(line)
            else:
                before_break = False

        return self._CreateCommitMessage(upgrade_lines, remaining_lines)

    def _GiveEmergeResults(self, pinfolist) -> None:
        """Summarize emerge checks, raise RuntimeError if there is a problem."""

        upgraded_pinfos = [pinfo for pinfo in pinfolist if pinfo.upgraded_cpv]
        upgraded_cpvs = [pinfo.upgraded_cpv for pinfo in upgraded_pinfos]
        masked_cpvs = {
            pinfo.upgraded_cpv
            for pinfo in upgraded_pinfos
            if not pinfo.upgraded_unmasked
        }

        (ok, cmd, output) = self._AreEmergeable(upgraded_cpvs)

        if masked_cpvs:
            # If any of the upgraded_cpvs are masked, then emerge should have
            # failed.  Give a helpful message.  If it didn't fail then panic.
            if ok:
                raise RuntimeError(
                    "Emerge passed for masked package(s)!  Something "
                    "fishy here. Emerge output follows:\n%s\n"
                    "Show this to the build team." % output
                )

            else:
                oper.Error(
                    '\nEmerge output for "%s" on %s follows:'
                    % (cmd, self._curr_arch)
                )
                print(output)
                for masked_cpv in masked_cpvs:
                    self._GiveMaskedError(masked_cpv, output)
                raise RuntimeError(
                    "\nOne or more upgraded packages are masked (see above)."
                )

        if ok:
            oper.Notice(
                "Confirmed that all upgraded packages can be emerged "
                "on %s after upgrade." % self._curr_board
            )
        else:
            oper.Error(
                "Packages cannot be emerged after upgrade.  The output "
                'of "%s" follows:' % cmd
            )
            print(output)
            raise RuntimeError(
                "Failed to complete upgrades on %s (see above). "
                "Address the emerge errors before continuing."
                % self._curr_board
            )

    def _UpgradePackages(self, pinfolist) -> None:
        """Given a list of cpv pinfos, adds the upstream cpv to the pinfos."""
        try:
            upgrades_this_run = False
            for pinfo in pinfolist:
                if self._UpgradePackage(pinfo):
                    self._upgrade_cnt += 1
                    upgrades_this_run = True

            # The verification of upgrades needs to happen after upgrades are
            # done. The reason is that it cannot be guaranteed that pinfolist is
            # ordered such that dependencies are satisified after each
            # individual upgrade, because one or more of the packages may only
            # exist upstream.
            for pinfo in pinfolist:
                if pinfo.upgraded_cpv:
                    self._VerifyPackageUpgrade(pinfo)

                self._PackageReport(pinfo)

            if upgrades_this_run:
                self._GiveEmergeResults(pinfolist)

            if self._IsInUpgradeMode():
                # If there were any ebuilds staged before running this script,
                # then make sure they were targeted in pinfolist. If not, abort.
                self._CheckStagedUpgrades(pinfolist)
        except RuntimeError as ex:
            oper.Error(str(ex))

            raise RuntimeError(
                "\nTo reset all changes in %s now:\n"
                " cd %s; git reset --hard; cd -"
                % (self._stable_repo, self._stable_repo)
            )
            # Allow the changes to stay staged so that the user can attempt to
            # address the issue (perhaps an edit to package.mask is required, or
            # another package must also be upgraded).

    def _CheckStagedUpgrades(self, pinfolist) -> None:
        """Raise RuntimeError if staged upgrades are not also in |pinfolist|."""
        # This deals with the situation where a previous upgrade run staged one
        # or more package upgrades, but did not commit them because it found an
        # error of some kind.  This is ok, as long as subsequent runs continue
        # to request an upgrade of that package again (presumably with the
        # problem fixed). However, if a subsequent run does not mention that
        # package then it should abort.  The user must reset those staged
        # changes first.

        if self._stable_repo_status:
            err_msgs = []

            # Go over files with pre-existing git statuses.
            ebuilds = [
                x for x in self._stable_repo_status if x.endswith(".ebuild")
            ]

            for ebuild in ebuilds:
                status = self._stable_repo_status[ebuild]
                (_overlay, cat, pn, _pv) = self._SplitEBuildPath(ebuild)
                package = "%s/%s" % (cat, pn)

                # As long as this package is involved in an upgrade this is
                # fine.
                matching_pinfos = [
                    pi for pi in pinfolist if pi.package == package
                ]
                if not matching_pinfos:
                    err_msgs.append(
                        "Staged %s (status=%s) is not an upgrade target."
                        % (ebuild, status)
                    )

            if err_msgs:
                raise RuntimeError(
                    "%s\nAdd to upgrade targets or reset staged changes."
                    % "\n".join(err_msgs)
                )

    def _GenParallelEmergeArgv(self, args):
        """Create argv for parallel_emerge using current options and |args|."""
        argv = ["--emptytree", "--pretend"]
        if self._curr_board and self._curr_board != self.HOST_BOARD:
            argv.append("--board=%s" % self._curr_board)
        if not self._verbose:
            argv.append("--quiet")
        if self._rdeps:
            argv.append("--root-deps=rdeps")
        argv.extend(args)

        return argv

    def _SetPortTree(self, settings, trees) -> None:
        """Set self._porttree from portage |settings| and |trees|."""
        root = settings["ROOT"]
        self._porttree = trees[root]["porttree"]

    def _GetPortageDBAPI(self):
        """Retrieve the Portage dbapi object, if available."""
        try:
            return self._porttree.dbapi
        except AttributeError:
            return None

    def _CreatePInfoFromCPV(self, cpv, cpv_key=None):
        """Return a basic pinfo object created from |cpv|."""
        pinfo = PInfo()
        self._FillPInfoFromCPV(pinfo, cpv, cpv_key)
        return pinfo

    def _FillPInfoFromCPV(self, pinfo, cpv, cpv_key=None) -> None:
        """Flesh out |pinfo| from |cpv|."""
        pkg = Upgrader._GetCatPkgFromCpv(cpv)
        (cat, pn) = pkg.split("/")

        pinfo.cpv = None
        pinfo.upstream_cpv = None

        pinfo.package = pkg
        pinfo.package_name = pn
        pinfo.category = cat

        if cpv_key:
            setattr(pinfo, cpv_key, cpv)

    def _GetCurrentVersions(self, target_pinfolist):
        """Returns a list of pkg pinfos of the current package dependencies.

        The dependencies are taken from giving the 'package' values in each
        pinfo of |target_pinfolist| to (parallel_)emerge.

        The returned list is ordered such that the dependencies of any mentioned
        package occur earlier in the list.
        """
        emerge_args = []
        for pinfo in target_pinfolist:
            local_cpv = pinfo.cpv
            if local_cpv and local_cpv != WORLD_TARGET:
                emerge_args.append("=" + local_cpv)
            else:
                emerge_args.append(pinfo.package)
        argv = self._GenParallelEmergeArgv(emerge_args)

        deps = depgraph.DepGraphGenerator()
        deps.Initialize(argv)

        try:
            deps_tree, deps_info, _ = deps.GenDependencyTree()
        except SystemExit:
            oper.Error(
                "Run of parallel_emerge exited with error while assembling"
                " package dependencies (error message should be above).\n"
                "Command effectively was:\n%s"
                % " ".join(["parallel_emerge"] + argv)
            )
            oper.Error("Address the source of the error, then run again.")
            raise
        self._SetPortTree(deps.emerge.settings, deps.emerge.trees)
        self._deps_graph = deps.GenDependencyGraph(deps_tree, deps_info)

        cpvlist = Upgrader._GetPreOrderDepGraph(self._deps_graph)
        cpvlist.reverse()

        pinfolist = []
        for cpv in cpvlist:
            # See if this cpv was in target_pinfolist
            is_target = False
            for pinfo in target_pinfolist:
                if cpv == pinfo.cpv:
                    pinfolist.append(pinfo)
                    is_target = True
                    break
            if not is_target:
                pinfolist.append(self._CreatePInfoFromCPV(cpv, cpv_key="cpv"))

        return pinfolist

    def _FinalizeLocalPInfolist(self, orig_pinfolist):
        """Filters and fleshes out |orig_pinfolist|, returns new list.

        Each pinfo object is assumed to have entries for:
        cpv, package, package_name, category
        """
        pinfolist = []
        for pinfo in orig_pinfolist:
            # No need to report or try to upgrade chromeos-base packages.
            if pinfo.category == "chromeos-base":
                continue

            dbapi = self._GetPortageDBAPI()
            ebuild_path = dbapi.findname2(pinfo.cpv)[0]
            if not ebuild_path:
                # This has only happened once.  See https://crbug.com/209254.
                # In that case, this meant the package, while in the deps graph,
                # was actually to be uninstalled.  How is that possible?  The
                # package was newly added to package.provided.  So skip it.
                oper.Notice(
                    "Skipping %r from deps graph, as it appears to be"
                    " scheduled for uninstall." % pinfo.cpv
                )
                continue

            (overlay, _cat, pn, pv) = self._SplitEBuildPath(ebuild_path)
            ver_rev = pv.replace(pn + "-", "")
            (slot,) = dbapi.aux_get(pinfo.cpv, ["SLOT"])

            pinfo.slot = slot
            pinfo.overlay = overlay
            pinfo.version_rev = ver_rev
            pinfo.package_ver = pv

            pinfolist.append(pinfo)

        return pinfolist

    # TODO(mtennant): It is likely this method can be yanked now that all
    # attributes in PInfo are initialized to something (None).
    # TODO(mtennant): This should probably not return anything, since it
    # also modifies the list that is passed in.
    def _FinalizeUpstreamPInfolist(self, pinfolist):
        """Adds missing values in upstream |pinfolist|, returns list."""

        for pinfo in pinfolist:
            pinfo.slot = NOT_APPLICABLE
            pinfo.overlay = NOT_APPLICABLE
            pinfo.version_rev = NOT_APPLICABLE
            pinfo.package_ver = NOT_APPLICABLE

        return pinfolist

    def _ResolveAndVerifyArgs(self, args, upgrade_mode):
        """Resolve |args| to full pkgs, and check validity of each.

        Each argument will be resolved to a full category/packagename, if
        possible, by looking in both the local overlays and the upstream
        overlay. Any argument that cannot be resolved will raise a RuntimeError.

        Arguments that specify a specific version of a package are only
        allowed when |upgrade_mode| is True.

        The 'world' target is handled as a local package.

        Any errors will raise a RuntimeError.

        Return list of package pinfos, one for each argument.  Each will have:
        'user_arg' = Original command line argument package was resolved from
        'package'  = Resolved category/package_name
        'package_name' = package_name
        'category' = category (None for 'world' target)
        Packages found in local overlays will also have:
        'cpv'      = Current cpv ('world' for 'world' target)
        Packages found upstream will also have:
        'upstream_cpv' = Upstream cpv
        """
        pinfolist = []

        for arg in args:
            pinfo = PInfo(user_arg=arg)

            if arg == WORLD_TARGET:
                # The 'world' target is a special case. Consider it a valid
                # target locally, but not an upstream package.
                pinfo.package = arg
                pinfo.package_name = arg
                pinfo.category = None
                pinfo.cpv = arg
            else:
                catpkg = Upgrader._GetCatPkgFromCpv(arg)
                verrev = Upgrader._GetVerRevFromCpv(arg)

                if verrev and not upgrade_mode:
                    raise RuntimeError(
                        "Specifying specific versions is only allowed "
                        "in upgrade mode.  Do not know what to do with "
                        '"%s".' % arg
                    )

                # Local cpv search ignores version in argument, if any. If
                # version is in argument, though, it *must* be found upstream.
                local_arg = catpkg if catpkg else arg

                local_cpv = self._FindCurrentCPV(local_arg)
                upstream_cpv = self._FindUpstreamCPV(arg, self._unstable_ok)

                # Old-style virtual packages will resolve to their target
                # packages, which we do not want here because if the package
                # 'virtual/foo' was specified at the command line we want to try
                # upgrading the actual 'virtual/foo' package, not whatever
                # package equery resolves it to. This only matters when
                # 'virtual/foo' is currently an old-style virtual but a
                # new-style virtual for it exists upstream which we want to
                # upgrade to.  For new-style virtuals, equery will resolve
                # 'virtual/foo' to 'virtual/foo', which is fine.
                if arg.startswith("virtual/"):
                    if local_cpv and not local_cpv.startswith("virtual/"):
                        local_cpv = None

                if not upstream_cpv and upgrade_mode:
                    # See if --unstable-ok is required for this upstream
                    # version.
                    if not self._unstable_ok and self._FindUpstreamCPV(
                        arg, True
                    ):
                        raise RuntimeError(
                            'Upstream "%s" is unstable on %s.  Re-run with '
                            "--unstable-ok option?" % (arg, self._curr_arch)
                        )
                    else:
                        raise RuntimeError(
                            'Unable to find "%s" upstream on %s.'
                            % (arg, self._curr_arch)
                        )

                any_cpv = local_cpv if local_cpv else upstream_cpv
                if not any_cpv:
                    msg = (
                        f'Unable to resolve "{arg}" as a package either local '
                        "or upstream."
                    )
                    if arg.find("/") < 0:
                        msg = (
                            msg
                            + " Try specifying the full category/package_name."
                        )

                    raise RuntimeError(msg)

                self._FillPInfoFromCPV(pinfo, any_cpv)
                pinfo.cpv = local_cpv
                pinfo.upstream_cpv = upstream_cpv
                if local_cpv and upstream_cpv:
                    oper.Notice(
                        'Resolved "%s" to "%s" (local) and "%s" (upstream).'
                        % (arg, local_cpv, upstream_cpv)
                    )
                elif local_cpv:
                    oper.Notice(
                        'Resolved "%s" to "%s" (local).' % (arg, local_cpv)
                    )
                elif upstream_cpv:
                    oper.Notice(
                        'Resolved "%s" to "%s" (upstream).'
                        % (arg, upstream_cpv)
                    )

            pinfolist.append(pinfo)

        return pinfolist

    def _DowngradeEAPI(self) -> None:
        """Downgrade to supported EAPI for requested packages."""
        oper.Notice(f"Downgrading EAPI version for {self._args}.")
        pkg_dirs = []
        envvars = self._GenPortageEnvvars(
            "*",
            unstable_ok=True,
            portdir=self._upstream,
            portage_configroot=self._emptydir,
        )
        # Construct the upstream package path for each requested package.
        for pkg in self._args:
            result = self._EqueryWhich(pkg, envvars)
            if result:
                (_overlay, cat, pn, _pv) = result
                pkg_dirs.append(os.path.join(self._upstream, cat, pn))
            elif "/" in pkg:
                # If there are no EAPI<8 packages equery will fail so provide
                # a fallback.
                cat, pn = pkg.split("/", 2)
                pkg_dirs.append(os.path.join(self._upstream, cat, pn))

        try:
            # Compile a list of ebuild files to be processed.
            ebuild_files = [
                f
                for d in pkg_dirs
                for f in glob.glob(os.path.join(d, "*.ebuild"))
            ]
            # Replace EAPI version 8 with 7 for each ebuild file.
            for ebuild in ebuild_files:
                with open(ebuild, "r+", encoding="utf-8") as f:
                    changed = False
                    lines = []
                    for line in f.readlines():
                        if line.startswith("EAPI=") and "8" in line:
                            lines.append(line.replace("8", "7"))
                            changed = True
                        else:
                            lines.append(line)
                    if changed:
                        f.seek(0)
                        f.writelines(lines)
        except OSError as e:
            oper.Error(f"Failed to downgrade ebuild file(s) {e}")

    def PrepareToRun(self) -> None:
        """Checkout upstream gentoo if necessary, and any other prep steps."""
        if os.path.exists(self._upstream):
            if self._local_only:
                oper.Notice(
                    "Using upstream cache as-is (no network) %s."
                    % self._upstream
                )
            else:
                # Recheck the pathway; it's possible in switching off
                # alternates, this was converted down to a depth=1 repo.

                oper.Notice(
                    "Updating previously created upstream cache at %s."
                    % self._upstream
                )
                self._RunGit(
                    self._upstream,
                    [
                        "remote",
                        "set-url",
                        self.GIT_REMOTE,
                        self.PORTAGE_GIT_URL,
                    ],
                )
                self._RunGit(
                    self._upstream,
                    [
                        "config",
                        "remote.%s.fetch" % self.GIT_REMOTE,
                        "+refs/heads/%s:refs/remotes/%s"
                        % (self.GIT_BRANCH, self.GIT_REMOTE_BRANCH),
                    ],
                )
                self._RunGit(self._upstream, ["remote", "update"])
                self._RunGit(
                    self._upstream,
                    ["checkout", "-f", self.GIT_REMOTE_BRANCH],
                    stdout=True,
                    stderr=subprocess.STDOUT,
                )
        else:
            if self._local_only:
                oper.Die(
                    "--local-only specified, but no local cache exists. "
                    "Re-run w/out --local-only to create cache automatically."
                )

            root = os.path.dirname(self._upstream)
            osutils.SafeMakedirs(root)
            # Create local copy of upstream gentoo.
            oper.Notice(
                "Cloning %s at %s as upstream reference."
                % (self.GIT_REMOTE_BRANCH, self._upstream)
            )
            name = os.path.basename(self._upstream)
            args = ["clone", "--branch", self.GIT_BRANCH]
            args += ["--depth", "1", self.PORTAGE_GIT_URL, name]
            self._RunGit(root, args)

            # Create a README file to explain its presence.
            with open(self._upstream + "-README", "w", encoding="utf-8") as f:
                f.write(
                    "Directory at %s is local copy of upstream "
                    "Gentoo/Portage packages. Used by cros_portage_upgrade.\n"
                    "Feel free to delete if you want the space back.\n"
                    % self._upstream
                )

        # TODO(b/242758296) Remove this when ChromeOS supports EAPI 8.
        self._DowngradeEAPI()

        # An empty directory is needed to trick equery later.
        self._emptydir = tempfile.mkdtemp()

    def RunCompleted(self) -> None:
        """Undo any checkout of upstream gentoo if requested."""
        if self._no_upstream_cache:
            oper.Notice(
                "Removing upstream cache at %s as requested." % self._upstream
            )
            osutils.RmDir(self._upstream, ignore_missing=True)

            # Remove the README file, too.
            readmepath = self._upstream + "-README"
            osutils.SafeUnlink(readmepath)
        else:
            oper.Notice("Keeping upstream cache at %s." % self._upstream)

        if self._emptydir:
            osutils.RmDir(self._emptydir, ignore_missing=True)

    def CommitIsStaged(self):
        """Return True if upgrades are staged and ready for a commit."""
        return bool(self._upgrade_cnt)

    def Commit(self) -> None:
        """Commit whatever has been prepared in the stable repo."""
        # Lines for the body of the commit message.
        commit_lines = []
        # Overlays for upgraded packages in non-portage overlays.
        pkg_overlays = {}

        for pkg in sorted(self._upgraded_packages, key=lambda x: x.package):
            upgraded_ver = self._GetVerRevFromCpv(pkg.upgraded_cpv)
            commit_lines.append(
                f"{UPGRADED} {pkg.package} to version {upgraded_ver}."
            )

            # Save the overlay this package is originally from, if the overlay
            # is not a Portage overlay (e.g. chromiumos-overlay).
            if pkg.overlay not in (
                NOT_APPLICABLE,
                self.UPSTREAM_OVERLAY_NAME,
                self.STABLE_OVERLAY_NAME,
            ):
                pkg_overlays[pkg.package] = pkg.overlay

        if commit_lines:
            if self._amend:
                message = self._AmendCommitMessage(commit_lines)
                self._RunGit(
                    self._stable_repo, ["commit", "--amend", "-m", message]
                )
            else:
                message = self._CreateCommitMessage(commit_lines)
                self._RunGit(self._stable_repo, ["commit", "-m", message])

            oper.Warning(
                "\n"
                "Upgrade changes committed (see above),"
                " but message needs edit BY YOU:\n"
                " cd %s; git commit --amend; cd -" % self._stable_repo
            )
            # See if any upgraded packages are in non-portage overlays now,
            # meaning they probably require a patch and should not go into
            # portage-stable.
            if pkg_overlays:
                # TODO(b/236161656): Fix.
                # pylint: disable-next=consider-using-dict-items
                lines = ["%s [%s]" % (p, pkg_overlays[p]) for p in pkg_overlays]
                oper.Warning(
                    "\n"
                    "The following packages were coming from a non-portage"
                    " overlay, which means they were probably patched.\n"
                    "You should consider whether the upgraded package"
                    " needs the same patches applied now.\n"
                    "If so, do not commit these changes in portage-stable."
                    " Instead, copy them to the applicable overlay dir.\n"
                    "%s" % "\n".join(lines)
                )
            oper.Notice(
                "\n"
                "To remove any individual file above from commit do:\n"
                " cd %s; git reset HEAD~ <filepath>; rm <filepath>;"
                " git commit --amend -C HEAD; cd -" % self._stable_repo
            )

            oper.Notice(
                "\n"
                "If you wish to undo all the changes to %s:\n"
                " cd %s; git reset --hard HEAD~; cd -"
                % (self.STABLE_OVERLAY_NAME, self._stable_repo)
            )

    def PreRunChecks(self) -> None:
        """Run any board-independent validation checks before Run is called."""
        # Upfront check(s) if upgrade is requested.
        if self._upgrade or self._upgrade_deep:
            # Stable source must be on branch.
            self._CheckStableRepoOnBranch()

    def RunBoard(self, board) -> None:
        """Runs the upgrader based on the supplied options and arguments.

        Currently just lists all package dependencies in pre-order along with
        potential upgrades.
        """
        # Preserve status report for entire stable repo (output of
        # 'git status -s').
        self._SaveStatusOnStableRepo()
        # Read contents of profiles/categories for later checks.
        self._LoadStableRepoCategories()

        self._porttree = None
        self._deps_graph = None

        self._curr_board = board
        self._curr_arch = Upgrader._FindBoardArch(board)
        upgrade_mode = self._IsInUpgradeMode()

        if self._AnyChangesStaged():
            self._StashChanges()

        try:
            target_pinfolist = self._ResolveAndVerifyArgs(
                self._args, upgrade_mode
            )
            upstream_only_pinfolist = [
                pi for pi in target_pinfolist if not pi.cpv
            ]
            if not upgrade_mode and upstream_only_pinfolist:
                # This means that not all arguments were found in local source,
                # which is only allowed in upgrade mode.
                msg = (
                    "The following packages were not found in current overlays"
                    " (but they do exist upstream):\n%s"
                    % "\n".join(
                        [pinfo.user_arg for pinfo in upstream_only_pinfolist]
                    )
                )
                raise RuntimeError(msg)

            full_pinfolist = None

            if self._upgrade:
                # Shallow upgrade mode only cares about targets as they were
                # found upstream.
                full_pinfolist = self._FinalizeUpstreamPInfolist(
                    target_pinfolist
                )
            else:
                # Assembling dependencies only matters in status report mode or
                # if --upgrade-deep was requested.
                local_target_pinfolist = [
                    pi for pi in target_pinfolist if pi.cpv
                ]
                if local_target_pinfolist:
                    oper.Notice("Assembling package dependencies.")
                    full_pinfolist = self._GetCurrentVersions(
                        local_target_pinfolist
                    )
                    full_pinfolist = self._FinalizeLocalPInfolist(
                        full_pinfolist
                    )
                else:
                    full_pinfolist = []

                # Append any command line targets that were not found in current
                # overlays. The idea is that they will still be found upstream
                # for upgrading.
                if upgrade_mode:
                    tmp_list = self._FinalizeUpstreamPInfolist(
                        upstream_only_pinfolist
                    )
                    full_pinfolist = full_pinfolist + tmp_list

            self._UnstashAnyChanges()
            self._UpgradePackages(full_pinfolist)

        finally:
            self._DropAnyStashedChanges()

    def SayGoodbye(self) -> None:
        """Print any final messages to user."""
        if not self._IsInUpgradeMode():
            # Without this message users are confused why running a script
            # with 'upgrade' in the name does not actually do an upgrade.
            oper.Warning(
                'Completed status report run.  To run in "upgrade"'
                " mode include the --upgrade option."
            )


def _BoardIsSetUp(board):
    """Return true if |board| has been setup."""
    return os.path.isdir(build_target_lib.get_default_sysroot_path(board))


def _CreateParser():
    """Create the parser object for command-line args."""
    epilog = (
        "\n"
        'There are essentially two "modes": status report mode and '
        "upgrade mode.\nStatus report mode is the default; upgrade "
        "mode is enabled by either --upgrade or --upgrade-deep.\n"
        "\n"
        "In either mode, packages can be specified in any manner "
        "commonly accepted by Portage tools.  For example:\n"
        " category/package_name\n"
        " package_name\n"
        " category/package_name-version (upgrade mode only)\n"
        "\n"
        "Status report mode will report on the status of the specified "
        "packages relative to upstream,\nwithout making any changes. "
        "In this mode, the specified packages are often high-level\n"
        'targets such as "virtual/target-os". '
        "The --unstable-ok option in this mode will make "
        'the upstream comparison (e.g. "needs update") be\n'
        "relative to the latest upstream version, stable or not.\n"
        "\n"
        "Upgrade mode will attempt to upgrade the specified "
        "packages to one of the following versions:\n"
        "1) The version specified in argument (e.g. foo/bar-1.2.3)\n"
        "2) The latest stable version upstream (the default)\n"
        "3) The latest overall version upstream (with --unstable-ok)\n"
        "\n"
        "Unlike with --upgrade, if --upgrade-deep is specified, "
        "then the package dependencies will also be upgraded.\n"
        "In upgrade mode, it is ok if the specified packages only "
        "exist upstream.\n"
        "The --force option can be used to do a package upgrade "
        "even if the local version matches the upstream version.\n"
        "\n"
        "Status report mode examples:\n"
        "> cros_portage_upgrade --board=arm-generic:x86-generic "
        " virtual/target-os\n"
        "> cros_portage_upgrade --unstable-ok --board=x86-mario "
        " virtual/target-os virtual/target-os-dev virtual/target-os-test\n"
        "Upgrade mode examples:\n"
        "> cros_portage_upgrade --board=arm-generic:x86-generic "
        "--upgrade sys-devel/gdb virtual/yacc\n"
        "> cros_portage_upgrade --unstable-ok --board=x86-mario "
        "--upgrade-deep gdata\n"
        "> cros_portage_upgrade --board=x86-generic --upgrade "
        "media-libs/libpng-1.2.45\n"
        "\n"
    )

    parser = commandline.ArgumentParser(
        epilog=epilog, default_log_level="notice"
    )
    parser.add_argument(
        "packages", nargs="*", default=None, help="Packages to process."
    )
    parser.add_argument(
        "--amend",
        action="store_true",
        default=False,
        help="Amend existing commit when doing upgrade.",
    )
    parser.add_argument(
        "--board", default=None, help="Target board(s), colon-separated"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        default=False,
        help="Force upgrade even if version already in source",
    )
    parser.add_argument(
        "--host",
        action="store_true",
        default=False,
        help="Host target pseudo-board",
    )
    parser.add_argument(
        "--no-upstream-cache",
        action="store_true",
        default=False,
        help="Do not preserve cached upstream for future runs",
    )
    parser.add_argument(
        "--rdeps",
        action="store_true",
        default=False,
        help="Use runtime dependencies only",
    )
    parser.add_argument(
        "--srcroot",
        type="str_path",
        default=os.path.join(constants.SOURCE_ROOT, "src"),
        help="Path to root src directory [default: %(default)s]",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        default=False,
        help="Upgrade target package(s) only",
    )
    parser.add_argument(
        "--upgrade-deep",
        action="store_true",
        default=False,
        help="Upgrade target package(s) and all dependencies",
    )
    parser.add_argument(
        "--upstream",
        type="str_path",
        default=Upgrader.UPSTREAM_TMP_REPO,
        help="Latest upstream repo location [default: %(default)s]",
    )
    parser.add_argument(
        "--unstable-ok",
        action="store_true",
        default=False,
        help="Use latest upstream ebuild, stable or not",
    )
    parser.add_argument(
        "-l",
        "--local-only",
        action="store_true",
        default=False,
        help="Do not attempt to update local portage cache",
    )
    return parser


def main(argv) -> None:
    """Main function."""
    parser = _CreateParser()
    options = parser.parse_args(argv)
    # TODO: Can't freeze until options.host modification below is sorted.
    # options.Freeze()

    oper.verbose = options.verbose

    #
    # Do some argument checking.
    #

    if not options.board and not options.host:
        options.host = True
        oper.Notice("Using the SDK (--host) by default for dependency checks.")

    if not options.packages:
        parser.print_usage()
        oper.Die("No packages provided.")

    # The --upgrade and --upgrade-deep options are mutually exclusive.
    if options.upgrade_deep and options.upgrade:
        parser.print_usage()
        oper.Die(
            "The --upgrade and --upgrade-deep options are mutually exclusive."
        )

    # The --force option only makes sense with --upgrade or --upgrade-deep.
    if options.force and not (options.upgrade or options.upgrade_deep):
        parser.print_usage()
        oper.Die("The --force option requires --upgrade or --upgrade-deep.")

    upgrader = Upgrader(options)
    upgrader.PreRunChecks()

    # Automatically handle board 'host' as 'amd64-host'.
    boards = []
    if options.board:
        boards = options.board.split(":")

        # Specifying --board=host is equivalent to --host.
        if "host" in boards:
            options.host = True

        boards = [b for b in boards if b != "host"]

    # Make sure host pseudo-board is run first.
    if options.host and Upgrader.HOST_BOARD not in boards:
        boards.insert(0, Upgrader.HOST_BOARD)
    elif Upgrader.HOST_BOARD in boards:
        boards = [b for b in boards if b != Upgrader.HOST_BOARD]
        boards.insert(0, Upgrader.HOST_BOARD)

    # Check that all boards have been setup first.
    for board in boards:
        if board != Upgrader.HOST_BOARD and not _BoardIsSetUp(board):
            parser.print_usage()
            oper.Die("You must setup the %s board first." % board)

    passed = True
    try:
        upgrader.PrepareToRun()

        for board in boards:
            oper.Notice("Running with board %s." % board)
            upgrader.RunBoard(board)
    except RuntimeError as ex:
        passed = False
        oper.Error(str(ex))

    finally:
        upgrader.RunCompleted()

    if not passed:
        oper.Die("Failed with above errors.")

    if upgrader.CommitIsStaged():
        upgrader.Commit()

    # TODO(mtennant): Move stdout output to here, rather than as-we-go.  That
    # way it won't come out for each board.  Base it on contents of final table.
    # Make verbose-dependent?

    upgrader.SayGoodbye()
