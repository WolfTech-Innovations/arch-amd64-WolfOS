# Copyright 2018 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Sysroot service."""

import datetime
import glob
import json
import logging
import multiprocessing
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import (
    Callable,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    TYPE_CHECKING,
    Union,
)
import urllib

from chromite.api.gen.chromiumos import prebuilts_cloud_pb2
from chromite.lib import binpkg
from chromite.lib import build_target_lib
from chromite.lib import cache
from chromite.lib import compression_lib
from chromite.lib import constants
from chromite.lib import cpupower_helper
from chromite.lib import cros_build_lib
from chromite.lib import gs
from chromite.lib import metrics_lib
from chromite.lib import osutils
from chromite.lib import path_util
from chromite.lib import portage_util
from chromite.lib import sysroot_lib
from chromite.lib import workon_helper
from chromite.lib.telemetry import trace
from chromite.service import binhost as binhost_service
from chromite.service import sdk as sdk_service


if TYPE_CHECKING:
    from chromite.lib import chroot_lib


tracer = trace.get_tracer(__name__)

_CHROME_PACKAGES = ("chromeos-base/chromeos-chrome", "chromeos-base/chrome-icu")

# A list of critical system packages that should never be incidentally
# reinstalled as a side effect of build_packages. All packages in this list
# are special cased to prefer matching installed versions, overriding the
# typical logic of upgrading to the newest available version.
#
# This list can't include any package that gets installed to a board!
# Packages such as LLVM or binutils must not be in this list as the normal
# rebuild logic must still apply to them for board targets.
#
# TODO(crbug/1050752): Remove this list once we figure out how to exclude
# toolchain packages from being upgraded transitively via BDEPEND relations.
_CRITICAL_SDK_PACKAGES = (
    "dev-lang/rust",
    "dev-lang/go",
    "sys-libs/glibc",
    "sys-devel/gcc",
)

_PACKAGE_LIST = List[Optional[str]]

# The default to use for --backtrack everywhere. Must be manually changed in
# update_chroot.
BACKTRACK_DEFAULT = 30

SYSROOT_ARCHIVE_FILE = "sysroot.tar.zst"
BAZEL_ALLPACKAGES_COMMAND_PROFILE_FILE = "/tmp/allpackages_command.profile.gz"
BAZEL_ALLPACKAGES_CQUERY_PROFILE_FILE = "/tmp/allpackages_cquery.profile.gz"
BAZEL_ALLPACKAGES_ACTION_LOGS_FILE = "/tmp/allpackages_action_logs.tar.gz"
BAZEL_ALLPACKAGES_EXEC_LOG_FILE = "/tmp/allpackages_exec_compact.log"
BAZEL_ALLPACKAGES_PREBUILTS_FILE = "/tmp/prebuilts.bzl"
BAZEL_ALLPACKAGES_GRAPH_LOG_FILE = "/tmp/allpackages_graph.log"
BAZEL_BUILD_EVENT_JSON_FILE_PATH = "/tmp/chromeos_bazel_build_events.json"
BAZEL_COMMAND = constants.CHROMITE_BIN_DIR / "bazel"


class Error(Exception):
    """Base error class for the module."""


class NoFilesError(Error):
    """When there are no files to archive."""


class InvalidArgumentsError(Error):
    """Invalid arguments."""


class NotInChrootError(Error):
    """When SetupBoard is run outside of the chroot."""


class UpdateChrootError(Error):
    """Error occurred when running update chroot."""

    def __init__(self, *args, failed_packages) -> None:
        super().__init__(*args)
        self.failed_packages = failed_packages


class SetupBoardRunConfig:
    """Value object for full setup board run configurations."""

    def __init__(
        self,
        set_default: bool = False,
        force: bool = False,
        usepkg: bool = True,
        jobs: Optional[int] = None,
        regen_configs: bool = False,
        quiet: bool = False,
        update_toolchain: bool = False,
        upgrade_chroot: bool = True,
        init_board_pkgs: bool = True,
        local_build: bool = False,
        toolchain_changed: bool = False,
        expanded_binhost_inheritance: bool = False,
        use_cq_prebuilts: bool = False,
        backtrack: int = BACKTRACK_DEFAULT,
        binhost_lookup_service_data: Optional[
            prebuilts_cloud_pb2.BinhostLookupServiceData
        ] = None,
    ) -> None:
        """Initialize method.

        Args:
            set_default: Whether to set the passed board as the default.
            force: Force a new sysroot creation when it already exists.
            usepkg: Whether to use binary packages to bootstrap.
            jobs: Max number of simultaneous packages to build.
            regen_configs: Whether to only regen the configs.
            quiet: Whether to print notification when sysroot exists.
            update_toolchain: Update the toolchain?
            upgrade_chroot: Upgrade the chroot before building?
            init_board_pkgs: Emerging packages to sysroot?
            local_build: Bootstrap only from local packages?
            toolchain_changed: Has a toolchain change occurred? Implies 'force'.
            expanded_binhost_inheritance: Allow expanded binhost inheritance.
            use_cq_prebuilts: Whether to use the prebuilts generated by CQ.
            backtrack: emerge --backtrack value.
            binhost_lookup_service_data: Data needed for fetching binhosts.
        """
        self.set_default = set_default
        self.force = force or toolchain_changed
        self.usepkg = usepkg
        self.jobs = jobs
        self.regen_configs = regen_configs
        self.quiet = quiet
        self.update_toolchain = update_toolchain
        self.update_chroot = upgrade_chroot
        self.init_board_pkgs = init_board_pkgs
        self.local_build = local_build
        self.expanded_binhost_inheritance = expanded_binhost_inheritance
        self.use_cq_prebuilts = use_cq_prebuilts
        self.backtrack = backtrack
        self.binhost_lookup_service_data = binhost_lookup_service_data

    def GetUpdateChrootArgs(
        self, toolchain_target: str
    ) -> sdk_service.UpdateArguments:
        """Create a list containing the relevant update_chroot arguments.

        Returns:
            The list of arguments
        """
        return sdk_service.UpdateArguments(
            build_source=not self.usepkg,
            toolchain_targets=[toolchain_target],
            jobs=self.jobs,
            backtrack=self.backtrack,
            update_toolchain=self.update_toolchain,
        )


