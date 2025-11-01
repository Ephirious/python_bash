from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable

from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.exception.shell_exception import ShellException
from src.utils.path_utils import PathUtils


class AbstractCommand(ABC):
    available_options: set[Option]
    parser: Parser
    parsed_arguments: ParsedArguments
    logger: Logger

    def __init__(self, options: set[Option], parser: Parser, logger: Logger):
        self.available_options = options
        self.parser = parser
        self.parsed_arguments = ParsedArguments([], set(), {})
        self.logger = logger

    @abstractmethod
    def execute(self, arguments: InputArguments, context: Context):
        pass

    def output_help_if_need(self) -> bool:
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
        self.logger.info(result[:-1])
        self.logger.print(result[:-1])
        return True

    @staticmethod
    def is_in_parsed_arguments(option_short: str, option_long: str, parsed_arguments: ParsedArguments) -> bool:
        return (option_short in parsed_arguments.options_with_argument or
                option_short in parsed_arguments.options_without_argument or
                option_long in parsed_arguments.options_without_argument or
                option_long in parsed_arguments.options_with_argument)

    @staticmethod
    def _get_max_length(objects: list[Any], method: Callable[[Any], Any]) -> int:
        return max(
            [len(str(method(obj))) for obj in objects]
        )

    def _remove_if(self, paths: list[str], path_utils_func: Callable[[Path], Any]) -> int:
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