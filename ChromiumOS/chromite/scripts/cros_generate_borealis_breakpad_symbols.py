# Copyright 2023 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Generate minidump symbols for use by the Crash server.

This script takes debug packages generated by the Borealis Arch build and
converts them to breakpad format.

The debug packages from Arch are generated by adding "options=(debug strip)"
to the PKGBUILD file.  The resulting archive contains:
- split .debug files in usr/lib/debug with a normal filesystem layout
- optional source files in usr/src/debug which will be ignored
- optional text metadata files (eg .PKGINFO, .BUILDINFO) which will be ignored
"""

import logging
import multiprocessing
import os

from chromite.lib import commandline
from chromite.lib import compression_lib
from chromite.lib import osutils
from chromite.lib import parallel
from chromite.scripts import cros_generate_breakpad_symbols


def GenerateBreakpadSymbols(breakpad_dir, symbols_dir):
    """Generate symbols for all binaries in symbols_dir.

    Args:
        breakpad_dir: The full path in which to write out breakpad symbols.
        symbols_dir: The full path to the binaries to process from.

    Returns:
        The number of errors that were encountered.
    """
    osutils.SafeMakedirs(breakpad_dir)
    logging.info("generating breakpad symbols from %s", symbols_dir)

    num_errors = parallel.WrapMultiprocessing(multiprocessing.Value, "i")

    # Now start generating symbols for the discovered elfs.
    with parallel.BackgroundTaskRunner(
        cros_generate_breakpad_symbols.GenerateBreakpadSymbol,
        breakpad_dir=breakpad_dir,
        num_errors=num_errors,
        # Mesa driver libraries fail with "-d".
        dump_syms_args=["-v", "-m"],
    ) as queue:
        for root, _, files in os.walk(symbols_dir):
            for f in files:
                queue.put([os.path.join(root, f)])

    return num_errors.value


def ProcessSymbolsTarball(archive, breakpad_dir, symbols_path) -> None:
    """Extract, process, and upload all symbols in a symbols file.

    Take the symbols file build artifact from an Borealis build, process it
    into breakpad format.

    The symbols files are really expected to be unstripped elf .debug files
    (or libraries).

    Args:
        archive: Name of the tarball to process.
        breakpad_dir: Root directory for writing out breakpad files.
        symbols_path: Relative directory to search for binaries.
    """
    with osutils.TempDir(prefix="extracted-") as extract_dir:
        logging.info("Extracting %s into %s", archive, extract_dir)
        # We are trusting the contents from a security point of view.
        compression_lib.extract_tarball(archive, extract_dir)

        logging.info(
            "Generate breakpad symbols from %s into %s",
            extract_dir,
            breakpad_dir,
        )
        GenerateBreakpadSymbols(
            breakpad_dir, os.path.join(extract_dir, symbols_path)
        )


def get_parser():
    """Returns a command line parser."""
    parser = commandline.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--symbols-file",
        type="str_path",
        required=True,
        help="Tarball containing debug binaries",
    )
    parser.add_argument(
        "--symbols-path",
        default="usr/lib/debug",
        help="Path to search for debug binaries",
    )
    parser.add_argument(
        "--breakpad-dir",
        type="str_path",
        required=True,
        help="Root directory for breakpad symbol files.",
    )
    return parser


def main(argv) -> None:
    """Helper method mostly used for manual testing."""
    parser = get_parser()
    opts = parser.parse_args(argv)
    opts.Freeze()

    ProcessSymbolsTarball(
        opts.symbols_file, opts.breakpad_dir, opts.symbols_path
    )
