# Copyright 2015 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unit tests for the flash module."""

import logging
import os
from unittest import mock

from chromite.cli import flash
from chromite.lib import commandline
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.lib import dev_server_wrapper
from chromite.lib import osutils
from chromite.lib import partial_mock


class USBImagerMock(partial_mock.PartialCmdMock):
    """Mock out USBImager."""

    TARGET = "chromite.cli.flash.USBImager"
    ATTRS = (
        "CopyImageToDevice",
        "ChooseRemovableDevice",
        "ListAllRemovableDevices",
        "GetRemovableDeviceDescription",
    )
    VALID_IMAGE = True

    def __init__(self) -> None:
        partial_mock.PartialCmdMock.__init__(self)

    def CopyImageToDevice(self, _inst, *_args, **_kwargs) -> None:
        """Mock out CopyImageToDevice."""

    def ChooseRemovableDevice(self, _inst, *_args, **_kwargs) -> None:
        """Mock out ChooseRemovableDevice."""

    def ListAllRemovableDevices(self, _inst, *_args, **_kwargs):
        """Mock out ListAllRemovableDevices."""
        return ["foo", "taco", "milk"]

    def GetRemovableDeviceDescription(self, _inst, *_args, **_kwargs) -> None:
        """Mock out GetRemovableDeviceDescription."""


class USBImagerTest(cros_test_lib.MockTempDirTestCase):
    """Test the flow of flash.Flash() with USBImager."""

    IMAGE = "/path/to/image"

    def Device(self, path):
        """Create a USB device for passing to flash.Flash()."""
        return commandline.Device(
            scheme=commandline.DeviceScheme.USB, path=path
        )

    def setUp(self) -> None:
        """Patches objects."""
        self.usb_mock = USBImagerMock()
        self.imager_mock = self.StartPatcher(self.usb_mock)
        self.PatchObject(
            dev_server_wrapper,
            "GetImagePathWithXbuddy",
            return_value=(
                "taco-paladin/R36/chromiumos_test_image.bin",
                "remote/taco-paladin/R36/test",
            ),
        )
        # To prevent flaky tests, patch this code. It currently attempts to
        # create files at the same path, potentially leading to conflicts.
        self.PatchObject(
            dev_server_wrapper.DevServerWrapper, "CreateStaticDirectory"
        )
        self.PatchObject(os.path, "exists", return_value=True)
        self.PatchObject(os.path, "getsize", return_value=200)
        self.isgpt_mock = self.PatchObject(
            flash, "_IsFilePathGPTDiskImage", return_value=True
        )
        self.PatchObject(osutils, "GetDeviceSize", return_value=200)

    def testLocalImagePathCopy(self) -> None:
        """Tests that imaging methods are called correctly."""
        with mock.patch("os.path.isfile", return_value=True):
            flash.Flash(self.Device("/dev/foo"), self.IMAGE)
            self.assertTrue(
                self.imager_mock.patched["CopyImageToDevice"].called
            )

    def testLocalBadImagePath(self) -> None:
        """Tests that using an image not having the magic bytes has prompt."""
        self.isgpt_mock.return_value = False
        with mock.patch("os.path.isfile", return_value=True):
            with mock.patch.object(
                cros_build_lib, "BooleanPrompt"
            ) as mock_prompt:
                mock_prompt.return_value = False
                flash.Flash(self.Device("/dev/foo"), self.IMAGE)
                self.assertTrue(mock_prompt.called)

    def testNonLocalImagePath(self) -> None:
        """Tests that we try to get the image path using xbuddy."""
        with mock.patch.object(
            dev_server_wrapper,
            "GetImagePathWithXbuddy",
            return_value=("translated/xbuddy/path", "resolved/xbuddy/path"),
        ) as mock_xbuddy:
            with mock.patch("os.path.isfile", return_value=False):
                with mock.patch("os.path.isdir", return_value=False):
                    flash.Flash(self.Device("/dev/foo"), self.IMAGE)
                    self.assertTrue(mock_xbuddy.called)

    def testConfirmNonRemovableDevice(self) -> None:
        """Tests that we ask user to confirm if the device is not removable."""
        with mock.patch.object(cros_build_lib, "BooleanPrompt") as mock_prompt:
            flash.Flash(self.Device("/dev/stub"), self.IMAGE)
            self.assertTrue(mock_prompt.called)

    def testSkipPromptNonRemovableDevice(self) -> None:
        """Tests that we skip the prompt for non-removable with --yes."""
        with mock.patch.object(cros_build_lib, "BooleanPrompt") as mock_prompt:
            flash.Flash(self.Device("/dev/stub"), self.IMAGE, yes=True)
            self.assertFalse(mock_prompt.called)

    def testChooseRemovableDevice(self) -> None:
        """Tests that we ask user to choose a device if none is given."""
        flash.Flash(self.Device(""), self.IMAGE)
        self.assertTrue(
            self.imager_mock.patched["ChooseRemovableDevice"].called
        )

    def testInsufficientRemovableDeviceStorage(self) -> None:
        self.PatchObject(osutils, "GetDeviceSize", return_value=100)
        with self.assertRaises(flash.FlashError):
            flash.Flash(self.Device(""), self.IMAGE)