class BuildPackagesRunConfig:
    """Value object to hold build packages run configs."""

    def __init__(
        self,
        usepkg: bool = True,
        packages: Optional[List[str]] = None,
        use_flags: Optional[List[str]] = None,
        use_remoteexec: bool = False,
        reproxy_cfg_file: str = "",
        incremental_build: bool = True,
        dryrun: bool = False,
        usepkgonly: bool = False,
        workon: bool = True,
        install_auto_test: bool = True,
        autosetgov: bool = False,
        autosetgov_sticky: bool = False,
        use_any_chrome: bool = True,
        internal_chrome: bool = False,
        eclean: bool = True,
        jobs: Optional[int] = None,
        local_pkg: bool = False,
        dev_image: bool = True,
        factory_image: bool = True,
        test_image: bool = True,
        debug_version: bool = True,
        backtrack: int = BACKTRACK_DEFAULT,
        bazel: bool = False,
        bazel_lite: bool = False,
        noclean: bool = False,
        binhost_lookup_service_data: Optional[
            prebuilts_cloud_pb2.BinhostLookupServiceData
        ] = None,
        timeout: datetime.datetime = None,
        bazel_use_remote_execution: bool = False,
    ) -> None:
        """Init method.

        Args:
            usepkg: Whether to use binpkgs or build from source. False currently
                triggers a local build, which will enable local reuse.
            packages: The list of packages to install, by default install all
                packages for the target.
            use_flags: A list of use flags to set.
            use_remoteexec: Whether to use RBE for remoteexec.
            reproxy_cfg_file: Config file for remoteexec
            incremental_build: Whether to treat the build as an incremental
                build or a fresh build. Always treating it as an incremental
                build is safe, but certain operations can be faster when we know
                we are doing a fresh build.
            dryrun: Whether to do a dryrun and not actually build any packages.
            usepkgonly: Only use binary packages to bootstrap; abort if any are
                missing.
            workon: Force-build workon packages.
            install_auto_test: Build autotest client code.
            autosetgov: Automatically set cpu governor to 'performance'.
            autosetgov_sticky: Remember --autosetgov setting for future runs.
            use_any_chrome: Use any Chrome prebuilt available, even if the
                prebuilt doesn't match exactly.
            internal_chrome: Build the internal version of chrome.
            eclean: Run eclean to delete old binpkgs.
            jobs: How many packages to build in parallel at maximum.
            local_pkg: Bootstrap from local packages instead of remote packages.
            dev_image: Build useful developer friendly utilities.
            factory_image: Build factory installer.
            test_image: Build packages required for testing.
            debug_version: Build debug versions of Chromium-OS-specific
                packages.
            backtrack: emerge --backtrack value.
            bazel: Whether to use Bazel to build packages.
            bazel_lite: Whether to perform lite Bazel build, which limits
                the set of target packages.
            noclean: Whether to set the noclean FEATURES flag.
            binhost_lookup_service_data: Data needed to fetch binhosts from the
                binhost lookup service.
            timeout: If set, the main build command will be aborted after this
                datetime.
            bazel_use_remote_execution: Whether Bazel builds should execute
                Bazel actions remotely.
        """
        self.usepkg = usepkg
        self.packages = packages
        self.use_flags = use_flags
        self.use_remoteexec = use_remoteexec
        self.reproxy_cfg_file = reproxy_cfg_file
        self.is_incremental = incremental_build
        self.dryrun = dryrun
        self.usepkgonly = usepkgonly
        self.workon = workon
        self.install_auto_test = install_auto_test
        self.autosetgov = autosetgov
        self.autosetgov_sticky = autosetgov_sticky
        self.use_any_chrome = use_any_chrome
        self.internal_chrome = internal_chrome
        self.eclean = eclean
        self.jobs = jobs
        self.local_pkg = local_pkg
        self.dev_image = dev_image
        self.factory_image = factory_image
        self.test_image = test_image
        self.debug_version = debug_version
        self.backtrack = backtrack
        self.bazel = bazel
        self.bazel_lite = bazel_lite
        self.noclean = noclean
        self.binhost_lookup_service_data = binhost_lookup_service_data
        self.timeout = timeout
        self.bazel_use_remote_execution = bazel_use_remote_execution

    def GetUseFlags(self) -> Optional[str]:
        """Get the use flags as a single string."""
        use_flags = os.environ.get("USE", "").split()

        if self.use_flags:
            use_flags.extend(self.use_flags)

        if self.internal_chrome:
            use_flags.append("chrome_internal")

        if not self.debug_version:
            use_flags.append("-cros-debug")

        return " ".join(use_flags) if use_flags else None

    def get_features(self) -> Optional[str]:
        """Get the features as a single string."""
        use_flags = os.environ.get("FEATURES", "").split()

        if self.noclean:
            use_flags.append("noclean")

        return " ".join(use_flags) if use_flags else None

    def GetExtraEnv(self) -> Dict[str, str]:
        """Get the extra env for this config."""
        env = {}

        use_flags = self.GetUseFlags()
        if use_flags:
            env["USE"] = use_flags

        features = self.get_features()
        if features:
            env["FEATURES"] = features

        if self.use_remoteexec:
            env["USE_REMOTEEXEC"] = "true"
            env["REPROXY_CFG_FILE"] = self.reproxy_cfg_file

        return env

    def GetPackages(self) -> List[str]:
        """Get the set of packages to build for this config."""
        if self.packages:
            return self.packages

        packages = [constants.TARGET_OS_PKG]

        if self.dev_image:
            packages.append(constants.TARGET_OS_DEV_PKG)

        if self.factory_image:
            # See platform/factory/README.md for context.
            packages.append(constants.TARGET_OS_FACTORY_PKG)
            packages.append(constants.TARGET_OS_FACTORY_SHIM_PKG)

        if self.test_image:
            packages.append(constants.TARGET_OS_TEST_PKG)

        if self.install_auto_test:
            packages.append("chromeos-base/autotest-all")

        return packages

    @metrics_lib.timed("service.sysroot.GetForceLocalBuildPackages")
    def GetForceLocalBuildPackages(
        self, sysroot: sysroot_lib.Sysroot
    ) -> _PACKAGE_LIST:
        """Get the set of force local build packages for this config.

        This includes:
            1. Getting packages for a test image.
            2. Getting packages and reverse dependencies for cros workon
                packages.
            3. Getting packages and reverse dependencies for base install
                packages.

        Args:
            sysroot: The sysroot to get packages for.

        Returns:
            A list of packages to build from source.

        Raises:
            cros_build_lib.RunCommandError
        """
        sysroot_path = Path(sysroot.path)
        force_local_build_packages = set()
        packages = self.GetPackages()
        metrics_prefix = "service.sysroot.GetForceLocalBuildPackages"

        cros_workon_packages = None
        if self.workon:
            cros_workon_packages = _GetCrosWorkonPackages(sysroot_path)

            # Any package that directly depends on an active cros_workon package
            # also needs to be rebuilt in order to be correctly built against
            # the current set of changes a user may have made to the cros_workon
            # package.
            if cros_workon_packages:
                force_local_build_packages.update(cros_workon_packages)

                with metrics_lib.timer(
                    f"{metrics_prefix}.CrosWorkonReverseDependencies"
                ):
                    reverse_dependencies = [
                        x.atom
                        for x in portage_util.GetReverseDependencies(
                            cros_workon_packages, sysroot_path
                        )
                    ]
                logging.info(
                    "The following packages depend directly on an active "
                    "cros_workon package and will be rebuilt: %s",
                    " ".join(reverse_dependencies),
                )
                force_local_build_packages.update(reverse_dependencies)

        # Determine base install packages and reverse dependencies when doing an
        # incremental build.
        if self.is_incremental:
            logging.info("Starting reverse dependency calculations...")

            # Temporarily modify the emerge flags so we can calculate the
            # revdeps on the modified packages.
            sim_emerge_flags = self.GetEmergeFlags()
            sim_emerge_flags.extend(
                [
                    "--pretend",
                    "--columns",
                    f'--reinstall-atoms={" ".join(packages)}',
                    f'--usepkg-exclude={" ".join(packages)}',
                ]
            )

            # cros-workon packages are always going to be force reinstalled, so
            # we add the forced reinstall behavior to the modified package
            # calculation. This is necessary to include when a user has already
            # installed a 9999 ebuild and is now reinstalling that package with
            # additional local changes, because otherwise the modified package
            # calculation would not see that a 'new' package is being installed.
            if cros_workon_packages:
                sim_emerge_flags.extend(
                    [
                        f'--reinstall-atoms={" ".join(cros_workon_packages)}',
                        f'--usepkg-exclude={" ".join(cros_workon_packages)}',
                    ]
                )

            revdeps_packages = _GetBaseInstallPackages(
                sysroot_path, sim_emerge_flags, packages
            )
            if revdeps_packages:
                force_local_build_packages.update(revdeps_packages)
                logging.info(
                    "Calculating reverse dependencies on packages: %s",
                    " ".join(revdeps_packages),
                )
                with metrics_lib.timer(f"{metrics_prefix}.ReverseDependencies"):
                    r_revdeps_packages = portage_util.GetReverseDependencies(
                        revdeps_packages, sysroot_path, indirect=True
                    )

                exclude_patterns = ["virtual/"]
                exclude_patterns.extend(_CHROME_PACKAGES)
                reverse_dependencies = [
                    x.atom
                    for x in r_revdeps_packages
                    if not any(p in x.atom for p in exclude_patterns)
                ]
                logging.info(
                    "Final reverse dependencies that will be rebuilt: %s",
                    " ".join(reverse_dependencies),
                )
                force_local_build_packages.update(reverse_dependencies)

        return list(force_local_build_packages)

    def GetEmergeFlags(self) -> List[str]:
        """Get the emerge flags for this config."""
        flags = [
            "-uDNv",
            f"--backtrack={self.backtrack}",
            "--newrepo",
            "--with-test-deps",
            "y",
        ]

        if self.use_any_chrome:
            for pkg in _CHROME_PACKAGES:
                flags.append(f"--force-remote-binary={pkg}")

        extra_board_flags = os.environ.get("EXTRA_BOARD_FLAGS", "").split()
        if extra_board_flags:
            flags.extend(extra_board_flags)

        if self.dryrun:
            flags.append("--pretend")

        if self.usepkg or self.local_pkg or self.usepkgonly:
            # Use binary packages. Include all build-time dependencies, so as to
            # avoid unnecessary differences between source and binary builds.
            flags.extend(["--getbinpkg", "--with-bdeps", "y"])
            if self.usepkgonly:
                flags.append("--usepkgonly")
            else:
                flags.append("--usepkg")

        if self.jobs:
            flags.append(f"--jobs={self.jobs}")

        return flags


@tracer.start_as_current_span("service.sysroot.SetupBoard")
def SetupBoard(
    target: "build_target_lib.BuildTarget",
    accept_licenses: Optional[str] = None,
    run_configs: Optional[SetupBoardRunConfig] = None,
) -> None:
    """Run the full process to setup a board's sysroot.

    This is the entry point to run the setup_board script.

    Args:
        target: The build target configuration.
        accept_licenses: The additional licenses to accept.
        run_configs: The run configs.

    Raises:
        sysroot_lib.ToolchainInstallError when the toolchain fails to install.
    """
    if not cros_build_lib.IsInsideChroot():
        raise NotInChrootError("SetupBoard must be run from inside the chroot")

    # Make sure we have valid run configs setup.
    run_configs = run_configs or SetupBoardRunConfig()

    sysroot = Create(target, run_configs, accept_licenses)

    if run_configs.regen_configs:
        # We're now done if we're only regenerating the configs.
        return

    InstallToolchain(target, sysroot, run_configs)


