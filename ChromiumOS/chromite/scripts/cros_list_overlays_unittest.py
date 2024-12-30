# Copyright 2014 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Unittests for cros_list_overlays.py"""

from chromite.lib import cros_test_lib
from chromite.lib import portage_util
from chromite.scripts import cros_list_overlays


class ListOverlaysTest(cros_test_lib.MockTestCase):
    """Tests for main()"""

    def setUp(self) -> None:
        self.find_mock = self.PatchObject(portage_util, "FindOverlays")

    def testSmoke(self) -> None:
        """Basic confidence check"""
        cros_list_overlays.main([])

    def testAll(self) -> None:
        """Verify --all returns a lot."""
        cros_list_overlays.main(["--all"])

    def testBoard(self) -> None:
        """Check --board handling."""
        cros_list_overlays.main(["--board", "eve"])