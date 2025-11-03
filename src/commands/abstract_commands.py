from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable

from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.exception.command_exception import (
    NotEnoughOptionException,
)
from src.exception.shell_exception import ShellException
from src.utils.path_utils import PathUtils


class AbstractCommand(ABC):
    available_options: set[Option]
    parser: Parser
    parsed_arguments: ParsedArguments
    logger: Logger

    def __init__(self, options: set[Option], parser: Parser, logger: Logger):
        """
        Initialize the command with available options, parser, and logger.
        :param options: Supported options for the command.
        :type options: set[Option]
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for messaging.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        self.available_options = options
        self.parser = parser
        self.parsed_arguments = ParsedArguments([], set(), {})
        self.logger = logger

    @abstractmethod
    def execute(self, arguments: InputArguments, context: Context):
        """
        Execute the command using the provided arguments and context.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Execution context of the shell.
        :type context: Context
        :return: None
        :rtype: None
        """
        pass

    def output_help_if_need(self) -> bool:
        """
        Print command help when the help option is present.
        :return: Flag indicating whether help was displayed.
        :rtype: bool
        """
        if not AbstractCommand.is_in_parsed_arguments("-h", "--help", self.parsed_arguments):
            return False

        long_names = [option.get_full_name() for option in self.available_options]
        long_names.append("LONG NAME")
        align_for_long_names = AbstractCommand._get_max_length(long_names, lambda x: x)

        result = (
            f"SHORT_NAME "
            f"{"LONG_NAME":<{align_for_long_names}} "
            f"REQUIRED_ARGUMENT "
            f"REPEATABLE "
            f"DESCRIPTION\n"
        )
        for option in self.available_options:
            result += (
                f"{option.get_short_name():<{len("SHORT NAME")}} "
                f"{option.get_full_name():<{align_for_long_names}} "
                f"{str(option.is_required_argument()):<{len("REQUIRED ARGUMENT")}} "
                f"{str(option.is_repeatable()):<{len("REPEATABLE")}} "
                f"{option.get_description()} \n"
            )
        self.logger.print(result[:-1])
        return True

    @staticmethod
    def is_in_parsed_arguments(option_short: str, option_long: str, parsed_arguments: ParsedArguments) -> bool:
        """
        Determine whether an option is present in parsed arguments.
        :param option_short: Short option name to inspect.
        :type option_short: str
        :param option_long: Long option name to inspect.
        :type option_long: str
        :param parsed_arguments: Parsed arguments to search.
        :type parsed_arguments: ParsedArguments
        :return: Flag indicating if the option exists in parsed arguments.
        :rtype: bool
        """
        return (option_short in parsed_arguments.options_with_argument or
                option_short in parsed_arguments.options_without_argument or
                option_long in parsed_arguments.options_without_argument or
                option_long in parsed_arguments.options_with_argument)

    @staticmethod
    def _get_max_length(objects: list[Any], method: Callable[[Any], Any]) -> int:
        """
        Determine the maximum string length produced by applying a method.
        :param objects: Objects to measure.
        :type objects: list[Any]
        :param method: Callable extracting comparable value.
        :type method: Callable[[Any], Any]
        :return: Maximum length of the resulting strings.
        :rtype: int
        """
        return max(
            [len(str(method(obj))) for obj in objects]
        )

    def _get_options_arguments(self, short_name: str, long_name: str) -> str:
        """
        Retrieve the argument associated with an option.
        :param short_name: Short option name.
        :type short_name: str
        :param long_name: Long option name.
        :type long_name: str
        :return: Argument associated with the option.
        :rtype: str
        """
        if short_name in self.parsed_arguments.options_with_argument:
            return self.parsed_arguments.options_with_argument[short_name]
        elif long_name in self.parsed_arguments.options_with_argument:
            return self.parsed_arguments.options_with_argument[long_name]
        raise NotEnoughOptionException(short_name)

    def _remove_if(self, paths: list[str], path_utils_func: Callable[[Path], Any]) -> int:
        """
        Remove paths that trigger an exception during validation.
        :param paths: Collection of path strings to filter.
        :type paths: list[str]
        :param path_utils_func: Callable applying validation to each path.
        :type path_utils_func: Callable[[Path], Any]
        :return: Count of removed paths.
        :rtype: int
        """
        removed_paths = []
        for path_as_str in paths:
            path = PathUtils.get_resolved_path(Path(path_as_str))
            try:
                path_utils_func(path)
            except ShellException as exception:
                removed_paths.append(path_as_str)
                self.logger.print(exception.message)
                self.logger.error(exception.message)
        removed = len(removed_paths)
        for removed_path in removed_paths:
            paths.remove(removed_path)
        return removed

    def _remove_if2(self, paths: list[str], predicate: Callable[[Any], bool], message: str = "") -> int:
        removed_paths = []
        for path_as_str in paths:
            path = PathUtils.get_resolved_path(Path(path_as_str))
            if predicate(path):
                removed_paths.append(path_as_str)
                if message != "":
                    self.logger.print(message)
                    self.logger.error(message)
        removed = len(removed_paths)
        for removed_path in removed_paths:
            paths.remove(removed_path)
        return removed