@tracer.start_as_current_span("service.sysroot.Create")
@osutils.rotate_log_file(constants.PORTAGE_DEPGRAPH_COUNTERS_LOG)
def Create(
    target: "build_target_lib.BuildTarget",
    run_configs: SetupBoardRunConfig,
    accept_licenses: Optional[str],
) -> sysroot_lib.Sysroot:
    """Create a sysroot.

    This entry point is the subset of the full setup process that does the
    creation and configuration of a sysroot, including installing portage.

    Args:
        target: The build target being installed in the sysroot being created.
        run_configs: The run configs.
        accept_licenses: The additional licenses to accept.
    """
    cros_build_lib.AssertInsideChroot()

    sysroot = sysroot_lib.Sysroot(target.root)

    if sysroot.Exists() and not run_configs.force and not run_configs.quiet:
        logging.warning(
            "Board output directory already exists: %s\n"
            "Use --force to clobber the board root and start again.",
            sysroot.path,
        )

    # Override regen_configs setting to force full setup run if the sysroot does
    # not exist.
    run_configs.regen_configs = run_configs.regen_configs and sysroot.Exists()

    # Make sure the chroot is fully up to date before we start unless the
    # chroot update is explicitly disabled, or we're only regenerating the
    # configs.
    if run_configs.update_chroot and not run_configs.regen_configs:
        with tracer.start_as_current_span(
            "service.sysroot.Create.update_chroot"
        ) as span:
            result = sdk_service.Update(
                run_configs.GetUpdateChrootArgs(target.name)
            )

            portage_util.write_depgraph_counters_to_span(span)

            if not result.success:
                raise UpdateChrootError(
                    "Error occurred while updating the chroot. "
                    "See the logs for more information.",
                    failed_packages=result.failed_pkgs,
                )

    # Delete old sysroot to force a fresh start if requested.
    if sysroot.Exists() and run_configs.force:
        sysroot.Delete(background=True)

    # Step 1: Create folders.
    # Dependencies: None.
    # Create the skeleton.
    logging.info("Creating sysroot directories.")
    _CreateSysrootSkeleton(sysroot)

    # Step 2: Standalone configurations.
    # Dependencies: Folders exist.
    # Install main, board setup, and user make.conf files.
    logging.info("Installing configurations into sysroot.")
    _InstallConfigs(sysroot, target)

    # Step 3: Portage configurations.
    # Dependencies: make.conf.board_setup.
    # Create the command wrappers, choose profile, and make.conf.board.
    # Refresh the workon symlinks to compensate for crbug.com/679831.
    logging.info("Setting up portage in the sysroot.")
    _InstallPortageConfigs(
        sysroot,
        target,
        accept_licenses,
        run_configs.local_build,
        use_cq_prebuilts=run_configs.use_cq_prebuilts,
        expanded_binhost_inheritance=run_configs.expanded_binhost_inheritance,
        binhost_lookup_service_data=run_configs.binhost_lookup_service_data,
    )

    # Developer Experience Step: Set default board (if requested) to allow
    # running later commands without needing to pass the --board argument.
    if run_configs.set_default:
        cros_build_lib.SetDefaultBoard(target.name)

    # Initialize the per-board BROOT.
    logging.info("Initializing broot.")
    build_target = build_target_lib.BuildTarget("amd64-host")
    build_sysroot = sysroot_lib.Sysroot(target.broot)
    _CreateSysrootSkeleton(build_sysroot)
    _InstallConfigs(build_sysroot, build_target)

    return sysroot


def GenerateArchive(
    output_dir: str, build_target_name: str, pkg_list: List[str]
) -> str:
    """Generate a sysroot tarball for informational builders.

    Args:
        output_dir: Directory to contain the created the sysroot.
        build_target_name: The build target for the sysroot being created.
        pkg_list: List of 'category/package' package strings.

    Returns:
        Path to the sysroot tar file.
    """
    cmd = [
        "cros_generate_sysroot",
        "--out-file",
        constants.TARGET_SYSROOT_TAR,
        "--out-dir",
        output_dir,
        "--board",
        build_target_name,
        "--package",
        " ".join(pkg_list),
    ]
    cros_build_lib.run(cmd, cwd=constants.SOURCE_ROOT)
    return os.path.join(output_dir, constants.TARGET_SYSROOT_TAR)


def _create_sysroot(
    chroot: "chroot_lib.Chroot",
    _sysroot_class,
    build_target: "build_target_lib.BuildTarget",
    output_dir: str,
    package_list: List[str],
    output_file: str,
    deps_only: bool = True,
) -> str:
    """Create a sysroot to use.

    Args:
        chroot: The chroot class used for these artifacts.
        sysroot_class: The sysroot class used for these artifacts.
        build_target: The build target used for these artifacts.
        output_dir: The path to write artifacts to.
        package_list: List of packages to use.
        output_file: Name of the archive to output.
        deps_only: Whether to pass --deps-only.

    Returns:
        Path to the sysroot tar file.
    """
    with chroot.tempdir() as tempdir:
        outdir = chroot.chroot_path(tempdir)
        cmd = [
            "cros_generate_sysroot",
            "--out-dir",
            outdir,
            "--board",
            build_target.name,
            "--package",
            " ".join(package_list),
            "--out-file",
            output_file,
        ]
        if deps_only:
            cmd.append("--deps-only")
        chroot.run(cmd, cwd=constants.SOURCE_ROOT)

        # Move the artifact out of the chroot.
        sysroot_tar_path = os.path.join(tempdir, output_file)
        shutil.copy(sysroot_tar_path, output_dir)
        return os.path.join(output_dir, output_file)


def CreateSimpleChromeSysroot(
    chroot: "chroot_lib.Chroot",
    _sysroot_class,
    build_target: "build_target_lib.BuildTarget",
    output_dir: str,
) -> str:
    """Create a sysroot for SimpleChrome to use.

    Args:
        chroot: The chroot class used for these artifacts.
        sysroot_class: The sysroot class used for these artifacts.
        build_target: The build target used for these artifacts.
        output_dir: The path to write artifacts to.

    Returns:
        Path to the sysroot tar file.
    """
    return _create_sysroot(
        chroot,
        _sysroot_class,
        build_target,
        output_dir,
        [constants.CHROME_CP],
        output_file=constants.CHROME_SYSROOT_TAR,
    )


def CreateFuzzerSysroot(
    chroot: "chroot_lib.Chroot",
    _sysroot_class,
    build_target: "build_target_lib.BuildTarget",
    output_dir: str,
) -> str:
    """Create a sysroot for fuzzer builders.

    Args:
        chroot: The chroot class used for these artifacts.
        sysroot_class: The sysroot class used for these artifacts.
        build_target: The build target used for these artifacts.
        output_dir: The path to write artifacts to.

    Returns:
        Path to the sysroot tar file.
    """
    return _create_sysroot(
        chroot,
        _sysroot_class,
        build_target,
        output_dir,
        ["virtual/target-fuzzers"],
        output_file="sysroot_virtual_target-os.tar.xz",
        deps_only=False,
    )


def CreateChromeEbuildEnv(
    chroot: "chroot_lib.Chroot",
    sysroot_class: sysroot_lib.Sysroot,
    _build_target,
    output_dir: str,
) -> Optional[str]:
    """Generate Chrome ebuild environment.

    Args:
        chroot: The chroot class used for these artifacts.
        sysroot_class: The sysroot where the original environment archive can be
        found.
        output_dir: Where the result should be stored.

    Returns:
        The path to the archive, or None.
    """
    pkg_dir = chroot.full_path(sysroot_class.path, portage_util.VDB_PATH)
    files = glob.glob(os.path.join(pkg_dir, constants.CHROME_CP) + "-*")
    if not files:
        logging.warning("No package found for %s", constants.CHROME_CP)
        return None

    if len(files) > 1:
        logging.warning(
            "Expected one package for %s, found %d",
            constants.CHROME_CP,
            len(files),
        )

    chrome_dir = sorted(files)[-1]
    env_bzip = os.path.join(chrome_dir, "environment.bz2")
    result_path = os.path.join(output_dir, constants.CHROME_ENV_TAR)
    with osutils.TempDir() as tempdir:
        # Convert from bzip2 to tar format.
        bzip2 = compression_lib.find_compressor(
            compression_lib.CompressionType.BZIP2
        )
        tempdir_tar_path = os.path.join(tempdir, constants.CHROME_ENV_FILE)
        cros_build_lib.run(
            [bzip2, "-d", env_bzip, "-c"], stdout=tempdir_tar_path
        )

        compression_lib.create_tarball(result_path, tempdir)

    return result_path