class UsbImagerOperationTest(cros_test_lib.RunCommandTestCase):
    """Tests for flash.UsbImagerOperation."""

    # pylint: disable=protected-access

    def setUp(self) -> None:
        self.PatchObject(
            flash.UsbImagerOperation, "__init__", return_value=None
        )

    def testUsbImagerOperationCalled(self) -> None:
        """Test flash.UsbImagerOperation is called when log level <= NOTICE."""
        expected_cmd = [
            "dd",
            "if=foo",
            "of=bar",
            "bs=4M",
            "iflag=fullblock",
            "oflag=direct",
            "conv=fdatasync",
        ]
        usb_imager = flash.USBImager("stub_device", "board", "foo", "latest")
        run_mock = self.PatchObject(flash.UsbImagerOperation, "Run")
        self.PatchObject(
            logging.Logger, "getEffectiveLevel", return_value=logging.NOTICE
        )
        usb_imager.CopyImageToDevice("foo", "bar")

        # Check that flash.UsbImagerOperation.Run() is called correctly.
        run_mock.assert_called_with(
            cros_build_lib.sudo_run,
            expected_cmd,
            debug_level=logging.NOTICE,
            encoding="utf-8",
            update_period=0.5,
        )

    def testSudoRunCommandCalled(self) -> None:
        """Test that sudo_run is called when log level > NOTICE."""
        expected_cmd = [
            "sudo",
            "--",
            "dd",
            "if=foo",
            "of=bar",
            "bs=4M",
            "iflag=fullblock",
            "oflag=direct",
            "conv=fdatasync",
        ]
        usb_imager = flash.USBImager("stub_device", "board", "foo", "latest")
        self.PatchObject(
            logging.Logger, "getEffectiveLevel", return_value=logging.WARNING
        )
        usb_imager.CopyImageToDevice("foo", "bar")

        # Check that sudo_run() is called correctly.
        self.rc.assertCommandCalled(
            expected_cmd, debug_level=logging.NOTICE, print_cmd=False
        )

    def testPingDD(self) -> None:
        """Test that UsbImagerOperation._PingDD() sends the correct signal."""
        expected_cmd = ["sudo", "--", "kill", "-USR1", "5"]
        op = flash.UsbImagerOperation("foo")
        op._PingDD(5)

        # Check that sudo_run was called correctly.
        self.rc.assertCommandCalled(expected_cmd, print_cmd=False)

    def testGetDDPidFound(self) -> None:
        """Check that the expected pid is returned for _GetDDPid()."""
        expected_pid = 5
        op = flash.UsbImagerOperation("foo")
        self.PatchObject(osutils, "IsChildProcess", return_value=True)
        self.rc.AddCmdResult(
            partial_mock.Ignore(), stdout=f"{expected_pid}\n10\n"
        )

        pid = op._GetDDPid()

        # Check that the correct pid was returned.
        self.assertEqual(pid, expected_pid)

    def testGetDDPidNotFound(self) -> None:
        """Check -1 is returned for _GetDDPid() if the pids aren't valid."""
        expected_pid = -1
        op = flash.UsbImagerOperation("foo")
        self.PatchObject(osutils, "IsChildProcess", return_value=False)
        self.rc.AddCmdResult(partial_mock.Ignore(), stdout="5\n10\n")

        pid = op._GetDDPid()

        # Check that the correct pid was returned.
        self.assertEqual(pid, expected_pid)


class FlashUtilTest(cros_test_lib.MockTempDirTestCase):
    """Tests the helpers from cli.flash."""

    def testChooseImage(self) -> None:
        """Tests that we can detect a GPT image."""
        # pylint: disable=protected-access

        with self.PatchObject(
            flash, "_IsFilePathGPTDiskImage", return_value=True
        ):
            # No images defined. Choosing the image should raise an error.
            with self.assertRaises(ValueError):
                flash._ChooseImageFromDirectory(self.tempdir)

            file_a = os.path.join(self.tempdir, "a")
            osutils.Touch(file_a)
            # Only one image available, it should be selected automatically.
            self.assertEqual(
                file_a, flash._ChooseImageFromDirectory(self.tempdir)
            )

            osutils.Touch(os.path.join(self.tempdir, "b"))
            file_c = os.path.join(self.tempdir, "c")
            osutils.Touch(file_c)
            osutils.Touch(os.path.join(self.tempdir, "d"))

            # Multiple images available, we should ask the user to select the
            # right image.
            with self.PatchObject(cros_build_lib, "GetChoice", return_value=2):
                self.assertEqual(
                    file_c, flash._ChooseImageFromDirectory(self.tempdir)
                )

    def testIsFilePathGPTDiskImage(self) -> None:
        """Tests the GPT image probing."""
        # pylint: disable=protected-access

        INVALID_PMBR = b" " * 0x200
        INVALID_GPT = b" " * 0x200
        VALID_PMBR = (b" " * 0x1FE) + b"\x55\xaa"
        VALID_GPT = b"EFI PART" + (b" " * 0x1F8)
        TESTCASES = (
            (False, False, INVALID_PMBR + INVALID_GPT),
            (False, False, VALID_PMBR + INVALID_GPT),
            (False, True, INVALID_PMBR + VALID_GPT),
            (True, True, VALID_PMBR + VALID_GPT),
        )

        img = os.path.join(self.tempdir, "img.bin")
        for exp_pmbr_t, exp_pmbr_f, data in TESTCASES:
            osutils.WriteFile(img, data, mode="wb")
            self.assertEqual(
                flash._IsFilePathGPTDiskImage(img, require_pmbr=True),
                exp_pmbr_t,
            )
            self.assertEqual(
                flash._IsFilePathGPTDiskImage(img, require_pmbr=False),
                exp_pmbr_f,
            )
