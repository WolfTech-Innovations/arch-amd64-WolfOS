# Copyright 2017 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Tests the `cros chroot` command."""

from unittest import mock

from chromite.cli import command_unittest
from chromite.cli.cros import cros_tryjob
from chromite.lib import config_lib
from chromite.lib import cros_build_lib
from chromite.lib import cros_test_lib
from chromite.utils import outcap


class MockTryjobCommand(command_unittest.MockCommand):
    """Mock out the `cros tryjob` command."""

    TARGET = "chromite.cli.cros.cros_tryjob.TryjobCommand"
    TARGET_CLASS = cros_tryjob.TryjobCommand
    COMMAND = "tryjob"


class TryjobTest(cros_test_lib.MockTestCase):
    """Base class for Tryjob command tests."""

    def setUp(self) -> None:
        self.cmd_mock = None

    def SetupCommandMock(self, cmd_args):
        """Sets up the `cros tryjob` command mock."""
        self.cmd_mock = MockTryjobCommand(cmd_args)
        self.StartPatcher(self.cmd_mock)

        return self.cmd_mock.inst.options


class TryjobTestPrintKnownConfigs(TryjobTest):
    """Test the PrintKnownConfigs function."""

    def setUp(self) -> None:
        self.site_config = config_lib.GetConfig()

    def testConfigsToPrintAllIncluded(self) -> None:
        """Test we can generate results for --list."""
        tryjob_configs = cros_tryjob.ConfigsToPrint(
            self.site_config, production=False, build_config_fragments=[]
        )

        release_configs = cros_tryjob.ConfigsToPrint(
            self.site_config, production=True, build_config_fragments=[]
        )

        self.assertEqual(
            len(self.site_config), len(tryjob_configs) + len(release_configs)
        )

    def testConfigsToPrintFiltered(self) -> None:
        """Test ConfigsToPrint filters correctly."""
        tryjob_configs = cros_tryjob.ConfigsToPrint(
            self.site_config, production=False, build_config_fragments=[]
        )

        board_tryjob_configs = cros_tryjob.ConfigsToPrint(
            self.site_config, production=False, build_config_fragments=["eve"]
        )

        board_release_tryjob_configs = cros_tryjob.ConfigsToPrint(
            self.site_config,
            production=False,
            build_config_fragments=["eve", "release"],
        )

        # Prove expecting things are there.
        self.assertIn(self.site_config["eve-release-tryjob"], tryjob_configs)
        self.assertIn(
            self.site_config["eve-release-tryjob"], board_tryjob_configs
        )
        self.assertIn(
            self.site_config["eve-release-tryjob"],
            board_release_tryjob_configs,
        )

        # Unexpecting things aren't.
        self.assertNotIn(self.site_config["eve-release"], tryjob_configs)

        # And that we really filtered something out in every case.
        self.assertLess(
            len(board_release_tryjob_configs), len(board_tryjob_configs)
        )

        self.assertLess(len(board_tryjob_configs), len(tryjob_configs))

    def testListTryjobs(self) -> None:
        """Test we can generate results for --list."""
        with outcap.OutputCapturer() as output:
            cros_tryjob.PrintKnownConfigs(
                self.site_config, production=False, build_config_fragments=[]
            )

        # We have at least 10 lines of output, and no error out.
        self.assertGreater(len(output.GetStdoutLines()), 10)
        self.assertEqual("", output.GetStderr())

    def testListProduction(self) -> None:
        """Test we can generate results for --production --list."""
        with outcap.OutputCapturer() as output:
            cros_tryjob.PrintKnownConfigs(
                self.site_config, production=True, build_config_fragments=[]
            )

        # We have at least 10 lines of output, and no error out.
        self.assertGreater(len(output.GetStdoutLines()), 10)
        self.assertEqual("", output.GetStderr())

    def testListTryjobsEmpty(self) -> None:
        """Test we can generate ~empty results for failed --list search."""
        with outcap.OutputCapturer() as output:
            cros_tryjob.PrintKnownConfigs(
                self.site_config,
                production=False,
                build_config_fragments=["this-is-not-a-builder-name"],
            )

        # We have fewer than 6 lines of output, and no error out.
        self.assertLess(len(output.GetStdoutLines()), 6)
        self.assertEqual("", output.GetStderr())