@tracer.start_as_current_span("service.sysroot.InstallToolchain")
@osutils.rotate_log_file(constants.PORTAGE_DEPGRAPH_COUNTERS_LOG)
def InstallToolchain(
    target: "build_target_lib.BuildTarget",
    sysroot: sysroot_lib.Sysroot,
    run_configs: SetupBoardRunConfig,
) -> None:
    """Update the toolchain to a sysroot.

    This entry point just installs the target's toolchain into the sysroot.
    Everything else must have been done already for this to be successful.

    Args:
        target: The target whose toolchain is being installed.
        sysroot: The sysroot where the toolchain is being installed.
        run_configs: The run configs.
    """
    cros_build_lib.AssertInsideChroot()
    if not sysroot.Exists():
        # Sanity check before we try installing anything.
        raise ValueError("The sysroot must exist, run Create first.")

    # Step 4: Install toolchain and packages.
    # Dependencies: Portage configs and wrappers have been installed.
    if run_configs.init_board_pkgs:
        logging.info("Updating toolchain.")
        # Use the local packages if we're doing a local only build or usepkg is
        # set.
        local_init = run_configs.usepkg or run_configs.local_build
        _InstallToolchain(sysroot, target, local_init=local_init)

    portage_util.write_depgraph_counters_to_span(trace.get_current_span())


@tracer.start_as_current_span("service.sysroot.BuildPackages")
@metrics_lib.timed("service.sysroot.BuildPackages")
@osutils.rotate_log_file(constants.PORTAGE_DEPGRAPH_COUNTERS_LOG)
@osutils.rotate_log_file(portage_util.get_die_hook_status_file())
def BuildPackages(
    target: "build_target_lib.BuildTarget",
    sysroot: sysroot_lib.Sysroot,
    run_configs: BuildPackagesRunConfig,
) -> None:
    """Build and install packages into a sysroot.

    Args:
        target: The target whose packages are being installed.
        sysroot: The sysroot where the packages are being installed.
        run_configs: The run configs.

    Raises:
        sysroot_lib.PackageInstallError when packages fail to install.
    """
    cros_build_lib.AssertInsideChroot()
    cros_build_lib.AssertNonRootUser()
    metrics_prefix = "service.sysroot.BuildPackages"

    logging.info("Bootstraping depot_tools")
    cros_build_lib.run([constants.DEPOT_TOOLS_DIR / "ensure_bootstrap"])

    if os.environ.get("CROS_CLEAN_OUTDATED_PKGS") != "0":
        cop_command = [
            "cros",
            "clean-outdated-pkgs",
            f"--board={target.name}",
        ]
        try:
            cros_build_lib.sudo_run(
                cop_command,
                preserve_env=True,
            )
        except Exception as e:
            cmd_as_str = " ".join(cop_command)
            logging.error(
                'While cleaning outdated packages with "%s": %s', cmd_as_str, e
            )
            raise e

    extra_env = run_configs.GetExtraEnv()
    extra_env["PKGDIR"] = f"{sysroot.path}/packages"

    # Get the pre-existing list of binhosts specified by make.conf.board.
    portage_binhost = portage_util.PortageqEnvvar(
        "PORTAGE_BINHOST", target.name
    )
    make_conf_binhosts = portage_binhost.strip().split()
    # Split out the binhosts.
    chrome_binhosts = [x for x in make_conf_binhosts if "cq-" in x]
    target_binhosts = [x for x in make_conf_binhosts if "cq-" not in x]

    # Use the binhost lookup service.
    fetched_binhosts = None
    try:
        fetched_binhosts = binhost_service.lookup_binhosts(
            build_target=target,
            binhost_lookup_service_data=run_configs.binhost_lookup_service_data,
        )
        logging.info(
            "Binhosts fetched from the lookup service: %s", fetched_binhosts
        )
    # Do not block on any exceptions thrown from the lookup service.
    except Exception as e:
        logging.info("Lookup service error: %s", e)

    # If the lookup service returned binhosts, use them + the chrome binhosts.
    if fetched_binhosts:
        binhosts = fetched_binhosts + chrome_binhosts
    # The lookup service did not return binhosts, use the fallback mechanism.
    else:
        binhosts = target_binhosts + chrome_binhosts

    extra_env["PORTAGE_BINHOST"] = " ".join(binhosts)

    if logging.getLogger().isEnabledFor(logging.DEBUG):
        # Logging binhost ages requires multiple remote requests, so only do it
        # with logging level >= debug.
        _LogBinhostAge(binhosts, date_threshold=30)

    with cpupower_helper.ModifyCpuGovernor(
        run_configs.autosetgov, run_configs.autosetgov_sticky
    ):
        cros_build_lib.ClearShadowLocks(sysroot.path)

        # Before running any emerge operations, regenerate the Portage
        # dependency cache in parallel.
        logging.info("Rebuilding Portage cache.")
        with metrics_lib.timer(f"{metrics_prefix}.RegenPortageCache"):
            portage_util.RegenDependencyCache(
                sysroot=sysroot.path, jobs=run_configs.jobs
            )

        # Install per-board bdepends packages.
        logging.info("Updating per-board bdepends")

        # These packages are allowed to live in the broot & SDK as a
        # transitional measure.  We'll eventually drop this.
        TEMP_DUPLICATE_PACKAGES = {
            "chromeos-base/tast-cmd",
            "chromeos-base/tast-remote-tests",
            "chromeos-base/tast-remote-tests-cros",
            "chromeos-base/tast-remote-tests-crosint",
            "chromeos-base/tast-remote-tests-crosint_intel",
            "chromeos-base/tast-tests-remote-data",
            "dev-libs/flatbuffers",
            "dev-util/test-services",
            "dev-util/cros-dut",
            "dev-util/cros-provision",
            "dev-util/cros-publish",
            "dev-util/cros-servod",
            "dev-util/cros-test",
            "dev-util/cros-test-finder",
            "dev-util/fw-provision",
            "dev-util/cros-hpt",
            "dev-util/pre-process",
            "dev-util/post-process",
            "dev-util/testlabenv-local",
            "dev-util/cros-ctp2-filters",
            "dev-util/vm-provision",
            "dev-util/cros-fw-provision",
            "dev-util/android-provision",
            "virtual/tast-remote-tests",
        }
        sdk_vdb = portage_util.PortageDB()
        provided = (
            target.broot / "etc" / "portage" / "profile" / "package.provided"
        )
        pkgdir = target.broot / "packages"
        osutils.SafeMakedirs(provided.parent, sudo=True)
        osutils.WriteFile(
            provided,
            "".join(
                sorted(
                    f"{x.package_info.cpvr}\n"
                    for x in sdk_vdb.InstalledPackages()
                    if x.package_info.cp not in TEMP_DUPLICATE_PACKAGES
                )
            ),
            sudo=True,
        )

        cmd = [
            constants.CHROMITE_BIN_DIR / "parallel_emerge",
            "--root",
            target.broot,
            "--sysroot",
            target.broot,
            "--with-bdepends=n",
            "--update",
            "--deep",
            "--newuse",
            "--verbose",
            "--newrepo",
        ]
        if run_configs.usepkg:
            cmd += ["--usepkg", "--getbinpkg"]
        cmd += [constants.TARGET_SDK_BROOT]
        with metrics_lib.timer(f"{metrics_prefix}.Broot"):
            try:
                cros_build_lib.sudo_run(
                    cmd, extra_env={"PKGDIR": str(pkgdir), "USE": ""}
                )
            except cros_build_lib.RunCommandError as e:
                failed_pkgs = portage_util.ParseDieHookStatusFile()
                raise sysroot_lib.PackageInstallError(
                    "Merging broot packages failed",
                    e.result,
                    exception=e,
                    packages=failed_pkgs,
                ) from e

        # Clean out any stale binpkgs we've accumulated. This is done
        # immediately after regenerating the cache in case ebuilds have been
        # removed (e.g. from a revert).
        if run_configs.eclean:
            binpkg.CleanStaleBinpkgs(sysroot.path)

        emerge_cmd = _GetEmergeCommand(sysroot.path)
        emerge_flags = run_configs.GetEmergeFlags()
        rebuild_pkgs = " ".join(run_configs.GetForceLocalBuildPackages(sysroot))
        if rebuild_pkgs:
            emerge_flags.extend(
                [
                    f"--reinstall-atoms={rebuild_pkgs}",
                    f"--usepkg-exclude={rebuild_pkgs}",
                ]
            )

        sdk_pkgs = " ".join(_CRITICAL_SDK_PACKAGES)
        emerge_flags.extend(
            [
                f"--useoldpkg-atoms={sdk_pkgs}",
                f"--rebuild-exclude={sdk_pkgs}",
            ]
        )

        logging.info("Merging board packages now.")
        try:
            with metrics_lib.timer(f"{metrics_prefix}.emerge"):
                packages = run_configs.GetPackages()

                span = trace.get_current_span()
                span.set_attributes(
                    {
                        "board": target.name,
                        "packages": packages,
                        "bazel": run_configs.bazel,
                    }
                )

                timeout = (
                    (
                        run_configs.timeout - datetime.datetime.utcnow()
                    ).total_seconds()
                    if run_configs.timeout
                    else None
                )
                logging.info(
                    "Timeout datetime is %s. "
                    "The build comand will be aborted after %s seconds.",
                    run_configs.timeout,
                    str(timeout),
                )

                if run_configs.bazel:
                    _BazelBuild(
                        packages,
                        target.name,
                        run_configs.bazel_lite,
                        run_configs.bazel_use_remote_execution,
                        extra_env,
                        timeout,
                        _PrintProcessTree,
                    )
                else:
                    cros_build_lib.sudo_run(
                        emerge_cmd + emerge_flags + packages,
                        preserve_env=True,
                        extra_env=extra_env,
                        cmd_timeout=timeout,
                        pre_timeout_hook=_PrintProcessTree,
                    )
            logging.info("Builds complete.")
        except cros_build_lib.RunCommandError as e:
            failed_pkgs = portage_util.ParseDieHookStatusFile()
            raise sysroot_lib.PackageInstallError(
                "Merging board packages failed",
                e.result,
                exception=e,
                packages=failed_pkgs,
            ) from e

        # Remove any broken or outdated binpkgs.
        if run_configs.eclean:
            portage_util.CleanOutdatedBinaryPackages(sysroot.path, deep=True)

    portage_util.write_depgraph_counters_to_span(trace.get_current_span())


