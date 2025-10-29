from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.exception.command_exception import NotEnoughArgumentsException
from src.utils.path_utils import PathUtils


class CommandCat(AbstractCommand):
    OPTIONS: set[Option] = set()

    def __init__(self, parser: Parser):
        super().__init__(CommandCat.OPTIONS, parser, ParsedArguments([], set(), {}))

    def execute(self, arguments: InputArguments, context: Context):
        self.parsed_arguments = self.parser.parse(CommandCat.OPTIONS, arguments)
        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                raise NotEnoughArgumentsException()
            case _:
                for path_as_str in self.parsed_arguments.position_arguments:
                    path = Path(path_as_str)
                    PathUtils.check_presence_file(path)
                    print(path.read_text(encoding="utf-8", errors="ignore"), end="")
