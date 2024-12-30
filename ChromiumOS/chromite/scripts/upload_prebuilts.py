# Copyright 2012 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""This script is used to upload host prebuilts as well as board BINHOSTS.

Prebuilts are uploaded using gsutil to Google Storage. After these prebuilts
are successfully uploaded, a file is updated with the proper BINHOST version.

To read more about prebuilts/binhost binary packages please refer to:
http://goto/chromeos-prebuilts

Example of uploading prebuilt amd64 host files to Google Storage:
upload_prebuilts -p /b/cbuild/build -s -u gs://chromeos-prebuilt

Example of uploading x86-dogfood binhosts to Google Storage:
upload_prebuilts -b x86-dogfood -p /b/cbuild/build/ -u gs://chromeos-prebuilt -g
"""

import argparse
import datetime
import functools
import glob
import logging
import multiprocessing
import os
from pathlib import Path
import re
import tempfile
from typing import Any, Optional, Tuple

from chromite.cbuildbot import cbuildbot_alerts
from chromite.cbuildbot import commands
from chromite.lib import binpkg
from chromite.lib import chroot_lib
from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib
from chromite.lib import cros_sdk_lib
from chromite.lib import git
from chromite.lib import gs
from chromite.lib import osutils
from chromite.lib import parallel
from chromite.lib import portage_util
from chromite.lib.parser import package_info
from chromite.utils import gs_urls_util
from chromite.utils import pformat


# How many times to retry uploads.
_RETRIES = 10

# Multiplier for how long to sleep (in seconds) between retries; will delay
# (1*sleep) the first time, then (2*sleep), continuing via attempt * sleep.
_SLEEP_TIME = 60

# The length of time (in seconds) that Portage should wait before refetching
# binpkgs from the same binhost. We don't ever modify binhosts, so this should
# be something big.
_BINPKG_TTL = 60 * 60 * 24 * 365

_HOST_PACKAGES_PATH = "var/lib/portage/pkgs"
_HOST_ARCH = "amd64"
_BOARD_PATH = "build/%(board)s"
_REL_BOARD_PATH = "board/%(target)s/%(version)s"
_REL_HOST_PATH = "host/%(host_arch)s/%(target)s/%(version)s"
# Private overlays to look at for builds to filter
# relative to build path
_PRIVATE_OVERLAY_DIR = "src/private-overlays"
_GOOGLESTORAGE_GSUTIL_FILE = "googlestorage_acl.txt"
_BINHOST_BASE_URL = "gs://chromeos-prebuilt"
_PREBUILT_BASE_DIR = "src/third_party/chromiumos-overlay/chromeos/config/"
# Created in the event of new host targets becoming available
_PREBUILT_MAKE_CONF = {
    "amd64": os.path.join(_PREBUILT_BASE_DIR, "make.conf.amd64-host")
}


class BuildTarget:
    """A board/profile tuple."""

    def __init__(self, board, profile=None) -> None:
        self.board = board
        self.profile = profile

    def __str__(self) -> str:
        if self.profile:
            return "%s_%s" % (self.board, self.profile)
        else:
            return self.board

    def __eq__(self, other: Any) -> bool:
        return str(other) == str(self)

    def __hash__(self) -> int:
        return hash(str(self))


def GetVersion():
    """Get the version to put in LATEST and update the git version with."""
    return datetime.datetime.now().strftime("%Y.%m.%d.%H%M%S")


def _GsUpload(gs_context, acl, local_file, remote_file) -> None:
    """Upload to GS bucket.

    Args:
        gs_context: A lib.gs.GSContext instance.
        acl: The ACL to use for uploading the file.
        local_file: The local file to be uploaded.
        remote_file: The remote location to upload to.
    """
    CANNED_ACLS = [
        "public-read",
        "private",
        "bucket-owner-read",
        "authenticated-read",
        "bucket-owner-full-control",
        "public-read-write",
    ]
    if acl in CANNED_ACLS:
        gs_context.Copy(local_file, remote_file, acl=acl)
    else:
        # For private uploads we assume that the overlay board is set up
        # properly and a googlestore_acl.xml is present. Otherwise, this script
        # errors. We set version=0 here to ensure that the ACL is set only once
        # (see http://b/15883752#comment54).
        try:
            gs_context.Copy(local_file, remote_file, version=0)
        except gs.GSContextPreconditionFailed as ex:
            # If we received a GSContextPreconditionFailed error, we know that
            # the file exists now, but we don't know whether our specific update
            # succeeded. See http://b/15883752#comment62
            logging.warning(
                "Assuming upload succeeded despite PreconditionFailed errors: "
                "%s",
                ex,
            )

        if acl.endswith(".xml"):
            # Apply the passed in ACL xml file to the uploaded object.
            gs_context.SetACL(remote_file, acl=acl)
        else:
            gs_context.ChangeACL(remote_file, acl_args_file=acl)


def RemoteUpload(gs_context, acl, files, pool=10) -> None:
    """Upload to google storage.

    Create a pool of process and call _GsUpload with the proper arguments.

    Args:
        gs_context: A lib.gs.GSContext instance.
        acl: The canned acl used for uploading. acl can be one of:
            "public-read", "public-read-write", "authenticated-read",
            "bucket-owner-read", "bucket-owner-full-control", or "private".
        files: dictionary with keys to local files and values to remote path.
        pool: integer of maximum processes to have at the same time.

    Returns:
        Return a set of tuple arguments of the failed uploads
    """
    upload = functools.partial(_GsUpload, gs_context, acl)
    tasks = [[key, value] for key, value in files.items()]
    parallel.RunTasksInProcessPool(upload, tasks, pool)


def GenerateUploadDict(base_local_path, base_remote_path, pkgs):
    """Build a dictionary of local remote file key pairs to upload.

    Args:
        base_local_path: The base path to the files on the local hard drive.
        base_remote_path: The base path to the remote paths.
        pkgs: The packages to upload.

    Returns:
        Returns a dictionary of local_path/remote_path pairs
    """
    upload_files = {}
    for pkg in pkgs:
        suffix = pkg["CPV"] + ".tbz2"
        local_path = os.path.join(base_local_path, suffix)
        assert os.path.exists(local_path), "%s does not exist" % local_path
        upload_files[local_path] = os.path.join(base_remote_path, suffix)

        if pkg.get("DEBUG_SYMBOLS") == "yes":
            debugsuffix = pkg["CPV"] + ".debug.tbz2"
            local_path = os.path.join(base_local_path, debugsuffix)
            assert os.path.exists(local_path)
            upload_files[local_path] = os.path.join(
                base_remote_path, debugsuffix
            )

    return upload_files


def GetBoardOverlay(build_path, target):
    """Get the path to the board.

    Args:
        build_path: The path to the root of the build directory.
        target: The target board as a BuildTarget object.

    Returns:
        The last overlay configured for the given board as a string.
    """
    overlays = portage_util.FindOverlays(
        constants.BOTH_OVERLAYS, target.board, buildroot=build_path
    )
    # We only care about the last entry.
    return overlays[-1]


def DeterminePrebuiltConfFile(build_path, target):
    """Determine the prebuilt.conf file that needs to be updated for prebuilts.

    Args:
        build_path: The path to the root of the build directory.
        target: String representation of the board. This includes host and board
            targets.

    Returns:
        A string path to a prebuilt.conf file to be updated.
    """
    if _HOST_ARCH == target:
        # We are host.
        # Without more examples of hosts this is a kludge for now.
        # TODO(Scottz): as new host targets come online expand this to
        # work more like boards.
        make_path = _PREBUILT_MAKE_CONF[target]
    else:
        # We are a board
        board = GetBoardOverlay(build_path, target)
        make_path = os.path.join(board, "prebuilt.conf")

    return make_path


def UpdateBinhostConfFile(filepath: str, key: str, value: str) -> None:
    """Update binhost config file with key=value.

    The updated file will be committed, but not submitted.

    Args:
        filepath: Path to the key-value store file to update.
        key: Key to update.
        value: New value for key.
    """
    dirname, basename = os.path.split(os.path.abspath(filepath))
    osutils.SafeMakedirs(dirname)
    if not git.GetCurrentBranch(dirname):
        git.CreatePushBranch(
            constants.STABLE_EBUILD_BRANCH, dirname, sync=False
        )
    osutils.WriteFile(filepath, "", mode="a")
    if binpkg.UpdateKeyInLocalFile(filepath, key, value):
        desc = f"{basename}: {'updating' if value else 'clearing'} {key}"
        git.AddPath(filepath)
        git.Commit(dirname, desc)


def GenerateHtmlIndex(files, index, board, version, remote_location) -> None:
    """Given the list of |files|, generate an index.html at |index|.

    Args:
        files: The list of files to link to.
        index: The path to the html index.
        board: Name of the board this index is for.
        version: Build version this index is for.
        remote_location: Remote gs location prebuilts are uploaded to.
    """
    title = "Package Prebuilt Index: %s / %s" % (board, version)

    files = files + [
        ".|Google Storage Index",
        "..|",
    ]
    commands.GenerateHtmlIndex(
        index,
        files,
        title=title,
        url_base=gs_urls_util.GsUrlToHttp(remote_location),
    )


def _GrabAllRemotePackageIndexes(binhost_urls):
    """Grab all the packages files associated with a list of binhost_urls.

    Args:
        binhost_urls: The URLs for the directories containing the Packages files
            we want to grab.

    Returns:
        A list of PackageIndex objects.
    """
    pkg_indexes = []
    for url in binhost_urls:
        pkg_index = binpkg.GrabRemotePackageIndex(url)
        if pkg_index:
            pkg_indexes.append(pkg_index)
    return pkg_indexes


class PrebuiltUploader:
    """Synchronize host and board prebuilts."""

    def __init__(
        self,
        upload_location,
        acl,
        binhost_base_url,
        pkg_indexes,
        build_path,
        packages,
        skip_upload,
        binhost_conf_dir,
        dryrun,
        target,
        slave_targets,
        version,
        report,
        chroot=None,
        out_dir=None,
    ) -> None:
        """Constructor for prebuilt uploader object.

        This object can upload host or prebuilt files to Google Storage.

        Args:
            upload_location: The upload location.
            acl: The canned acl used for uploading to Google Storage. acl can be
                one of: "public-read", "public-read-write",
                "authenticated-read", "bucket-owner-read",
                "bucket-owner-full-control", "project-private", or "private"
                (see "gsutil help acls"). If we are not uploading to Google
                Storage, this parameter is unused.
            binhost_base_url: The URL used for downloading the prebuilts.
            pkg_indexes: Old uploaded prebuilts to compare against. Instead of
                uploading duplicate files, we just link to the old files.
            build_path: The path to the directory containing the chroot.
            packages: Packages to upload.
            skip_upload: Don't actually upload the tarballs.
            binhost_conf_dir: Directory where to store binhost.conf files.
            dryrun: Don't push or upload prebuilts.
            target: BuildTarget managed by this builder.
            slave_targets: List of BuildTargets managed by slave builders.
            version: A unique string, intended to be included in the upload
                path, which identifies the version number of the uploaded
                prebuilts.
            report: Dict in which to collect information to report to the user.
            chroot: Path to the chroot.
            out_dir: Path to the SDK output directory for the chroot.
        """
        self._upload_location = upload_location
        self._acl = acl
        self._binhost_base_url = binhost_base_url
        self._pkg_indexes = pkg_indexes
        self._build_path = build_path
        self._packages = set(packages)
        self._found_packages = set()
        self._skip_upload = skip_upload
        self._binhost_conf_dir = binhost_conf_dir
        self._dryrun = dryrun
        self._target = target
        self._slave_targets = slave_targets
        self._version = version
        self._report = report
        chroot_path = chroot or os.path.join(
            build_path, constants.DEFAULT_CHROOT_DIR
        )
        out_path = Path(
            out_dir or os.path.join(build_path, constants.DEFAULT_OUT_DIR)
        )
        self._chroot = chroot_lib.Chroot(path=chroot_path, out_path=out_path)
        self._gs_context = gs.GSContext(
            retries=_RETRIES, sleep=_SLEEP_TIME, dry_run=self._dryrun
        )

    def _Upload(self, local_file, remote_file) -> None:
        """Wrapper around _GsUpload"""
        _GsUpload(self._gs_context, self._acl, local_file, remote_file)

    def _ShouldFilterPackage(self, pkg):
        if not self._packages:
            return False
        cpv = package_info.SplitCPV(pkg["CPV"])
        self._found_packages.add(cpv.cp)
        return (
            cpv.package not in self._packages and cpv.cp not in self._packages
        )

    def _UploadPrebuilt(self, package_path, url_suffix) -> None:
        """Upload host or board prebuilt files to Google Storage space.

        Args:
            package_path: The path to the packages dir.
            url_suffix: The remote subdirectory where we should upload the
                packages.
        """
        # Process Packages file, removing duplicates and filtered packages.
        pkg_index = binpkg.GrabLocalPackageIndex(package_path)
        pkg_index.SetUploadLocation(self._binhost_base_url, url_suffix)
        pkg_index.RemoveFilteredPackages(self._ShouldFilterPackage)
        uploads = pkg_index.ResolveDuplicateUploads(self._pkg_indexes)
        unmatched_pkgs = self._packages - self._found_packages
        if unmatched_pkgs:
            logging.warning("unable to match packages: %r", unmatched_pkgs)

        # Write Packages file.
        pkg_index.header["TTL"] = _BINPKG_TTL
        tmp_packages_file = pkg_index.WriteToNamedTemporaryFile()

        remote_location = "%s/%s" % (
            self._upload_location.rstrip("/"),
            url_suffix,
        )
        assert remote_location.startswith("gs://")

        upload_files = GenerateUploadDict(
            package_path, remote_location, uploads
        )
        remote_file = "%s/Packages" % remote_location.rstrip("/")
        upload_files[tmp_packages_file.name] = remote_file

        # Build list of files to upload. Manually include the dev-only files but
        # skip them if not present.
        dev_only = os.path.join(package_path, "dev-only-extras.tar.xz")
        if os.path.exists(dev_only):
            upload_files[dev_only] = "%s/%s" % (
                remote_location.rstrip("/"),
                os.path.basename(dev_only),
            )

        RemoteUpload(self._gs_context, self._acl, upload_files)

        with tempfile.NamedTemporaryFile(
            prefix="chromite.upload_prebuilts.index."
        ) as index:
            GenerateHtmlIndex(
                [x[len(remote_location) + 1 :] for x in upload_files.values()],
                index.name,
                self._target,
                self._version,
                remote_location,
            )
            self._Upload(
                index.name, "%s/index.html" % remote_location.rstrip("/")
            )

            link_name = "Prebuilts[%s]: %s" % (self._target, self._version)
            url = "%s%s/index.html" % (
                gs_urls_util.PUBLIC_BASE_HTTPS_URL,
                remote_location[len(gs_urls_util.BASE_GS_URL) :],
            )
            cbuildbot_alerts.PrintBuildbotLink(link_name, url)

    def _UploadSdkTarball(
        self,
        board_path,
        url_suffix,
        prepackaged,
        toolchains_overlay_tarballs,
        toolchains_overlay_upload_path,
        toolchain_tarballs,
        toolchain_upload_path,
        sync_remote_latest_sdk_file: bool,
    ) -> None:
        """Upload a tarball of the sdk at the specified path to Google Storage.

        Args:
            board_path: The path to the board dir.
            url_suffix: The remote subdirectory where we should upload the
                packages.
            prepackaged: If given, a tarball that has been packaged outside of
                this script and should be used.
            toolchains_overlay_tarballs: List of toolchains overlay tarball
                specifications to upload. Items take the form
                "toolchains_spec:/path/to/tarball".
            toolchains_overlay_upload_path: Path template under the bucket to
                place toolchains overlay tarballs.
            toolchain_tarballs: List of toolchain tarballs to upload.
            toolchain_upload_path: Path under the bucket to place toolchain
                tarballs.
            sync_remote_latest_sdk_file: If True, update the remote latest SDK
                file in Google Storage to point to the newly uploaded SDK.
        """
        remote_location = "%s/%s" % (
            self._upload_location.rstrip("/"),
            url_suffix,
        )
        assert remote_location.startswith("gs://")
        boardname = os.path.basename(board_path.rstrip("/"))
        # We do not upload non SDK board tarballs,
        assert boardname == constants.CHROOT_BUILDER_BOARD
        assert prepackaged is not None

        # _version consists of a prefix followed by the actual version.
        # We want the version without the prefix. It starts with the
        # year, month, and date in YYYY.MM.DD format, so we match that.
        m = re.match(r"(.*-)?(\d\d\d\d\.\d\d\.\d\d.*)", self._version)
        assert m, "version does not match format .*YYYY.MM.DD.*"
        version_str = m[2]
        remote_tarfile = cros_sdk_lib.get_sdk_tarball_url(
            version_str, for_gsutil=True
        )
        # For SDK, also upload the manifest which is guaranteed to exist
        # by the builderstage.
        self._Upload(prepackaged + ".Manifest", remote_tarfile + ".Manifest")
        self._Upload(prepackaged, remote_tarfile)

        # Upload SDK toolchains overlays and toolchain tarballs, if given.
        for tarball_list, upload_path, qualifier_name in (
            (
                toolchains_overlay_tarballs,
                toolchains_overlay_upload_path,
                "toolchains",
            ),
            (toolchain_tarballs, toolchain_upload_path, "target"),
        ):
            for tarball_spec in tarball_list:
                qualifier_val, local_path = tarball_spec.split(":")
                suburl = upload_path % {qualifier_name: qualifier_val}
                remote_path = cros_sdk_lib.get_sdk_gs_url(
                    suburl=suburl,
                    for_gsutil=True,
                )
                self._Upload(local_path, remote_path)

        # Finally, also update the pointer to the latest SDK on which polling
        # scripts rely.
        if sync_remote_latest_sdk_file:
            self._UpdateRemoteSdkLatestFile(latest_sdk=version_str)

    def _UpdateRemoteSdkLatestFile(
        self,
        latest_sdk: Optional[str] = None,
    ) -> None:
        """Update the remote SDK pointer file on GS://.

        The remote file contains multiple key-value pairs. This function can
        update one or more of them; Nones will retain their existing values.

        Args:
            latest_sdk: The latest SDK that is tested and ready to be used. If
                None, then the existing value on GS:// will be retained.
        """
        # This would be a noop in dryrun mode -- or worse, it would fail to
        # parse the remote key-value store after pretending to download it.
        # Instead of side-stepping errors, return early with descriptive logs.
        if self._dryrun:
            logging.debug("Not updating remote SDK latest file in dryrun mode.")
            if latest_sdk is not None:
                logging.debug("Would have set LATEST_SDK=%s", latest_sdk)
            return

        # Get existing values from the remote file.
        remote_pointerfile = cros_sdk_lib.get_sdk_latest_conf_file_url(
            for_gsutil=True
        )
        existing_keyval = self._gs_context.LoadKeyValueStore(
            remote_pointerfile, acl=self._acl
        )

        for required_key in ("LATEST_SDK",):
            if required_key not in existing_keyval:
                raise ValueError(
                    f"Remote pointer file {remote_pointerfile} missing "
                    f"expected key {required_key}:\n{existing_keyval}"
                )

        # If any values were not specified in args, use the existing values.
        if latest_sdk is None:
            latest_sdk = existing_keyval["LATEST_SDK"]

        # Write a new local latest file with target values, and upload.
        new_file_contents = self._CreateRemoteSdkLatestFileContents(latest_sdk)
        with osutils.TempDir() as tmpdir:
            local_pointerfile = os.path.join(tmpdir, "cros-sdk-latest.conf")
            osutils.WriteFile(local_pointerfile, new_file_contents)
            self._Upload(local_pointerfile, remote_pointerfile)

    @staticmethod
    def _CreateRemoteSdkLatestFileContents(latest_sdk: str) -> str:
        """Generate file contents for a remote SDK file.

        Args:
            latest_sdk: The latest SDK that is tested and ready to be used.

        Returns:
            The contents of a remote SDK latest file containing the given args
            as a key-value store.
        """
        return f"""\