class TryjobTestParsing(TryjobTest):
    """Test cros try command line parsing."""

    def setUp(self) -> None:
        self.expected = {
            "where": cros_tryjob.REMOTE,
            "buildroot": None,
            "branch": "main",
            "production": False,
            "yes": False,
            "list": False,
            "gerrit_patches": [],
            "local_patches": [],
            "passthrough": None,
            "passthrough_raw": None,
            "build_configs": ["amd64-generic-full-tryjob"],
        }

    def testMinimalParsing(self) -> None:
        """Tests flow for an interactive session."""
        self.SetupCommandMock(["amd64-generic-full-tryjob"])
        options = self.cmd_mock.inst.options
        self.assertGreaterEqual(vars(options).items(), self.expected.items())

    def testComplexParsingRemote(self) -> None:
        """Tests flow for an interactive session."""
        self.SetupCommandMock(
            [
                "--remote",
                "--yes",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--buildroot",
                "/buildroot",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--local-patches",
                "chromiumos/chromite:tryjob",
                "-p",
                "other:other",
                "--chrome_version",
                "chrome_git_hash",
                "--debug-cidb",
                "--pass-through=--cbuild-arg",
                "--pass-through",
                "bar",
                "--list",
                "amd64-generic-full-tryjob",
                "eve-release",
            ]
        )
        options = self.cmd_mock.inst.options

        self.expected.update(
            {
                "where": cros_tryjob.REMOTE,
                "buildroot": "/buildroot",
                "branch": "main",
                "yes": True,
                "list": True,
                "gerrit_patches": ["123", "*123", "123..456"],
                "local_patches": ["chromiumos/chromite:tryjob", "other:other"],
                "passthrough": [
                    "--latest-toolchain",
                    "--notests",
                    "--novmtests",
                    "--noimagetests",
                    "--timeout",
                    "5",
                    "--confidence-check-build",
                    "--chrome_version",
                    "chrome_git_hash",
                    "--debug-cidb",
                ],
                "passthrough_raw": ["--cbuild-arg", "bar"],
                "build_configs": ["amd64-generic-full-tryjob", "eve-release"],
            }
        )
        self.assertGreaterEqual(vars(options).items(), self.expected.items())

    def testComplexParsingLocal(self) -> None:
        """Tests flow for an interactive session."""
        self.SetupCommandMock(
            [
                "--yes",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--local",
                "--buildroot",
                "/buildroot",
                "--git-cache-dir",
                "/git-cache",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--local-patches",
                "chromiumos/chromite:tryjob",
                "-p",
                "other:other",
                "--chrome_version",
                "chrome_git_hash",
                "--debug-cidb",
                "--pass-through=--cbuild-arg",
                "--pass-through",
                "bar",
                "--list",
                "amd64-generic-full",
                "eve-release",
            ]
        )
        options = self.cmd_mock.inst.options

        self.expected.update(
            {
                "where": cros_tryjob.LOCAL,
                "buildroot": "/buildroot",
                "git_cache_dir": "/git-cache",
                "branch": "main",
                "yes": True,
                "list": True,
                "gerrit_patches": ["123", "*123", "123..456"],
                "local_patches": ["chromiumos/chromite:tryjob", "other:other"],
                "passthrough": [
                    "--latest-toolchain",
                    "--notests",
                    "--novmtests",
                    "--noimagetests",
                    "--timeout",
                    "5",
                    "--confidence-check-build",
                    "--chrome_version",
                    "chrome_git_hash",
                    "--debug-cidb",
                ],
                "passthrough_raw": ["--cbuild-arg", "bar"],
                "build_configs": ["amd64-generic-full", "eve-release"],
            }
        )
        self.assertGreaterEqual(vars(options).items(), self.expected.items())

    def testComplexParsingCbuildbot(self) -> None:
        """Tests flow for an interactive session."""
        self.SetupCommandMock(
            [
                "--yes",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--cbuildbot",
                "--buildroot",
                "/buildroot",
                "--git-cache-dir",
                "/git-cache",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--local-patches",
                "chromiumos/chromite:tryjob",
                "-p",
                "other:other",
                "--chrome_version",
                "chrome_git_hash",
                "--pass-through=--cbuild-arg",
                "--pass-through",
                "bar",
                "--list",
                "amd64-generic-full-tryjob",
                "eve-release",
            ]
        )
        options = self.cmd_mock.inst.options

        self.expected.update(
            {
                "where": cros_tryjob.CBUILDBOT,
                "buildroot": "/buildroot",
                "git_cache_dir": "/git-cache",
                "branch": "main",
                "yes": True,
                "list": True,
                "gerrit_patches": ["123", "*123", "123..456"],
                "local_patches": ["chromiumos/chromite:tryjob", "other:other"],
                "passthrough": [
                    "--latest-toolchain",
                    "--notests",
                    "--novmtests",
                    "--noimagetests",
                    "--timeout",
                    "5",
                    "--confidence-check-build",
                    "--chrome_version",
                    "chrome_git_hash",
                ],
                "passthrough_raw": ["--cbuild-arg", "bar"],
                "build_configs": ["amd64-generic-full-tryjob", "eve-release"],
            }
        )
        self.assertGreaterEqual(vars(options).items(), self.expected.items())

    def testPayloadsParsing(self) -> None:
        """Tests flow for an interactive session."""
        self.SetupCommandMock(
            ["--version", "9795.0.0", "--channel", "canary", "eve-payloads"]
        )
        options = self.cmd_mock.inst.options

        self.expected.update(
            {
                "passthrough": ["--version", "9795.0.0", "--channel", "canary"],
                "build_configs": ["eve-payloads"],
            }
        )
        self.assertGreaterEqual(vars(options).items(), self.expected.items())


