import os
from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.exception.command_exception import UnexpectedArguments
from src.utils.path_utils import PathUtils


class CommandCD(AbstractCommand):
    OPTIONS: set[Option] = set()
    TILDA = "~"

    def __init__(self, parser: Parser):
        super().__init__(CommandCD.OPTIONS, parser, ParsedArguments([], set(), {}))

    def execute(self, arguments: InputArguments, context: Context):
        self.parsed_arguments = self.parser.parse(CommandCD.OPTIONS, arguments)
        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                context.current_directory = context.HOME
                os.chdir(context.HOME)
            case 1:
                user_input = self.parsed_arguments.position_arguments[0]
                if user_input == CommandCD.TILDA:
                    context.current_directory = context.HOME
                    os.chdir(context.HOME)
                else:
                    new_path = PathUtils.get_resolved_path(Path(user_input))
                    context.current_directory = new_path.absolute()
                    os.chdir(new_path)
            case _:
                raise UnexpectedArguments(self.parsed_arguments.position_arguments[1:])