def _LogBinhostAge(binhosts: List[str], date_threshold: int) -> None:
    """Log the age of the binhosts and suggest remediation steps if necessary.

    Args:
        binhosts: The list of binhost gs urls.
        date_threshold: The maximum number of days considered as acceptable
            before logging a warning.
    """
    today = datetime.datetime.now()

    for binhost in binhosts:
        # In some cases the binhost url ends with a trailing slash, the rstrip
        # handles those urls.
        package_index = binhost.rstrip("/") + "/Packages"

        try:
            binhost_age = gs.GSContext().GetCreationTimeSince(
                path=package_index, since_date=today
            )
        # Using the catch-all gs.GSContextException to record and suppress gs
        # errors since this is a function for logging and should not halt
        # program execution.
        except gs.GSContextException as e:
            logging.info("PORTAGE_BINHOST %s", binhost)
            logging.warning("Error getting the binhost age: %s", e)
            return

        logging.info(
            "PORTAGE_BINHOST %s was created %d days ago.",
            binhost,
            binhost_age.days,
        )

        if binhost_age.days >= date_threshold:
            logging.warning(
                "PORTAGE_BINHOST %s was created more than 30 days ago. "
                "Please repo sync for the latest build artifacts.",
                binhost,
            )


def _GetCrosWorkonPackages(sysroot: Union[str, os.PathLike]) -> _PACKAGE_LIST:
    """Get cros_workon packages.

    Args:
        sysroot: The sysroot to get cros_workon packages for.

    Raises:
        cros_build_lib.RunCommandError
    """
    # TODO(xcl): Migrate this to calling an imported Python lib
    cmd = ["cros_list_modified_packages", "--sysroot", sysroot]
    result = cros_build_lib.run(
        cmd, print_cmd=False, capture_output=True, encoding="utf-8"
    )
    logging.info(
        "Detected cros_workon modified packages: %s", result.stdout.rstrip()
    )
    packages = result.stdout.split()

    if os.environ.get("CHROME_ORIGIN"):
        packages.extend(_CHROME_PACKAGES)

    return packages


def _GetBaseInstallPackages(
    sysroot: Union[str, os.PathLike],
    emerge_flags: List[str],
    packages: List[str],
) -> List[Optional[str]]:
    """Get packages to determine reverse dependencies for.

    Args:
        sysroot: The sysroot to get packages for.
        emerge_flags: Emerge flags to run the command with.
        packages: The packages to get dependencies for.

    Raises:
        cros_build_lib.RunCommandError
    """
    # Do a pretend `emerge` command to get a list of what would be built.
    # Sample output:
    # [binary N] dev-go/containerd ... to /build/eve/ USE="..."
    # [ebuild r U] chromeos-base/tast-build-deps ... to /build/eve/ USE="..."
    # [binary U] chromeos-base/chromeos-chrome ... to /build/eve/ USE="..."
    cmd = _GetEmergeCommand(sysroot)
    result = cros_build_lib.sudo_run(
        cmd + emerge_flags + packages, capture_output=True, encoding="utf-8"
    )

    # Filter to a heuristic set of packages known to have incorrectly specified
    # dependencies that will be installed to the board sysroot.
    # Sample output is filtered to:
    # [ebuild r U] chromeos-base/tast-build-deps ... to /build/eve/ USE="..."
    include_patterns = ["coreboot-private-files", "tast-build-deps"]

    # Pattern used to rewrite the line from Portage's full output to only
    # $CATEGORY/$PACKAGE.
    pattern = re.compile(r"\[ebuild(.*?)\]\s(.*?)\s")

    # Filter and sort the output and remove any duplicate entries.
    packages = set()
    for line in result.stdout.splitlines():
        if "to /build/" in line and any(x in line for x in include_patterns):
            # Use regex to get substrings that matches a
            # '[ebuild ...] <some characters> ' pattern. The second matching
            # group returns the $CATEGORY/$PACKAGE from a line of the emerge
            # output.
            m = pattern.search(line)
            if m:
                packages.add(m.group(2))
    return sorted(packages)


def _GetEmergeCommand(
    sysroot: Optional[Union[str, os.PathLike]] = None
) -> List[Union[str, os.PathLike]]:
    """Get the emerge command to use with `cros build-packages`."""
    # TODO(xcl): Convert to directly importing and calling a Python lib instead
    # of calling a binary.
    cmd = [constants.CHROMITE_BIN_DIR / "parallel_emerge"]
    if sysroot:
        cmd.extend(
            [
                f"--sysroot={sysroot}",
                f"--root={sysroot}",
            ]
        )
    return cmd


def _GetFailedPackages(
    bazel_build_event_json_file: str, board: str
) -> List[str]:
    """Reads the specified file and returns a list of failed packages.

    Each line of the input file is a JSON object which represents an event, and
    each event looks like this:
    {
      "id": {
        "actionCompleted": {
          "primaryOutput": ".../chrome-icu/chrome-icu-122.0.6226.0_rc-r1.tbz2",
          "label": "@@.../chromeos-base/chrome-icu:122.0.6226.0_rc-r1",
          "configuration": {
            "id": "..."
          }
        }
      },
      "action": {
        "exitCode": 1,
        "stderr": {
          "name": "stderr",
          "uri": "bytestream://remotebuildexecution.googleapis.com/..."
        },
        "label": "@@.../chromeos-base/chrome-icu:122.0.6226.0_rc-r1",
        "configuration": {
          "id": "..."
        },
        "type": "Ebuild",
        "commandLine": [
          ...
        ],
        "failureDetail": {
          "message": "local spawn failed for Ebuild",
          "spawn": {
            "code": "NON_ZERO_EXIT",
            "spawnExitCode": 1
          }
        }
      }
    }
    """
    failed_packages = set()
    with open(bazel_build_event_json_file, encoding="utf-8") as f:
        for line in f:
            # Look for actionCompleted events with failureDetails.
            event = json.loads(line)
            action_completed = event.get("id", {}).get("actionCompleted")
            failure_detail = event.get("action", {}).get("failureDetail")
            if action_completed and failure_detail:
                label = action_completed.get("label", "")
                m = re.match(
                    "@@_main~portage~portage//.*/([^/]+)/([^:]+):(.*)", label
                )
                if m:
                    category = m.group(1)
                    pn = m.group(2)
                    pvr = m.group(3)
                    pf = "%s-%s" % (pn, pvr)
                    failed_packages.add("%s/%s" % (category, pf))

                    # Copy the package log file to the same path as portage.
                    primary_output = action_completed.get("primaryOutput")
                    if primary_output:
                        primary_output_path = (
                            Path(constants.BAZEL_WORKSPACE_ROOT)
                            / primary_output
                        )
                        log_path = primary_output_path.parent / ("%s.log" % pf)
                        if log_path.exists():
                            timestamp = datetime.datetime.now().strftime(
                                "%Y%m%d-%H%M%S"
                            )
                            dest_path = Path(
                                "/build/%s/tmp/portage/logs/%s:%s:%s.log"
                                % (board, category, pf, timestamp)
                            )
                            # Open `dest_path` with "a" to handle cases where
                            # it already exists (e.g. when the same package
                            # fails in multiple stages).
                            with open(
                                dest_path, "a", encoding="utf-8"
                            ) as f_dest:
                                f_dest.write(
                                    "(Copied from %s to %s)\n"
                                    % (log_path, dest_path)
                                )
                                with open(
                                    log_path, "r", encoding="utf-8"
                                ) as f_src:
                                    shutil.copyfileobj(f_src, f_dest)

    return list(failed_packages)


def _PrintProcessTree() -> None:
    """Print the process tree"""
    logging.info(
        "The build process is about to be aborted because of a timeout. "
        "Printing the process tree."
    )
    cros_build_lib.run(["pstree", "-Apal"])


