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
    OPTIONS: set[Option] = {
        Option("Показать список всех опций", "-h", "--help", False, True)
    }
    ENCODING_MODE: str = "utf-8"
    ERRORS_MODE: str = "ignore"

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the cat command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandCat.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        Output the contents of the provided files to standard output.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandCat.OPTIONS, arguments)
        if self.output_help_if_need():
            return
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_presence_file)
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_readable)

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                raise NotEnoughArgumentsException()
            case _:
                for path_as_str in self.parsed_arguments.position_arguments:
                    path = Path(path_as_str)
                    file_text = path.read_text(encoding=CommandCat.ENCODING_MODE, errors=CommandCat.ERRORS_MODE)
                    self.logger.print(file_text)
