#!/usr/bin/env python3
# Copyright 2016 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Wrapper around chromite executable scripts that use virtualenv."""

import os
import subprocess
import sys


try:
    import pytest  # pylint: disable=import-error

    wrapper3 = pytest.importorskip(
        "wrapper3", reason="File must be run in venv"
    )
except ImportError:
    import wrapper3

_CHROMITE_DIR = os.path.realpath(
    os.path.join(os.path.abspath(__file__), "..", "..")
)

# _VIRTUALENV_DIR contains the scripts for working with venvs
_VIRTUALENV_DIR = os.path.join(_CHROMITE_DIR, "..", "infra_virtualenv")
_CREATE_VENV_PATH = os.path.join(_VIRTUALENV_DIR, "bin", "create_venv3")
_REQUIREMENTS = os.path.join(_CHROMITE_DIR, "venv", "requirements.txt")

_VENV_MARKER = "INSIDE_CHROMITE_VENV"


def main() -> None:
    if _IsInsideVenv(os.environ):
        # Don't bleed the marker into children processes that might use the
        # wrapper themselves to run inside of the virtualenv.
        os.environ.pop(_VENV_MARKER)
        wrapper3.DoMain()
    else:
        venvdir = _CreateVenv()
        _ExecInVenv(venvdir, sys.argv)


def _CreateVenv():
    """Create or update chromite venv."""
    result = subprocess.run(
        [_CREATE_VENV_PATH, _REQUIREMENTS],
        check=False,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )
    if result.returncode:
        print(
            f'{os.path.basename(sys.argv[0])}: error: {" ".join(result.args)}: '
            f"exited {result.returncode}",
            file=sys.stderr,
        )
        sys.exit(result.returncode)
    return result.stdout.strip()


def _ExecInVenv(venvdir, args) -> None:
    """Exec command in chromite venv.

    Args:
        venvdir: virtualenv directory
        args: Sequence of arguments.
    """
    venv_python = os.path.join(venvdir, "bin", "python")
    os.execve(
        venv_python,
        [venv_python] + list(args),
        _CreateVenvEnvironment(os.environ),
    )


def _CreateVenvEnvironment(env_dict):
    """Create environment for a virtualenv.

    This adds a special marker variable to a copy of the input environment dict
    and returns the copy.

    Args:
        env_dict: Environment variable dict to use as base, which is not
            modified.

    Returns:
        New environment dict for a virtualenv.
    """
    new_env_dict = env_dict.copy()
    new_env_dict[_VENV_MARKER] = "1"
    new_env_dict.pop("PYTHONPATH", None)
    return new_env_dict


def _IsInsideVenv(env_dict):
    """Return whether the environment dict is running inside a virtualenv.

    This checks the environment dict for the special marker added by
    _CreateVenvEnvironment().

    Args:
        env_dict: Environment variable dict to check

    Returns:
        A true value if inside virtualenv, else a false value.
    """
    # Checking sys.prefix or doing any kind of path check is unreliable because
    # we check out chromite to weird places.
    return env_dict.get(_VENV_MARKER, "")


if __name__ == "__main__":
    main()