# The most recent SDK that is tested and ready for use.
LATEST_SDK=\"{latest_sdk}\""""

    def _GetTargets(self):
        """Retuns the list of targets to use."""
        targets = self._slave_targets[:]
        if self._target:
            targets.append(self._target)

        return targets

    def SyncHostPrebuilts(self, key, git_sync, sync_binhost_conf) -> None:
        """Synchronize host prebuilt files.

        This function will sync both the standard host packages, plus the host
        packages associated with all targets that have been "setup" with the
        current host's chroot. For instance, if this host has been used to build
        x86-generic, it will sync the host packages associated with
        'i686-pc-linux-gnu'. If this host has also been used to build
        arm-generic, it will also sync the host packages associated with
        'armv7a-cros-linux-gnueabi'.

        Args:
            key: The variable key to update in the git file.
            git_sync: If set, update make.conf of target to reference the latest
                prebuilt packages generated here.
            sync_binhost_conf: If set, update binhost config file in
                chromiumos-overlay for the host.
        """
        # Slave boards are listed before the master board so that the master
        # board takes priority (i.e. x86-generic preflight host prebuilts takes
        # priority over preflight host prebuilts from other builders.)
        binhost_urls = []
        for target in self._GetTargets():
            url_suffix = _REL_HOST_PATH % {
                "version": self._version,
                "host_arch": _HOST_ARCH,
                "target": target,
            }
            packages_url_suffix = "%s/packages" % url_suffix.rstrip("/")

            if self._target == target and not self._skip_upload:
                # Upload prebuilts.
                package_path = self._chroot.full_path(_HOST_PACKAGES_PATH)
                self._UploadPrebuilt(package_path, packages_url_suffix)

            # Record URL where prebuilts were uploaded.
            binhost_urls.append(
                "%s/%s/"
                % (
                    self._binhost_base_url.rstrip("/"),
                    packages_url_suffix.rstrip("/"),
                )
            )

        binhost = " ".join(binhost_urls)
        if git_sync:
            git_file = os.path.join(
                self._build_path, _PREBUILT_MAKE_CONF[_HOST_ARCH]
            )
            binpkg.UpdateAndSubmitKeyValueFile(
                git_file, {key: binhost}, self._report, dryrun=self._dryrun
            )
        if sync_binhost_conf:
            binhost_conf = os.path.join(
                self._binhost_conf_dir, "host", "%s-%s.conf" % (_HOST_ARCH, key)
            )
            UpdateBinhostConfFile(binhost_conf, key, binhost)

    def SyncBoardPrebuilts(
        self,
        key,
        git_sync,
        sync_binhost_conf,
        upload_board_tarball,
        prepackaged_board,
        toolchains_overlay_tarballs,
        toolchains_overlay_upload_path,
        toolchain_tarballs,
        toolchain_upload_path,
        sync_remote_latest_sdk_file: bool,
    ) -> None:
        """Synchronize board prebuilt files.

        Args:
            key: The variable key to update in the git file.
            git_sync: If set, update make.conf of target to reference the latest
                prebuilt packages generated here.
            sync_binhost_conf: If set, update binhost config file in
                chromiumos-overlay for the current board.
            upload_board_tarball: Include a tarball of the board in our upload.
            prepackaged_board: A tarball of the board built outside of this
                script.
            toolchains_overlay_tarballs: List of toolchains overlay tarball
                specifications to upload. Items take the form
                "toolchains_spec:/path/to/tarball".
            toolchains_overlay_upload_path: Path template under the bucket to
                place toolchains overlay tarballs.
            toolchain_tarballs: A list of toolchain tarballs to upload.
            toolchain_upload_path: Path under the bucket to place toolchain
                tarballs.
            sync_remote_latest_sdk_file: If True, update the remote latest SDK
                file in Google Storage to point to the newly uploaded SDK.
        """
        updated_binhosts = set()
        for target in self._GetTargets():
            board_path = self._chroot.full_path(
                _BOARD_PATH % {"board": target.board}
            )
            package_path = os.path.join(board_path, "packages")
            url_suffix = _REL_BOARD_PATH % {
                "target": target,
                "version": self._version,
            }
            packages_url_suffix = "%s/packages" % url_suffix.rstrip("/")

            # Process the target board differently if it is the main --board.
            if self._target == target and not self._skip_upload:
                # This strips "chroot" prefix because that is sometimes added as
                # the --prepend-version argument (e.g. by chromiumos-sdk bot).
                # TODO(build): Clean it up to be less hard-coded.
                version_str = self._version[len("chroot-") :]

                # Upload board tarballs in the background.
                if upload_board_tarball:
                    if toolchain_upload_path:
                        toolchain_upload_path %= {"version": version_str}
                    if toolchains_overlay_upload_path:
                        toolchains_overlay_upload_path %= {
                            "version": version_str
                        }
                    tar_process = multiprocessing.Process(
                        target=self._UploadSdkTarball,
                        args=(
                            board_path,
                            url_suffix,
                            prepackaged_board,
                            toolchains_overlay_tarballs,
                            toolchains_overlay_upload_path,
                            toolchain_tarballs,
                            toolchain_upload_path,
                            sync_remote_latest_sdk_file,
                        ),
                    )
                    tar_process.start()

                # Upload prebuilts.
                self._UploadPrebuilt(package_path, packages_url_suffix)

                # Make sure we finished uploading the board tarballs.
                if upload_board_tarball:
                    tar_process.join()
                    assert tar_process.exitcode == 0

            # Record URL where prebuilts were uploaded.
            url_value = "%s/%s/" % (
                self._binhost_base_url.rstrip("/"),
                packages_url_suffix.rstrip("/"),
            )

            if git_sync:
                git_file = DeterminePrebuiltConfFile(self._build_path, target)
                binpkg.UpdateAndSubmitKeyValueFile(
                    git_file,
                    {key: url_value},
                    self._report,
                    dryrun=self._dryrun,
                )

            if sync_binhost_conf:
                # Update the binhost configuration file in git.
                binhost_conf = os.path.join(
                    self._binhost_conf_dir,
                    "target",
                    "%s-%s.conf" % (target, key),
                )
                updated_binhosts.add(binhost_conf)
                UpdateBinhostConfFile(binhost_conf, key, url_value)

        if sync_binhost_conf:
            # Clear all old binhosts. The files must be left empty in case
            # anybody is referring to them.
            all_binhosts = set(
                glob.glob(
                    os.path.join(
                        self._binhost_conf_dir, "target", "*-%s.conf" % key
                    )
                )
            )
            for binhost_conf in all_binhosts - updated_binhosts:
                UpdateBinhostConfFile(binhost_conf, key, "")