def _BazelBuild(
    packages: List[str],
    target_name: str,
    bazel_lite: bool,
    bazel_use_remote_execution: bool,
    extra_env: Dict[str, str],
    timeout: int,
    pre_timeout_hook: Callable,
) -> None:
    """Build packages with Bazel.

    Args:
        packages: Packages to build, for example `[virtual/target-os, ...]`.
            They are ignored if `bazel_lite == True`.
        target_name: Target board, for example, `amd64-generic`.
        bazel_lite: Whether to perform lite build, which targets a reduced
            set of packages and skips sysroot installation.
        bazel_use_remote_execution: Whether Bazel builds should execute
            Bazel actions remotely.
        extra_env: Environment in which commands should be executed.
        timeout: If set, aborts the command after the specified number of
            seconds.
        pre_timeout_hook: A callable object which will be run before the
            timeout.
    """

    # Bazel needs amd64-host sysroot with sdk/bootstrap profile.
    cros_build_lib.run(
        [
            constants.CHROMITE_SHELL_DIR / "create_sdk_board_root",
            "--board",
            "amd64-host",
            "--profile",
            "sdk/bootstrap",
        ]
    )

    extra_env = {**extra_env, "BOARD": target_name}

    if bazel_lite:
        # We want to build all dependencies of virtual/target-os, -dev, and
        # -test except chromeos-chrome and packages that depend on it.
        # `cquery` handles `select`, instead of returning both branches.
        # Therefore it does not return stage1 targets which we
        # should not build.
        # b/315142814: target-os-dev is dropped temporarily.
        top_level_packages_to_build = [
            "virtual/target-os",
            "virtual/target-os-test",
            "virtual/target-os-dev",
            "virtual/target-os-factory",
            "virtual/target-os-factory-shim",
        ]
        packages_to_exclude = [
            "chromeos-base/chromeos-chrome",
        ]
        top_level_packages_query = "union".join(
            [
                f"""
    kind("ebuild",
        deps(@portage//target/{package})
    )
    """
                for package in top_level_packages_to_build
            ]
        )
        exclusion_query = "union".join(
            [
                f"""
        filter(
            "//internal/packages/stage2/target/board/chromiumos/{package}:",
            kind("ebuild", deps(@portage//target/{package}))
        )
        """
                for package in packages_to_exclude
            ]
        )
        query_text = f"""
let targets = {top_level_packages_query}
in
    $targets except rdeps(
        $targets,{exclusion_query}
    )
        """

        query_result = cros_build_lib.run(
            [
                BAZEL_COMMAND,
                "cquery",
                "--profile=" + BAZEL_ALLPACKAGES_CQUERY_PROFILE_FILE,
                query_text,
            ],
            extra_env=extra_env,
            stdout=True,
            encoding="utf-8",
        )

        # The results look like this
        # @portage//internal/(...)/chromeos-base/crosid:0.0.1-r209 (7729267)
        # and we need to remove the id at the end.
        targets = re.findall("(.*) \\(", query_result.stdout)
    else:
        targets = [
            "@portage//target/%s:installed" % package for package in packages
        ]

    build_success = False
    try:
        cmd = [
            BAZEL_COMMAND,
            "build",
            "--profile=" + BAZEL_ALLPACKAGES_COMMAND_PROFILE_FILE,
            "--noslim_profile",
            "--experimental_profile_include_target_label",
            "--experimental_profile_include_primary_output",
            # --keep_going to keep building packages even after a failure to
            # detect as many failure as possible on the CI builders.
            # We may need to delete this after launching Alchemy.
            "--keep_going=%s" % ("false" if bazel_lite else "true"),
            "--experimental_execution_log_compact_file="
            + BAZEL_ALLPACKAGES_EXEC_LOG_FILE,
            "--config=hash_tracer",
            "--config=collect_logs",
            "--config=collect_ebuild_metadata",
            "--build_event_json_file=%s" % BAZEL_BUILD_EVENT_JSON_FILE_PATH,
            # TODO(b/340476082): Switch back to uploading to BEP for Latency
            # Processor once Bazel's incomplete execlog data issue is fixed and
            # we stop needing the graph log for our analysis pipeline.
            "--experimental_enable_execution_graph_log",
            "--experimental_execution_graph_log_dep_type=all",
            "--experimental_execution_graph_log_path=%s"
            % BAZEL_ALLPACKAGES_GRAPH_LOG_FILE,
        ]
        if bazel_use_remote_execution:
            cmd += ["--config=rbe_exec"]
        cmd += targets
        cros_build_lib.run(
            cmd,
            extra_env=extra_env,
            cmd_timeout=timeout,
            pre_timeout_hook=pre_timeout_hook,
        )
        build_success = True
    except cros_build_lib.RunCommandError:
        failed_packages = _GetFailedPackages(
            BAZEL_BUILD_EVENT_JSON_FILE_PATH, target_name
        )
        if failed_packages:
            # "unknown" is a place holder for the failing ebuild phase name
            # which won't be used.
            osutils.WriteFile(
                portage_util.get_die_hook_status_file(),
                "\n".join(f"{x} unknown" for x in failed_packages),
                encoding="utf-8",
                sudo=True,
            )
            try:
                osutils.Chown(
                    portage_util.get_die_hook_status_file(), user=True
                )
            except (osutils.UnknownNonRootUserError, OSError):
                pass
        raise
    finally:
        # Postprocess the output, regardless of the build result.
        try:
            cros_build_lib.run(
                [
                    BAZEL_COMMAND,
                    "run",
                    "//bazel/portage/tools/process_artifacts",
                    "--",
                    "--build-events-jsonl=%s"
                    % BAZEL_BUILD_EVENT_JSON_FILE_PATH,
                    "--archive-logs=%s" % BAZEL_ALLPACKAGES_ACTION_LOGS_FILE,
                    "--prebuilts=%s" % BAZEL_ALLPACKAGES_PREBUILTS_FILE,
                ],
                extra_env=extra_env,
            )
        except cros_build_lib.RunCommandError:
            # If the build has failed, suppress the current exception to raise
            # the exception for the build. Otherwise, raise the current one.
            if build_success:
                raise


def _CreateSysrootSkeleton(sysroot: sysroot_lib.Sysroot) -> None:
    """Create the sysroot skeleton.

    Dependencies: None.
    Creates the sysroot directory structure and installs the portage hooks.

    Args:
        sysroot: The sysroot.
    """
    sysroot.CreateSkeleton()


def _InstallConfigs(
    sysroot: sysroot_lib.Sysroot, target: "build_target_lib.BuildTarget"
) -> None:
    """Install standalone configuration files into the sysroot.

    Dependencies: The sysroot exists (i.e. CreateSysrootSkeleton).
    Installs the main, board setup, and user make.conf files.

    Args:
        sysroot: The sysroot.
        target: The build target being setup in the sysroot.
    """
    sysroot.InstallMakeConf(target)
    sysroot.InstallMakeConfSdk(target, public_only=False)
    sysroot.InstallMakeConfBoardSetup(target)
    sysroot.InstallMakeConfUser()
    sysroot.write_build_target_config(target)

    if target.is_host():
        make_profile = sysroot.JoinPath("etc", "portage", "make.profile")
        osutils.SafeUnlink(make_profile, sudo=True)
        osutils.SafeSymlink(
            constants.SOURCE_ROOT
            / constants.CHROMIUMOS_OVERLAY_DIR
            / "profiles"
            / "default"
            / "linux"
            / "amd64"
            / "10.0"
            / "sdk",
            make_profile,
            sudo=True,
        )

        # Initialize the configs.
        workon_helper.WorkonHelper(sysroot.path, friendly_name="host")


def _InstallPortageConfigs(
    sysroot: sysroot_lib.Sysroot,
    target: "build_target_lib.BuildTarget",
    accept_licenses: Optional[str],
    local_build: bool,
    use_cq_prebuilts: bool = False,
    expanded_binhost_inheritance: bool = False,
    binhost_lookup_service_data: Optional[
        prebuilts_cloud_pb2.BinhostLookupServiceData
    ] = None,
) -> None:
    """Install portage wrappers and configurations.

    Dependencies: make.conf.board_setup (InstallConfigs).
    Create the command wrappers, choose profile, and generate make.conf.board.
    Refresh the workon symlinks to compensate for crbug.com/679831.

    Args:
        sysroot: The sysroot.
        target: The build target being installed in the sysroot.
        accept_licenses: Additional accepted licenses as a string.
        local_build: If the build is a local only build.
        use_cq_prebuilts: Whether to use the prebuilts generated by CQ.
        expanded_binhost_inheritance: Whether to allow expanded binhost
            inheritance.
        binhost_lookup_service_data: Data needed for fetching binhosts.
    """
    sysroot.CreateAllWrappers(friendly_name=target.name)
    _ChooseProfile(target, sysroot)
    _RefreshWorkonSymlinks(target.name, sysroot)

    fetched_binhosts = None
    try:
        fetched_binhosts = binhost_service.lookup_binhosts(
            target, binhost_lookup_service_data
        )
    # Do not block on any exceptions thrown from the lookup service.
    except Exception as e:
        # TODO(b/324316870): Resolve implicit .repo dependency.
        if path_util.is_citc_checkout():
            logging.warning("Skipping setup_board binhost fetching in Cog.")
        else:
            logging.info("Lookup service error: %s", e)

    # Must be done after the profile is chosen or binhosts may be incomplete.
    sysroot.InstallMakeConfBoard(
        accepted_licenses=accept_licenses,
        local_only=local_build,
        use_cq_prebuilts=use_cq_prebuilts,
        expanded_binhost_inheritance=expanded_binhost_inheritance,
        binhost_overrides=fetched_binhosts,
    )


