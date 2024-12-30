# Copyright 2023 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""A cros command used to retrieve firmware archives from Google Storage."""

from chromite.cli import command
from chromite.lib import commandline
from chromite.lib.fwbuddy import fwbuddy


@command.command_decorator("fwget")
class FwgetCommand(command.CliCommand):
    """Downloads firmware archives from Google Storage"""

    EPILOG = f"""
ATTENTION: fwget is still under heavy development and not to be relied on for
anything serious. THE API MAY CHANGE AT ANY POINT. YOU HAVE BEEN WARNED.
For questions/concerns/suggestions please create a bug at {fwbuddy.BUG_SUBMIT_URL}

Downloads and extracts the firmware image(s) identified by a given fwbuddy URI
to a local folder.

{fwbuddy.USAGE}

Examples:

    Define an fwbuddy archive using interactive mode and extract its
    contents to the downloads folder.

        cros fwget fwbuddy:// ~/Downloads

    Download and extract the entire contents of the unsigned version
    13606.459.0 Dedede firmware archive to a temporary directory.

        cros fwget fwbuddy://dedede/galtic/13606.459.0/unsigned

    Download and extract the unsigned EC binary for Galtic firmware
    verision 13606.459.0 to the downloads folder.

        cros fwget fwbuddy://dedede/galtic/13606.459.0/unsigned ~/Downloads --chip=ec

    Download and extract both the unsigned serial AP binary and the EC binary
    for Cozmo firmware verision 12574.111.0 to the downloads folder.

        cros fwget fwbuddy://jacuzzi/cozmo/12574.111.0/unsigned/serial ~/Downloads --chip=all
"""

    @classmethod
    def AddParser(cls, parser: commandline.ArgumentParser) -> None:
        """Add parser arguments."""
        super(FwgetCommand, cls).AddParser(parser)
        parser.add_argument(
            "uri",
            help="The fwbuddy URI that identifies the firmware archive. "
            "Input just the fwbuddy header 'fwbuddy://' to enable a user "
            "friendly interactive mode that will guide you through "
            "constructing an fwbuddy URI.",
        )
        parser.add_argument(
            "path",
            type="dir_exists",
            help="The path to the local folder where the firmware archive will "
            "be extracted to.",
        )
        parser.add_argument(
            "--chip",
            help=(
                "Limits the output to only include the specified chip: "
                "{ec|ap|all}"
            ),
        )

    def Run(self) -> None:
        """Downloads the firmware archive and extract its contents to path"""
        # Exits early if chip is defined, but not supported
        chip = (
            fwbuddy.Chip.from_str(self.options.chip)
            if self.options.chip
            else None
        )
        with fwbuddy.FwBuddy(uri=self.options.uri) as f:
            f.download()
            output_dir = self.options.path / f"{f.uri.board}-{f.uri.version}"
            if chip:
                f.extract()
                f.export(chip, output_dir)
            else:
                f.extract(output_dir)