class _AddSlaveBoardAction(argparse.Action):
    """Callback that adds a slave board to the list of slave targets."""

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        getattr(namespace, self.dest).append(BuildTarget(values))


class _AddSlaveProfileAction(argparse.Action):
    """Callback that adds a slave profile to the list of slave targets."""

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        if not namespace.slave_targets:
            parser.error("Must specify --slave-board before --slave-profile")
        if namespace.slave_targets[-1].profile is not None:
            parser.error("Cannot specify --slave-profile twice for same board")
        namespace.slave_targets[-1].profile = values


def ParseOptions(argv) -> Tuple[argparse.Namespace, Optional[BuildTarget]]:
    """Returns options given by the user and the target specified.

    Args:
        argv: The args to parse.

    Returns:
        A tuple containing a parsed options object and BuildTarget.
        The target instance is None if no board is specified.
    """
    parser = commandline.ArgumentParser(description=__doc__, dryrun=True)
    parser.add_argument(
        "-H",
        "--binhost-base-url",
        default=_BINHOST_BASE_URL,
        help="Base URL to use for binhost in make.conf updates",
    )
    parser.add_argument(
        "--previous-binhost-url",
        action="append",
        default=[],
        help="Previous binhost URL",
    )
    parser.add_argument(
        "-b", "--board", help="Board type that was built on this machine"
    )
    parser.add_argument(
        "-B",
        "--prepackaged-tarball",
        type="str_path",
        help="Board tarball prebuilt outside of this script.",
    )
    parser.add_argument(
        "--toolchains-overlay-tarball",
        dest="toolchains_overlay_tarballs",
        action="append",
        default=[],
        help="Toolchains overlay tarball specification to "
        "upload. Takes the form "
        '"toolchains_spec:/path/to/tarball".',
    )
    parser.add_argument(
        "--toolchains-overlay-upload-path",
        default="",
        help="Path template for uploading toolchains overlays.",
    )
    parser.add_argument(
        "--toolchain-tarball",
        dest="toolchain_tarballs",
        action="append",
        default=[],
        help="Redistributable toolchain tarball.",
    )
    parser.add_argument(
        "--toolchain-upload-path",
        default="",
        help="Path to place toolchain tarballs in the sdk tree.",
    )
    parser.add_argument(
        "--profile", help="Profile that was built on this machine"
    )
    parser.add_argument(
        "--slave-board",
        default=[],
        action=_AddSlaveBoardAction,
        dest="slave_targets",
        help="Board type that was built on a slave machine. To "
        "add a profile to this board, use --slave-profile.",
    )
    parser.add_argument(
        "--slave-profile",
        action=_AddSlaveProfileAction,
        help="Board profile that was built on a slave machine. "
        "Applies to previous slave board.",
    )
    parser.add_argument(
        "-p",
        "--build-path",
        required=True,
        help="Path to the directory containing the chroot",
    )
    parser.add_argument(
        "--chroot",
        help="Path where the chroot is located. "
        "(Default: {build_path}/chroot)",
    )
    parser.add_argument(
        "--out-dir",
        help="Path where the SDK output directory is located. "
        "(Default: {build_path}/out)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write a JSON report to the specified file. "
        "(Default is not to write the report.)",
    )
    parser.add_argument(
        "--packages",
        action="append",
        default=[],
        help="Only include the specified packages. "
        "(Default is to include all packages.)",
    )
    parser.add_argument(
        "-s",
        "--sync-host",
        default=False,
        action="store_true",
        help="Sync host prebuilts",
    )
    parser.add_argument(
        "-g",
        "--git-sync",
        default=False,
        action="store_true",
        help="Enable git version sync (This commits to a repo.) "
        "This is used by full builders to commit directly "
        "to board overlays.",
    )
    parser.add_argument(
        "--sync-remote-latest-sdk-file",
        action="store_true",
        default=True,
        help="Sync the remote latest SDK file on GS://. (Default)",
    )
    parser.add_argument(
        "--no-sync-remote-latest-sdk-file",
        dest="sync_remote_latest_sdk_file",
        action="store_false",
        help="Skip syncing the remote latest SDK file on GS://.",
    )
    parser.add_argument("-u", "--upload", help="Upload location")
    parser.add_argument(
        "-V",
        "--prepend-version",
        help="Add an identifier to the front of the version",
    )
    parser.add_argument(
        "-f",
        "--filters",
        action="store_true",
        default=False,
        help="Turn on filtering of private ebuild packages",
    )
    parser.add_argument(
        "-k",
        "--key",
        default="PORTAGE_BINHOST",
        help="Key to update in make.conf / binhost.conf",
    )
    parser.add_argument("--set-version", help="Specify the version string")
    parser.add_argument(
        "--sync-binhost-conf",
        default=False,
        action="store_true",
        help="Update binhost.conf in chromiumos-overlay or "
        "chromeos-overlay. Commit the changes, but don't "
        "push them. This is used for preflight binhosts.",
    )
    parser.add_argument(
        "--binhost-conf-dir",
        help="Directory to commit binhost config with " "--sync-binhost-conf.",
    )
    parser.add_argument(
        "-P",
        "--private",
        action="store_true",
        default=False,
        help="Mark gs:// uploads as private.",
    )
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        default=False,
        help="Skip upload step.",
    )
    parser.add_argument(
        "--upload-board-tarball",
        action="store_true",
        default=False,
        help="Upload board tarball to Google Storage.",
    )

    options = parser.parse_args(argv)
    if not options.upload and not options.skip_upload:
        parser.error("you need to provide an upload location using -u")
    if not options.set_version and options.skip_upload:
        parser.error(
            "If you are using --skip-upload, you must specify a "
            "version number using --set-version."
        )

    target = None
    if options.board:
        target = BuildTarget(options.board, options.profile)

    if target in options.slave_targets:
        parser.error("--board/--profile must not also be a slave target.")

    if len(set(options.slave_targets)) != len(options.slave_targets):
        parser.error("--slave-boards must not have duplicates.")

    if options.slave_targets and options.git_sync:
        parser.error("--slave-boards is not compatible with --git-sync")

    if (
        options.upload_board_tarball
        and options.skip_upload
        and options.board == "amd64-host"
    ):
        parser.error(
            "--skip-upload is not compatible with "
            "--upload-board-tarball and --board=amd64-host"
        )

    if (
        options.upload_board_tarball
        and not options.skip_upload
        and not options.upload.startswith("gs://")
    ):
        parser.error(
            "--upload-board-tarball only works with gs:// URLs.\n"
            "--upload must be a gs:// URL."
        )

    if options.upload_board_tarball and options.prepackaged_tarball is None:
        parser.error("--upload-board-tarball requires --prepackaged-tarball")

    if options.private:
        if options.sync_host:
            parser.error(
                "--private and --sync-host/-s cannot be specified "
                "together; we do not support private host prebuilts"
            )

        if not options.upload or not options.upload.startswith("gs://"):
            parser.error(
                "--private is only valid for gs:// URLs; "
                "--upload must be a gs:// URL."
            )

        if options.binhost_base_url != _BINHOST_BASE_URL:
            parser.error(
                "when using --private the --binhost-base-url "
                "is automatically derived."
            )

    if options.sync_binhost_conf and not options.binhost_conf_dir:
        parser.error("--sync-binhost-conf requires --binhost-conf-dir")

    if (
        options.toolchains_overlay_tarballs
        and not options.toolchains_overlay_upload_path
    ):
        parser.error(
            "--toolchains-overlay-tarball requires "
            "--toolchains-overlay-upload-path"
        )

    return options, target