def _InstallToolchain(
    sysroot: sysroot_lib.Sysroot,
    target: "build_target_lib.BuildTarget",
    local_init: bool = True,
) -> None:
    """Install toolchain and packages.

    Dependencies: Portage configs and wrappers have been installed
        (InstallPortageConfigs).
    Install the toolchain and the implicit dependencies.

    Args:
        sysroot: The sysroot to install to.
        target: The build target whose toolchain is being installed.
        local_init: Whether to use local packages to bootstrap implicit
            dependencies.
    """
    sysroot.UpdateToolchain(target.name, local_init=local_init)


def _RefreshWorkonSymlinks(target: str, sysroot: sysroot_lib.Sysroot) -> None:
    """Force refresh the workon symlinks.

    Create an instance of the WorkonHelper, which will recreate all symlinks
    to masked/unmasked packages currently worked on in case the sysroot was
    recreated (crbug.com/679831).

    This was done with a call to `cros_workon list` in the bash version of
    the script, but all we actually need is for the WorkonHelper to be
    instantiated since it refreshes the symlinks in its __init__.

    Args:
        target: The build target name.
        sysroot: The board's sysroot.
    """
    workon_helper.WorkonHelper(sysroot.path, friendly_name=target)


def _ChooseProfile(
    target: "build_target_lib.BuildTarget", sysroot: sysroot_lib.Sysroot
) -> None:
    """Helper function to execute cros_choose_profile.

    TODO(saklein) Refactor cros_choose_profile to avoid needing the run
    call here, and by extension this method all together.

    Args:
        target: The build target whose profile is being chosen.
        sysroot: The sysroot for which the profile is being chosen.
    """
    choose_profile = [
        constants.CHROMITE_BIN_DIR / "cros_choose_profile",
        "--board",
        target.name,
        "--board-root",
        sysroot.path,
    ]
    if target.profile:
        # Chooses base by default, only override when we have a passed param.
        choose_profile += ["--profile", target.profile]
    try:
        cros_build_lib.run(choose_profile, print_cmd=False)
    except cros_build_lib.RunCommandError as e:
        logging.error(
            "Selecting profile failed, removing incomplete board " "directory!"
        )
        sysroot.Delete()
        raise e


@metrics_lib.timed("service.sysroot.BundleDebugSymbols")
def BundleDebugSymbols(
    chroot: "chroot_lib.Chroot",
    sysroot_class: sysroot_lib.Sysroot,
    _build_target: "build_target_lib.BuildTarget",
    output_dir: str,
) -> Optional[str]:
    """Bundle debug symbols into a tarball for importing into GCE.

    Bundle the debug symbols found in the sysroot into a .tgz. This assumes
    these files are present.

    Args:
        chroot: The chroot class used for these artifacts.
        sysroot_class: The sysroot class used for these artifacts.
        build_target: The build target used for these artifacts.
        output_dir: The path to write artifacts to.

    Returns:
        A string path to the output debug.tgz artifact, or None.
    """
    base_path = chroot.full_path(sysroot_class.path)
    debug_dir = os.path.join(base_path, "usr/lib/debug")

    if not os.path.isdir(debug_dir):
        logging.error("No debug directory found at %s.", debug_dir)
        return None

    # Create tarball from destination_tmp, then copy it...
    tarball_path = os.path.join(output_dir, constants.DEBUG_SYMBOLS_TAR)
    exclude_breakpad_tar_arg = "--exclude=%s" % os.path.join(
        debug_dir, "breakpad"
    )
    exclude_vmlinux_tar_arg = "--exclude=%s" % os.path.join(
        debug_dir, "boot/vmlinux.debug"
    )
    result = None
    try:
        result = compression_lib.create_tarball(
            tarball_path,
            debug_dir,
            compression=compression_lib.CompressionType.GZIP,
            sudo=True,
            extra_args=[exclude_breakpad_tar_arg, exclude_vmlinux_tar_arg],
        )
    except compression_lib.TarballError:
        pass
    if not result or result.returncode:
        # We don't abort here, because the tar may still be somewhat intact.
        err = result.returncode if result else "TarballError"
        logging.error(
            "Error (%s) when creating tarball %s from %s",
            err,
            tarball_path,
            debug_dir,
        )
    if os.path.exists(tarball_path):
        return tarball_path
    else:
        return None


@metrics_lib.timed("service.sysroot.BundleBreakpadSymbols")
def BundleBreakpadSymbols(
    chroot: "chroot_lib.Chroot",
    sysroot_class: sysroot_lib.Sysroot,
    build_target: "build_target_lib.BuildTarget",
    output_dir: str,
    ignore_generation_errors: bool,
    ignore_generation_expected_files: List[str],
) -> Optional[str]:
    """Bundle breakpad debug symbols into a tarball for importing into GCE.

    Call the GenerateBreakpadSymbols function and archive this into a tar.gz.

    Args:
        chroot: The chroot class used for these artifacts.
        sysroot_class: The sysroot class used for these artifacts.
        build_target: The build target used for these artifacts.
        output_dir: The path to write artifacts to.
        ignore_generation_errors: If True, ignore errors during symbol
            generation.
        ignore_generation_expected_files: A list of files (like "ASH_CHROME" or
            "LIBC") that symbol generation normally expects to generate symbols
            for; the generate symbols program will not generate errors if it
            doesn't generate symbols for a file in the list. See
            cros_generate_breakpad_symbols.py's ExpectedFiles enum for the list
            of valid values.

    Returns:
        A string path to the output debug_breakpad.tar.gz artifact, or None.
    """
    base_path = chroot.full_path(sysroot_class.path)

    result = GenerateBreakpadSymbols(
        chroot,
        build_target,
        debug=True,
        ignore_errors=ignore_generation_errors,
        ignore_expected_files=ignore_generation_expected_files,
    )

    # Verify breakpad symbol generation before gathering the sym files.
    if result.returncode:
        logging.error(
            "Error (%d) when generating breakpad symbols", result.returncode
        )
        return None
    with chroot.tempdir() as symbol_tmpdir, chroot.tempdir() as dest_tmpdir:
        breakpad_dir = os.path.join(base_path, "usr/lib/debug/breakpad")
        # Call list on the atifacts.GatherSymbolFiles generator function to
        # materialize and consume all entries so that all are copied to
        # dest dir and complete list of all symbol files is returned.
        sym_file_list = list(
            GatherSymbolFiles(
                tempdir=symbol_tmpdir, destdir=dest_tmpdir, paths=[breakpad_dir]
            )
        )

        if not sym_file_list:
            logging.warning("No sym files found in %s.", breakpad_dir)
        # Create tarball from destination_tmp, then copy it...
        tarball_path = os.path.join(
            output_dir, constants.BREAKPAD_DEBUG_SYMBOLS_TAR
        )
        result = compression_lib.create_tarball(tarball_path, dest_tmpdir)
        if result.returncode != 0:
            logging.error(
                "Error (%d) when creating tarball %s from %s",
                result.returncode,
                tarball_path,
                dest_tmpdir,
            )
            return None
    return tarball_path


def CollectBazelPerformanceArtifacts(
    chroot: "chroot_lib.Chroot",
    _sysroot_class: sysroot_lib.Sysroot,
    _build_target: "build_target_lib.BuildTarget",
    output_dir: str,
) -> List[Path]:
    """Copy Bazel performance artifacts into output_dir for importing into GCS.

    Copy the known set of Bazel performance artifacts into output_dir, so they
    can be uploaded to GCS.

    Args:
        chroot: The chroot class used for these artifacts.
        output_dir: The path to write artifacts to.

    Returns:
        A List of string paths to the output Bazel performance artifacts.
    """
    chroot_raw_artifacts = [
        BAZEL_ALLPACKAGES_COMMAND_PROFILE_FILE,
        BAZEL_ALLPACKAGES_CQUERY_PROFILE_FILE,
        BAZEL_ALLPACKAGES_ACTION_LOGS_FILE,
        BAZEL_ALLPACKAGES_EXEC_LOG_FILE,
        BAZEL_ALLPACKAGES_PREBUILTS_FILE,
        BAZEL_ALLPACKAGES_GRAPH_LOG_FILE,
        BAZEL_BUILD_EVENT_JSON_FILE_PATH,
    ]
    raw_artifacts = [
        chroot.full_path(artifact) for artifact in chroot_raw_artifacts
    ]

    osutils.SafeMakedirs(output_dir)
    existing_artifacts = [Path(r) for r in raw_artifacts if Path(r).exists()]
    archive_paths = [
        shutil.copy2(existing_artifact, Path(output_dir))
        for existing_artifact in existing_artifacts
    ]
    return archive_paths


