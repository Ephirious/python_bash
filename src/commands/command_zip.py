from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import (
    NotEnoughOptionException,
    UnexpectedArgumentsException,
    NotEnoughArgumentsException,
)
from src.utils.path_utils import PathUtils


class CommandZIP(AbstractCommand):
    OPTIONS = {
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Создать архив", "-c", "--create", False, False),
        Option("Разархивировать архив", "-x", "--extract", False, False),
        Option("Указывает имя создаваемого архива", "-f", "--file", True, False),
    }

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the zip command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandZIP.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        Create or extract zip archives based on provided options.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandZIP.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_presence)
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_readable)

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                if self._is_extract_situation():
                    PathUtils.check_writable(context.current_directory)
                    self._if_extract_situation()
                else:
                    raise NotEnoughArgumentsException()
            case _:
                if self._is_create_situation():
                    self._if_create_situation()
                elif self._is_extract_situation():
                    raise UnexpectedArgumentsException(self.parsed_arguments.position_arguments)


    def _if_create_situation(self):
        """
        Handle archive creation when requested by options.
        :return: None
        :rtype: None
        """
        added_files = list(
            [PathUtils.get_resolved_path(Path(file)) for file in self.parsed_arguments.position_arguments]
        )
        archive_name = self._get_options_arguments("-f", "--file")
        PathUtils.create_zip_archive(archive_name, added_files)

    def _if_extract_situation(self):
        """
        Handle archive extraction when requested by options.
        :return: None
        :rtype: None
        """
        archive_name = self._get_options_arguments("-f", "--file")
        PathUtils.unzip_archive(archive_name)

    def _is_create_situation(self) -> bool:
        """
        Determine whether arguments request archive creation.
        :return: Flag indicating archive creation mode.
        :rtype: bool
        """
        if AbstractCommand.is_in_parsed_arguments("-c", "--create", self.parsed_arguments):
            if AbstractCommand.is_in_parsed_arguments("-x", "--extract", self.parsed_arguments):
                raise UnexpectedArgumentsException(["-x", "--extract"])
            if not AbstractCommand.is_in_parsed_arguments("-f", "--file", self.parsed_arguments):
                raise NotEnoughOptionException("-f")
            return True
        return False

    def _is_extract_situation(self) -> bool:
        """
        Determine whether arguments request archive extraction.
        :return: Flag indicating archive extraction mode.
        :rtype: bool
        """
        if AbstractCommand.is_in_parsed_arguments("-x", "--extract", self.parsed_arguments):
            if AbstractCommand.is_in_parsed_arguments("-c", "--create", self.parsed_arguments):
                raise UnexpectedArgumentsException(["-c", "--create"])
            if not AbstractCommand.is_in_parsed_arguments("-f", "--file", self.parsed_arguments):
                raise NotEnoughOptionException("-f")
            return True
        return False