def main(argv) -> None:
    # We accumulate information about actions taken and report it at the end
    # if asked to do so. Currently, this only records CL creation, which
    # is the only thing we need for now.
    report = {}

    # Set umask so that files created as root are readable.
    os.umask(0o22)

    options, target = ParseOptions(argv)

    # Calculate a list of Packages index files to compare against. Whenever we
    # upload a package, we check to make sure it's not already stored in one of
    # the packages files we uploaded. This list of packages files might contain
    # both board and host packages.
    pkg_indexes = _GrabAllRemotePackageIndexes(options.previous_binhost_url)

    if options.set_version:
        version = options.set_version
    else:
        version = GetVersion()

    if options.prepend_version:
        version = "%s-%s" % (options.prepend_version, version)

    acl = "public-read"
    binhost_base_url = options.binhost_base_url

    if options.private:
        binhost_base_url = options.upload
        if target:
            acl = portage_util.FindOverlayFile(
                _GOOGLESTORAGE_GSUTIL_FILE,
                board=target.board,
                buildroot=options.build_path,
            )
            if acl is None:
                cros_build_lib.Die(
                    "No Google Storage ACL file %s found in %s overlay.",
                    _GOOGLESTORAGE_GSUTIL_FILE,
                    target.board,
                )

    binhost_conf_dir = None
    if options.binhost_conf_dir:
        binhost_conf_dir = os.path.join(
            options.build_path, options.binhost_conf_dir
        )

    uploader = PrebuiltUploader(
        options.upload,
        acl,
        binhost_base_url,
        pkg_indexes,
        options.build_path,
        options.packages,
        options.skip_upload,
        binhost_conf_dir,
        options.dryrun,
        target,
        options.slave_targets,
        version,
        report,
        chroot=options.chroot,
        out_dir=options.out_dir,
    )

    if options.sync_host:
        uploader.SyncHostPrebuilts(
            options.key, options.git_sync, options.sync_binhost_conf
        )

    if options.board or options.slave_targets:
        uploader.SyncBoardPrebuilts(
            options.key,
            options.git_sync,
            options.sync_binhost_conf,
            options.upload_board_tarball,
            options.prepackaged_tarball,
            options.toolchains_overlay_tarballs,
            options.toolchains_overlay_upload_path,
            options.toolchain_tarballs,
            options.toolchain_upload_path,
            options.sync_remote_latest_sdk_file,
        )

    if options.output:
        with open(options.output, "w", encoding="utf-8") as f:
            pformat.json(report, fp=f)
