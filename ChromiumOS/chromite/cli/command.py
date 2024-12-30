# Copyright 2012 The ChromiumOS Authors
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Module that contains meta-logic related to CLI commands.

This module contains two important definitions used by all commands:
    CliCommand: The parent class of all CLI commands.
    command_decorator: Decorator that must be used to ensure that the command
        shows up in |_commands| and is discoverable.

Commands can be either imported directly or looked up using this module's
ListCommands() function.
"""

import abc
import importlib
import logging
import os
import sys
from typing import Any, Callable, Dict, Optional, Type

from chromite.lib import commandline
from chromite.lib import constants
from chromite.lib import cros_build_lib


# Paths for finding and importing subcommand modules.
_SUBCOMMAND_MODULE_DIRECTORY = os.path.join(os.path.dirname(__file__), "cros")
_SUBCOMMAND_MODULE_PREFIX = "cros_"


_commands = {}


def UseProgressBar():
    """Determine whether the progress bar is to be used or not.

    We only want the progress bar to display for the brillo commands which
    operate at logging level NOTICE. If the user wants to see the noisy output,
    then they can execute the command at logging level INFO or DEBUG.
    """
    return logging.getLogger().getEffectiveLevel() == logging.NOTICE


def ImportCommand(name):
    """Directly import the specified subcommand.

    This method imports the module which must contain the single subcommand.
    When the module is loaded, the declared command (those that use
    command_decorator) will automatically get added to |_commands|.

    Args:
        name: The subcommand to load.

    Returns:
        A reference to the subcommand class.
    """
    module_path = os.path.join(
        _SUBCOMMAND_MODULE_DIRECTORY, "cros_%s" % (name.replace("-", "_"),)
    )
    import_path = os.path.relpath(
        os.path.realpath(module_path), constants.CHROMITE_DIR.parent
    )
    module_parts = import_path.split(os.path.sep)
    importlib.import_module(".".join(module_parts))
    return _commands[name]


def ListCommands():
    """Return the set of available subcommands.

    We assume that there is a direct one-to-one relationship between the module
    name on disk and the command that module implements.  We assume this as a
    performance requirement (to avoid importing every subcommand every time even
    though we'd only ever run a single one), and to avoid 3rd party module usage
    in one subcommand breaking all other subcommands (not a great solution).
    """
    # Filenames use underscores due to python naming limitations, but
    # subcommands use dashes as they're easier for humans to type.
    # Strip off the leading "cros_" and the trailing ".py".
    return set(
        x[5:-3].replace("_", "-")
        for x in os.listdir(_SUBCOMMAND_MODULE_DIRECTORY)
        if (
            x.startswith(_SUBCOMMAND_MODULE_PREFIX)
            and x.endswith(".py")
            and not x.endswith("_unittest.py")
        )
    )


class InvalidCommandError(Exception):
    """Error that occurs when command class fails validity checks."""


def command_decorator(name):
    """Decorator to check validity and add class to list of usable commands."""

    def inner_decorator(original_class):
        """Inner Decorator that actually wraps the class."""
        if not hasattr(original_class, "__doc__"):
            raise InvalidCommandError(
                "All handlers must have docstrings: %s" % original_class
            )

        if not issubclass(original_class, CliCommand):
            raise InvalidCommandError(
                "All Commands must derive from CliCommand: %s" % original_class
            )

        _commands[name] = original_class
        original_class.name = name

        return original_class

    return inner_decorator


class CliCommand(abc.ABC):
    """All CLI commands must derive from this class.

    This class provides the abstract interface for all CLI commands. When
    designing a new command, you must sub-class from this class and use the
    command_decorator decorator. You must specify a class docstring as that will
    be used as the usage for the sub-command.

    In addition your command should implement AddParser which is passed in a
    parser that you can add your own custom arguments. See argparse for more
    information.
    """

    # Indicates whether command uses cache related commandline options.
    use_caching_options = False
    # Whether command uses dry-run options.
    use_dryrun_options = False

    # Indicates whether command uses filter related commandline options.
    use_filter_options = False

    def __init__(self, options) -> None:
        self.options = options

    @classmethod
    def AddParser(cls, parser) -> None:
        """Add arguments for this command to the parser."""
        parser.set_defaults(command_class=cls)

    @classmethod
    def ProcessOptions(
        cls,
        parser: commandline.ArgumentParser,
        options: commandline.ArgumentNamespace,
    ) -> None:
        """Validate & post-process options before freezing."""

    @classmethod
    def AddDeviceArgument(
        cls, parser, schemes=commandline.DeviceScheme.SSH, positional=False
    ) -> None:
        """Add a device argument to the parser.

        This standardizes the help message across all subcommands.

        Args:
            parser: The parser to add the device argument to.
            schemes: List of device schemes or single scheme to allow.
            positional: Whether it should be a positional or named argument.
        """
        help_strings = []
        schemes = list(cros_build_lib.iflatten_instance(schemes))
        if commandline.DeviceScheme.SSH in schemes:
            help_strings.append(
                "Target a device with [user@]hostname[:port]. "
                "IPv4/IPv6 addresses are allowed, but IPv6 must "
                "use brackets (e.g. [::1])."
            )
        if commandline.DeviceScheme.USB in schemes:
            help_strings.append("Target removable media with usb://[path].")
        if commandline.DeviceScheme.SERVO in schemes:
            help_strings.append(
                "Target a servo by port or serial number with "
                "servo:port[:port] or servo:serial:serial-number. "
                "e.g. servo:port:1234 or servo:serial:C1230024192."
            )
        if commandline.DeviceScheme.FILE in schemes:
            help_strings.append("Target a local file with file://path.")
        if positional:
            parser.add_argument(
                "device",
                type=commandline.DeviceParser(schemes),
                help=" ".join(help_strings),
            )
        else:
            parser.add_argument(
                "-d",
                "--device",
                type=commandline.DeviceParser(schemes),
                help=" ".join(help_strings),
            )

    @abc.abstractmethod
    def Run(self) -> None:
        """The command to run."""

    def TranslateToChrootArgv(self):
        """Hook to get the argv for reexecution inside the chroot.

        By default, return the same args used to execute it in the first place.
        Hook allows commands to translate specific arguments, i.e. change paths
        to chroot paths.
        """
        return sys.argv[:]


class CommandGroup(CliCommand):
    """Base class to implement a command which exposes many subcommands."""

    # _SUBCOMMANDS is shared amongst child classes.  Maps id(cls) to subcommands
    # for that class.
    _SUBCOMMANDS: Dict[int, Dict[str, Type[CliCommand]]] = {}
    EPILOG = "Run a subcommand with --help for help on specific commands."

    @classmethod
    def subcommand(
        cls, name: str, **kwargs: Any
    ) -> Callable[[Type[CliCommand]], Type[CliCommand]]:
        """Decorator to register a subcommand in this group."""
        cls._SUBCOMMANDS.setdefault(id(cls), {})

        def _decorator(klass):
            if name in cls._SUBCOMMANDS[id(cls)]:
                raise ValueError(f"Subcommand already registered: {name}")
            if not klass.__doc__:
                raise ValueError(f"Subcommand must have a docstring: {name}")
            if not issubclass(klass, CliCommand):
                raise ValueError(
                    f"Subcommand must derive from CliCommand: {name}"
                )
            cls._SUBCOMMANDS[id(cls)][name] = klass
            klass.name = name
            klass.parser_options = kwargs
            return klass

        return _decorator

    @classmethod
    def get_subcommand_class(
        cls, options: commandline.ArgumentNamespace
    ) -> Type[CliCommand]:
        """Get the subcommand class that was selected."""
        # We tag the class id in the subcommand destination as the options
        # namespace is shared amongst all CommandGroups.
        return cls._SUBCOMMANDS.get(id(cls), {})[
            getattr(options, f"_sub_{id(cls)}")
        ]

    @classmethod
    def AddParser(cls, parser: commandline.ArgumentParser) -> None:
        """Add subcommands and options."""
        super(CommandGroup, cls).AddParser(parser)
        subparsers = parser.add_subparsers(
            title="Subcommands",
            dest=f"_sub_{id(cls)}",
            required=True,
            metavar="SUBCOMMAND",
        )

        for name, klass in cls._SUBCOMMANDS.get(id(cls), {}).items():
            sub_parser = subparsers.add_parser(
                name,
                description=klass.__doc__,
                help=klass.__doc__,
                formatter_class=parser.formatter_class,
                **klass.parser_options,
            )
            klass.AddParser(sub_parser)

    @classmethod
    def ProcessOptions(
        cls,
        parser: commandline.ArgumentParser,
        options: commandline.ArgumentNamespace,
    ) -> None:
        """Post-process options."""
        klass = cls.get_subcommand_class(options)
        klass.ProcessOptions(parser, options)

    def Run(self) -> Optional[int]:
        """The main handler of this CLI."""
        klass = self.get_subcommand_class(self.options)
        subcmd = klass(self.options)
        return subcmd.Run()
