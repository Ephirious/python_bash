from abc import ABC, abstractmethod
from typing import Any, Callable

from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser


class AbstractCommand(ABC):
    available_options: set[Option]
    parser: Parser
    parsed_arguments: ParsedArguments

    def __init__(self, options: set[Option], parser: Parser, parsed_arguments: ParsedArguments):
        self.available_options = options
        self.parser = parser
        self.parsed_arguments = parsed_arguments

    @abstractmethod
    def execute(self, arguments: InputArguments, context: Context):
        pass

    def output_help(self):
        long_names = [option.get_full_name() for option in self.available_options]
        long_names.append("LONG NAME")
        aging_for_long_names = AbstractCommand._get_max_length(long_names, lambda x: x)

        result = (
            f"SHORT_NAME "
            f"{"LONG_NAME":<{aging_for_long_names}} "
            f"REQUIRED_ARGUMENT "
            f"REPEATABLE "
            f"DESCRIPTION\n"
        )
        for option in self.available_options:
            result += (
                f"{option.get_short_name():<{len("SHORT NAME")}} "
                f"{option.get_full_name():<{aging_for_long_names}} "
                f"{str(option.is_required_argument()):<{len("REQUIRED ARGUMENT")}} "
                f"{str(option.is_repeatable()):<{len("REPEATABLE")}} "
                f"{option.get_description()} \n"
            )
        print(result[:-1])

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