class TryjobTestProcessOptions(TryjobTest):
    """Test cros_tryjob.TryjobCommand.ProcessOptions."""

    def testRemote(self) -> None:
        """Test default remote buildroot."""
        self.SetupCommandMock(["config"])
        options = self.cmd_mock.inst.options

        cros_tryjob.TryjobCommand.ProcessOptions(None, options)

        self.assertIsNone(options.buildroot)
        self.assertIsNone(options.git_cache_dir)

    def testLocalDefault(self) -> None:
        """Test default local buildroot."""
        self.SetupCommandMock(["--local", "config"])
        options = self.cmd_mock.inst.options

        cros_tryjob.TryjobCommand.ProcessOptions(None, options)

        self.assertTrue(options.buildroot.endswith("/tryjob"))
        self.assertTrue(options.git_cache_dir.endswith("/tryjob/.git_cache"))

    def testLocalExplicit(self) -> None:
        """Test explicit local buildroot."""
        self.SetupCommandMock(
            [
                "--local",
                "--buildroot",
                "/buildroot",
                "--git-cache-dir",
                "/git-cache",
                "config",
            ]
        )
        options = self.cmd_mock.inst.options

        cros_tryjob.TryjobCommand.ProcessOptions(None, options)

        self.assertEqual(options.buildroot, "/buildroot")
        self.assertEqual(options.git_cache_dir, "/git-cache")

    def testCbuildbotDefault(self) -> None:
        """Test default cbuildbot buildroot."""
        self.SetupCommandMock(["--cbuildbot", "config"])
        options = self.cmd_mock.inst.options

        cros_tryjob.TryjobCommand.ProcessOptions(None, options)

        self.assertTrue(options.buildroot.endswith("/cbuild"))
        self.assertTrue(options.git_cache_dir.endswith("/cbuild/.git_cache"))

    def testCbuildbotExplicit(self) -> None:
        """Test explicit cbuildbot buildroot."""
        self.SetupCommandMock(
            [
                "--cbuildbot",
                "--buildroot",
                "/buildroot",
                "--git-cache-dir",
                "/git-cache",
                "config",
            ]
        )
        options = self.cmd_mock.inst.options

        cros_tryjob.TryjobCommand.ProcessOptions(None, options)

        self.assertEqual(options.buildroot, "/buildroot")
        self.assertEqual(options.git_cache_dir, "/git-cache")