# A SymbolFileTuple is a data object that contains:
#  relative_path (str): Relative path to the file based on initial search path.
#  source_file_name (str): Full path to where the SymbolFile was found.
# For example, if the search path for symbol files is '/some/bot/path/'
# and a symbol file is found at '/some/bot/path/a/b/c/file1.sym',
# then the relative_path would be 'a/b/c/file1.sym' and the source_file_name
# would be '/some/bot/path/a/b/c/file1.sym'.
# The source_file_name is informational for two reasons:
# 1) They are typically copied off a machine (such as a build bot) where
#    that path will disappear, which is why when we find them they get
#    copied to a destination directory.
# 2) For tar files, the source_file_name is not a full path that can be
#    opened, since it is the path the tar file plus the relative path of
#    the file when we untar it.
class SymbolFileTuple(NamedTuple):
    """Contain a relative and full path to a SymbolFile."""

    relative_path: str
    source_file_name: str


@metrics_lib.timed("service.sysroot.GenerateBreakpadSymbols")
def GenerateBreakpadSymbols(
    chroot: "chroot_lib.Chroot",
    build_target: "build_target_lib.BuildTarget",
    debug: bool,
    ignore_errors: bool,
    ignore_expected_files: List[str],
) -> cros_build_lib.CompletedProcess:
    """Generate breakpad (go/breakpad) symbols for debugging.

    This function generates .sym files to /build/<board>/usr/lib/debug/breakpad
    from .debug files found in /build/<board>/usr/lib/debug by calling
    cros_generate_breakpad_symbols.

    Args:
        chroot: The chroot in which the sysroot should be built.
        build_target: The sysroot's build target.
        debug: Include extra debugging output.
        ignore_errors: If True, ignore errors and generate symbols best effort.
        ignore_expected_files: A list of files (like "ASH_CHROME" or "LIBC")
            that we tell cros_generate_breakpad_symbols it should not expect to
            generate symbols for. See cros_generate_breakpad_symbols.py's
            ExpectedFiles enum for the list of valid values.
    """
    # The firmware directory contains elf symbols that we have trouble parsing
    # and that don't help with breakpad debugging (see crbug.com/213670).
    exclude_dirs = ["firmware"]

    cmd = ["cros_generate_breakpad_symbols"]
    if debug:
        cmd += ["--debug"]
    if ignore_errors:
        cmd += ["--ignore_errors"]
    for ignore_expected_file in ignore_expected_files:
        cmd += ["--ignore_expected_file=" + ignore_expected_file]

    # Execute for board in parallel with half # of cpus available to avoid
    # starving other parallel processes on the same machine.
    cmd += [
        "--board=%s" % build_target.name,
        "--jobs",
        str(max(1, multiprocessing.cpu_count() // 2)),
    ]
    cmd += ["--exclude-dir=%s" % x for x in exclude_dirs]

    logging.info("Generating breakpad symbols: %s.", cmd)
    result = chroot.run(cmd)
    return result


@metrics_lib.timed("service.sysroot.GatherSymbolFiles")
def GatherSymbolFiles(
    tempdir: str, destdir: str, paths: List[str]
) -> Generator[SymbolFileTuple, None, None]:
    """Locate symbol files in |paths|

    This generator function searches all paths for .sym files and copies them to
    destdir. A path to a tarball will result in the tarball being unpacked and
    examined. A path to a directory will result in the directory being searched
    for .sym files. The generator yields SymbolFileTuple objects that contain
    symbol file references which are valid after this exits. Those files may
    exist externally, or be created in the tempdir (when expanding tarballs).
    Typical usage in the BuildAPI will be for the .sym files to exist under a
    directory such as /build/<board>/usr/lib/debug/breakpad so that the path to
    a sym file will always be unique.
    Note: the caller must clean up the tempdir.
    Note: this function is recursive for tar files.

    Args:
        tempdir: Path to use for temporary files.
        destdir: All .sym files are copied to this path. Tarfiles are opened
            inside a tempdir and any .sym files within them are copied to
            destdir from within that temp path.
        paths: A list of input paths to walk. Files are returned based on .sym
            name w/out any checking internal symbol file format. Dirs are
            searched for files that end in ".sym". Urls are not handled.
            Tarballs are unpacked and walked.

    Yields:
        A SymbolFileTuple for every symbol file found in paths.
    """
    logging.info(
        "GatherSymbolFiles tempdir %s destdir %s paths %s",
        tempdir,
        destdir,
        paths,
    )
    for p in paths:
        o = urllib.parse.urlparse(p)
        if o.scheme:
            raise NotImplementedError("URL paths are not expected/handled: ", p)
        elif not os.path.exists(p):
            raise NoFilesError("The path did not exist: ", p)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                for f in files:
                    if f.endswith(".sym"):
                        # If p is '/tmp/foo' and filename is
                        # '/tmp/foo/bar/bar.sym', relative_path = 'bar/bar.sym'
                        filename = os.path.join(root, f)
                        relative_path = filename[len(p) :].lstrip("/")
                        try:
                            shutil.copy(
                                filename, os.path.join(destdir, relative_path)
                            )
                        except IOError:
                            # Handles pre-3.3 Python where we may need to make
                            # the target path's dirname before copying.
                            os.makedirs(
                                os.path.join(
                                    destdir, os.path.dirname(relative_path)
                                )
                            )
                            shutil.copy(
                                filename, os.path.join(destdir, relative_path)
                            )
                        yield SymbolFileTuple(
                            relative_path=relative_path,
                            source_file_name=filename,
                        )

        elif compression_lib.is_tarball(p):
            tardir = tempfile.mkdtemp(dir=tempdir)
            cache.Untar(os.path.realpath(p), tardir)
            for sym in GatherSymbolFiles(tardir, destdir, [tardir]):
                # The SymbolFileTuple is generated from [tardir], but we want
                # the source_file_name (which informational) to reflect the tar
                # path plus the relative path after the file is untarred. Thus,
                # something like /botpath/some/path/tmp22dl33sa/dir1/fileB.sym
                # (where the tardir is /botpath/some/path/tmp22dl33sa) has a
                # resulting path /botpath/some/path/symfiles.tar/dir1/fileB.sym
                # When we call GatherSymbolFiles with [tardir] as the argument,
                # the os.path.isdir case above will walk the tar contents,
                # processing only .sym. Non-sym files within the tar file will
                # be ignored (even tar files within tar files, which we don't
                # expect).
                new_source_file_name = sym.source_file_name.replace(tardir, p)
                yield SymbolFileTuple(
                    relative_path=sym.relative_path,
                    source_file_name=new_source_file_name,
                )

        elif os.path.isfile(p):
            # Path p is a file. This code path is only executed when a full file
            # path is one of the elements in the 'paths' argument. When a
            # directory is an element of the 'paths' argument, we walk the tree
            # (above) and process each file. When a tarball is an element of the
            # 'paths' argument, we untar it into a directory and recurse with
            # the temp tardir as the directory, so that tarfile contents are
            # processed (above) in the os.walk of the directory.
            if p.endswith(".sym"):
                shutil.copy(p, destdir)
                yield SymbolFileTuple(
                    relative_path=os.path.basename(p), source_file_name=p
                )
        else:
            raise ValueError("Unexpected input to GatherSymbolFiles: ", p)


def ArchiveSysroot(
    chroot: "chroot_lib.Chroot",
    sysroot: "sysroot_lib.Sysroot",
    _build_target: "build_target_lib.BuildTarget",
    output_dir: os.PathLike,
) -> Optional[os.PathLike]:
    """Archive the given sysroot.

    Args:
        chroot: The chroot in which the sysroot exists.
        sysroot: Sysroot that needs to be archived.
        output_dir: Directory in which the generated archive will be placed.

    Returns:
        The archive file path or None if the archive directory doesnt exists.
    """
    sysroot_path = Path(chroot.full_path(sysroot.path))
    if not sysroot_path.is_dir():
        return None

    osutils.SafeMakedirs(output_dir)
    archive_path = Path(output_dir) / SYSROOT_ARCHIVE_FILE

    compression_type = compression_lib.CompressionType.from_extension(
        SYSROOT_ARCHIVE_FILE
    )
    compression_lib.create_tarball(
        archive_path,
        sysroot_path,
        compression=compression_type,
        chroot=chroot.path,
        sudo=True,
    )

    return archive_path


def ExtractSysroot(
    chroot: "chroot_lib.Chroot",
    sysroot: "sysroot_lib.Sysroot",
    sysroot_archive: "os.PathLike",
) -> Optional[os.PathLike]:
    """Extract the given sysroot archive.

    Args:
        chroot: The chroot in which the sysroot exists.
        sysroot: Sysroot that needs to be extracted.
        sysroot_archive: The path of sysroot archive.

    Returns:
        The sysroot path or None if the sysroot directory doesn't exist.
    """
    sysroot_path = Path(chroot.full_path(sysroot.path))
    if not sysroot_path.is_dir():
        return None

    compression_lib.extract_tarball(
        Path(sysroot_archive),
        sysroot_path,
        sudo=True,
        replace_install_path=True,
    )
    return sysroot_path
