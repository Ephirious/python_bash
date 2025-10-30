from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import NotEnoughArgumentsException
from src.utils.path_utils import PathUtils


class CommandCat(AbstractCommand):
    OPTIONS: set[Option] = set()

    def __init__(self, parser: Parser, logger: Logger):
        super().__init__(CommandCat.OPTIONS, parser, logger)

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
                    file_text = path.read_text(encoding="utf-8", errors="ignore")
                    self.logger.print(file_text)