class PromptException(Exception):
    """Raise this in tests, instead of using an interactive prompt."""


class TryjobTestVerifyOptions(TryjobTest):
    """Test cros_tryjob.VerifyOptions."""

    def setUp(self) -> None:
        self.site_config = config_lib.GetConfig()

        # Raise an exception instead of blocking the test on a prompt.
        self.PatchObject(
            cros_build_lib, "BooleanPrompt", side_effect=PromptException
        )

    def testEmpty(self) -> None:
        """Test option verification with no options."""
        self.SetupCommandMock([])

        with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )
        self.assertEqual(cm.exception.code, 1)

    def testMinimal(self) -> None:
        """Test option verification with simplest normal options."""
        self.SetupCommandMock(
            [
                "-g",
                "123",
                "-b",
                "release-R107-15117.B",
                "amd64-generic-full-tryjob",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

        self.assertIsNone(self.cmd_mock.inst.options.buildroot)

    def testMinimalLocal(self) -> None:
        """Test option verification with simplest normal options."""
        self.SetupCommandMock(
            [
                "-g",
                "123",
                "-b",
                "release-R107-15117.B",
                "--local",
                "amd64-generic-full-tryjob",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testMinimalCbuildbot(self) -> None:
        """Test option verification with simplest normal options."""
        self.SetupCommandMock(
            [
                "-b",
                "release-R107-15117.B",
                "--cbuildbot",
                "amd64-generic-full",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testComplexLocalTryjob(self) -> None:
        """Test option verification with complex mix of options."""
        self.SetupCommandMock(
            [
                "--yes",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--local",
                "--buildroot",
                "/buildroot",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--chrome_version",
                "chrome_git_hash",
                "--committer-email",
                "foo@bar",
                "--version",
                "1.2.3",
                "--channel",
                "chan",
                "--pass-through=--cbuild-arg",
                "--pass-through=bar",
                "-b",
                "release-R107-15117.B",
                "amd64-generic-full-tryjob",
                "eve-release-tryjob",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testComplexCbuildbot(self) -> None:
        """Test option verification with complex mix of options."""
        self.SetupCommandMock(
            [
                "--yes",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--cbuildbot",
                "--buildroot",
                "/buildroot",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--committer-email",
                "foo@bar",
                "--version",
                "1.2.3",
                "--channel",
                "chan",
                "--pass-through=--cbuild-arg",
                "--pass-through=bar",
                "-b",
                "release-R107-15117.B",
                "amd64-generic-full",
                "eve-release",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testComplexRemoteTryjob(self) -> None:
        """Test option verification with complex mix of options."""
        self.SetupCommandMock(
            [
                "--swarming",
                "--yes",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--chrome_version",
                "chrome_git_hash",
                "--committer-email",
                "foo@bar",
                "--version",
                "1.2.3",
                "--channel",
                "chan",
                "--pass-through=--cbuild-arg",
                "--pass-through=bar",
                "-b",
                "release-R107-15117.B",
                "amd64-generic-full-tryjob",
                "eve-release-tryjob",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testList(self) -> None:
        """Test option verification with config list behavior."""
        self.SetupCommandMock(
            [
                "--list",
            ]
        )

        with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
            with outcap.OutputCapturer(quiet_fail=True):  # Hide list output.
                cros_tryjob.VerifyOptions(
                    self.cmd_mock.inst.options, self.site_config
                )
        self.assertEqual(cm.exception.code, 0)

    def testListProduction(self) -> None:
        """Test option verification with config list behavior."""
        self.SetupCommandMock(
            [
                "--list",
                "--production",
            ]
        )

        with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
            with outcap.OutputCapturer(quiet_fail=True):  # Hide list output.
                cros_tryjob.VerifyOptions(
                    self.cmd_mock.inst.options, self.site_config
                )
        self.assertEqual(cm.exception.code, 0)

    def testProduction(self) -> None:
        """Test option verification with production/no patches."""
        self.SetupCommandMock(
            [
                "--production",
                "-b",
                "release-R107-15117.B",
                "amd64-generic-full-tryjob",
                "eve-release",
            ]
        )

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testUnknownConfig(self) -> None:
        """Test option verification with production configs on branches."""

        # We have no way of knowing if the config is production or not on a
        # branch, so don't prompt at all
        self.SetupCommandMock(["bogus-config"])

        with self.assertRaises(PromptException):
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )

    def testBranchUnknownConfig(self) -> None:
        """Test option verification with production configs on branches."""

        # We have no way of knowing if the config is production or not on a
        # branch, so don't prompt at all
        self.SetupCommandMock(
            [
                "--branch",
                "old_branch",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "bogus-config",
            ]
        )

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testBranchProductionUnknownConfig(self) -> None:
        """Test option verification with production configs on branches."""

        # We have no way of knowing if the config is production or not on a
        # branch, so don't prompt at all
        self.SetupCommandMock(
            ["--branch", "old_branch", "--production", "bogus-config"]
        )

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testBranchProductionConfigTryjob(self) -> None:
        """Test option verification with production configs on branches."""

        # We have no way of knowing if the config is production or not on a
        # branch, so don't prompt at all
        self.SetupCommandMock(
            [
                "--branch",
                "old_branch",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "eve-release",
            ]
        )

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testProductionPatches(self) -> None:
        """Test option verification with production/patches."""
        self.SetupCommandMock(
            [
                "--production",
                "--gerrit-patches",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "amd64-generic-full-tryjob",
                "eve-release",
            ]
        )

        with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )
        self.assertEqual(cm.exception.code, 1)

    def testRemoteTryjobProductionConfig(self) -> None:
        """Test option verification remote tryjob w/production config."""
        self.SetupCommandMock(["amd64-generic-full-tryjob", "eve-release"])

        with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )
        self.assertEqual(cm.exception.code, 1)

    def testLocalTryjobProductionConfig(self) -> None:
        """Test option verification local tryjob w/production config."""
        self.SetupCommandMock(["--local", "eve-release"])

        with self.assertRaises(cros_build_lib.DieSystemExit) as cm:
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )
        self.assertEqual(cm.exception.code, 1)

    def testRemoteTryjobBranchProductionConfig(self) -> None:
        """Test a tryjob on a branch for a production config w/confirm."""
        self.SetupCommandMock(["--yes", "--branch", "foo", "eve-release"])

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testRemoteProductionBranchProductionConfig(self) -> None:
        """Test a production job on a branch for a prod config wo/confirm."""
        self.SetupCommandMock(
            ["--production", "--branch", "foo", "eve-release"]
        )

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testUnknownBuildYes(self) -> None:
        """Test option using yes to force accepting an unknown config."""
        self.SetupCommandMock(
            [
                "--yes",
                "-b",
                "release-R107-15117.B",
                "-g",
                "123",
                "unknown-config",
            ]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testNoPatchesYes(self) -> None:
        """Test option using yes to force an unknown config, no patches."""
        self.SetupCommandMock(
            ["--yes", "-b", "release-R107-15117.B", "unknown-config"]
        )
        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testUnsupportedReleaseBranch(self) -> None:
        """Test that the tool fails for an unsupported release branch."""
        self.SetupCommandMock(["--branch", "release-R108-15183.B"])

        with self.assertRaises(cros_build_lib.DieSystemExit):
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )

    def test108Release(self) -> None:
        """Test that the tool fails for an unsupported release branch."""
        self.SetupCommandMock(
            ["--branch", "release-R108-15183.B", "eve-release-tryjob"]
        )

        with self.assertRaises(cros_build_lib.DieSystemExit):
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )

    def test108NonRelease(self) -> None:
        """Test that the tool fails for an unsupported release branch."""
        # We have no way of knowing if the config is production or not on a
        # branch, so don't prompt at all
        self.SetupCommandMock(
            [
                "--branch",
                "release-R108-15183.B",
                "--production",
                "chromiumos-sdk-tryjob",
            ]
        )

        cros_tryjob.VerifyOptions(self.cmd_mock.inst.options, self.site_config)

    def testUnsupportedStabilizeBranch(self) -> None:
        """Test that the tool fails for an unsupported stabilize branch."""
        self.SetupCommandMock(["--branch", "stabilize-15183.14.B"])

        with self.assertRaises(cros_build_lib.DieSystemExit):
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )

    def testUnsupportedFirmwareBranch(self) -> None:
        """Test that the tool fails for an unsupported firmware branch."""
        self.SetupCommandMock(["--branch", "firmware-corsola-15194.B"])

        with self.assertRaises(cros_build_lib.DieSystemExit):
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )

    def testUnsupportedToT(self) -> None:
        """Test that the tool fails for ToT."""
        self.SetupCommandMock(["--branch", "main"])

        with self.assertRaises(cros_build_lib.DieSystemExit):
            cros_tryjob.VerifyOptions(
                self.cmd_mock.inst.options, self.site_config
            )


class TryjobTestCbuildbotArgs(TryjobTest):
    """Test cros_tryjob.CbuildbotArgs."""

    def helperOptionsToCbuildbotArgs(self, args_in):
        """Convert cros tryjob arguments -> cbuildbot arguments.

        Does not do all intermediate steps, only for testing CbuildbotArgs.
        """
        self.SetupCommandMock(args_in)
        options = self.cmd_mock.inst.options
        cros_tryjob.TryjobCommand.ProcessOptions(None, options)
        args_out = cros_tryjob.CbuildbotArgs(options)
        return args_out

    def testCbuildbotArgsMinimal(self) -> None:
        args_in = ["foo-build"]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--remote-trybot",
                "-b",
                "main",
            ],
        )

    def testCbuildbotArgsSimpleRemote(self) -> None:
        args_in = ["-g", "123", "foo-build"]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--remote-trybot",
                "-b",
                "main",
                "-g",
                "123",
            ],
        )

    def testCbuildbotArgsSimpleInfraTesting(self) -> None:
        args_in = ["--infra-testing", "-g", "123", "foo-build"]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--remote-trybot",
                "-b",
                "main",
                "-g",
                "123",
            ],
        )

    def testCbuildbotArgsSimpleLocal(self) -> None:
        args_in = [
            "--local",
            "-g",
            "123",
            "foo-build",
        ]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        # Default buildroot changes.
        self.assertEqual(
            args_out,
            [
                "--buildroot",
                mock.ANY,
                "--git-cache-dir",
                mock.ANY,
                "--no-buildbot-tags",
                "--debug",
                "-b",
                "main",
                "-g",
                "123",
            ],
        )

    def testCbuildbotArgsComplexRemote(self) -> None:
        args_in = [
            "--yes",
            "--latest-toolchain",
            "--notests",
            "--novmtests",
            "--noimagetests",
            "--timeout",
            "5",
            "--confidence-check-build",
            "--gerrit-patches",
            "123",
            "-g",
            "*123",
            "-g",
            "123..456",
            "--chrome_version",
            "chrome_git_hash",
            "--committer-email",
            "foo@bar",
            "--branch",
            "source_branch",
            "--version",
            "1.2.3",
            "--channel",
            "chan",
            "--pass-through=--cbuild-arg",
            "--pass-through=bar",
            "eve-release",
        ]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--remote-trybot",
                "-b",
                "source_branch",
                "-g",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--chrome_version",
                "chrome_git_hash",
                "--version",
                "1.2.3",
                "--channel",
                "chan",
                "--cbuild-arg",
                "bar",
            ],
        )

    def testCbuildbotArgsComplexLocal(self) -> None:
        args_in = [
            "--local",
            "--yes",
            "--latest-toolchain",
            "--notests",
            "--novmtests",
            "--noimagetests",
            "--buildroot",
            "/buildroot",
            "--timeout",
            "5",
            "--confidence-check-build",
            "--gerrit-patches",
            "123",
            "-g",
            "*123",
            "-g",
            "123..456",
            "--chrome_version",
            "chrome_git_hash",
            "--committer-email",
            "foo@bar",
            "--branch",
            "source_branch",
            "--version",
            "1.2.3",
            "--channel",
            "chan",
            "--pass-through=--cbuild-arg",
            "--pass-through=bar",
            "eve-release",
        ]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--buildroot",
                "/buildroot",
                "--git-cache-dir",
                "/buildroot/.git_cache",
                "--no-buildbot-tags",
                "--debug",
                "-b",
                "source_branch",
                "-g",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--chrome_version",
                "chrome_git_hash",
                "--version",
                "1.2.3",
                "--channel",
                "chan",
                "--cbuild-arg",
                "bar",
            ],
        )

    def testCbuildbotArgsComplexCbuildbot(self) -> None:
        args_in = [
            "--cbuildbot",
            "--yes",
            "--latest-toolchain",
            "--notests",
            "--novmtests",
            "--noimagetests",
            "--buildroot",
            "/buildroot",
            "--timeout",
            "5",
            "--confidence-check-build",
            "--gerrit-patches",
            "123",
            "-g",
            "*123",
            "-g",
            "123..456",
            "--committer-email",
            "foo@bar",
            "--branch",
            "source_branch",
            "--version",
            "1.2.3",
            "--channel",
            "chan",
            "--pass-through=--cbuild-arg",
            "--pass-through=bar",
            "amd64-generic-full",
            "eve-release",
        ]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--buildroot",
                "/buildroot/repository",
                "--workspace",
                "/buildroot/workspace",
                "--git-cache-dir",
                "/buildroot/.git_cache",
                "--debug",
                "--nobootstrap",
                "--noreexec",
                "--no-buildbot-tags",
                "-b",
                "source_branch",
                "-g",
                "123",
                "-g",
                "*123",
                "-g",
                "123..456",
                "--latest-toolchain",
                "--notests",
                "--novmtests",
                "--noimagetests",
                "--timeout",
                "5",
                "--confidence-check-build",
                "--version",
                "1.2.3",
                "--channel",
                "chan",
                "--cbuild-arg",
                "bar",
            ],
        )

    def testCbuildbotArgsProductionRemote(self) -> None:
        args_in = [
            "--production",
            "foo-build",
        ]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        self.assertEqual(
            args_out,
            [
                "--buildbot",
                "-b",
                "main",
            ],
        )

    def testCbuildbotArgsProductionLocal(self) -> None:
        args_in = [
            "--local",
            "--production",
            "foo-build",
        ]

        args_out = self.helperOptionsToCbuildbotArgs(args_in)

        # Default buildroot changes.
        self.assertEqual(
            args_out,
            [
                "--buildroot",
                mock.ANY,
                "--git-cache-dir",
                mock.ANY,
                "--no-buildbot-tags",
                "--buildbot",
                "-b",
                "main",
            ],
        )


class TryjobTestDisplayLabel(TryjobTest):
    """Test the helper function DisplayLabel."""

    def FindLabel(self, args):
        site_config = config_lib.GetConfig()
        options = self.SetupCommandMock(args)
        config_name = options.build_configs[-1]
        return cros_tryjob.DisplayLabel(site_config, options, config_name)

    def testMainTryjob(self) -> None:
        label = self.FindLabel(["amd64-generic-full-tryjob"])
        self.assertEqual(label, "tryjob")

    def testMainUnknown(self) -> None:
        label = self.FindLabel(["bogus-config"])
        self.assertEqual(label, "tryjob")

    def testMainKnownProduction(self) -> None:
        label = self.FindLabel(["--production", "amd64-generic-full"])
        self.assertEqual(label, "production_tryjob")

    def testMainUnknownProduction(self) -> None:
        label = self.FindLabel(["--production", "bogus-config"])
        self.assertEqual(label, "production_tryjob")
