import os
from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import UnexpectedArgumentsException
from src.utils.path_utils import PathUtils


class CommandCD(AbstractCommand):
    OPTIONS: set[Option] = {
        Option("Показать список всех опций", "-h", "--help", False, True)
    }
    TILDA = "~"

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the cd command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandCD.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        Change the current working directory based on provided path.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandCD.OPTIONS, arguments)
        if self.output_help_if_need():
            return
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
                    PathUtils.check_presence(new_path)
                    context.current_directory = new_path.absolute()
                    os.chdir(new_path)
            case _:
                raise UnexpectedArgumentsException(self.parsed_arguments.position_arguments[1:])
