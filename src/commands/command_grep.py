import re
from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import (
    NotEnoughArgumentsException, InvalidArgumentsException,
)
from src.utils.path_utils import PathUtils


class CommandGrep(AbstractCommand):
    OPTIONS = {
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Рекурсивный поиск вхождения в каталогах", "-r", "--recursive", False, True),
        Option("Поиск без учёта регистра", "-i", "--ignore-case", False, True),
        Option("Указывается паттерн поиска", "-p", "--pattern", True, False)
    }
    ENCODING_MODE: str = "utf-8"
    ERRORS_MODE: str = "ignore"

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the grep command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandGrep.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        Search for patterns within files using the provided options.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandGrep.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        self._check_pattern_exists()
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_presence)
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_readable)
        self._remove_if_not_exists_recursive_option()

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                raise NotEnoughArgumentsException()
            case _:
                for path_as_str in self.parsed_arguments.position_arguments:
                    path = PathUtils.get_resolved_path(Path(path_as_str))
                    if PathUtils.is_file(path):
                        self._find(path)
                    elif PathUtils.is_directory(path):
                        for file in PathUtils.get_all_files_in_path(path):
                            self._find(file)

    def _check_pattern_exists(self):
        """
        Validate that the supplied pattern is a valid regular expression.
        :return: None
        :rtype: None
        """
        pattern = self._get_options_arguments("-p", "--pattern")
        try:
            re.compile(pattern)
        except re.error:
            raise InvalidArgumentsException(list(pattern))

    def _remove_if_not_exists_recursive_option(self):
        """
        Remove directory arguments when recursive search is disabled.
        :return: None
        :rtype: None
        """
        if not self.is_in_parsed_arguments("-r", "--recursive", self.parsed_arguments):
            removed = list(
                [path_as_str for path_as_str in self.parsed_arguments.position_arguments
                 if PathUtils.is_directory(PathUtils.get_resolved_path(Path(path_as_str)))]
            )
            for removed_path_as_str in removed:
                self.logger.error(f"Not enough option: -r for {removed_path_as_str}")
                self.logger.print(f"Not enough option: -r for {removed_path_as_str}")
                self.parsed_arguments.position_arguments.remove(removed_path_as_str)

    def _find(self, file: Path):
        """
        Search for the configured pattern within the provided file.
        :param file: File path to inspect.
        :type file: Path
        :return: None
        :rtype: None
        """
        pattern = self._get_options_arguments("-p", "--pattern")
        text = file.read_text(CommandGrep.ENCODING_MODE, CommandGrep.ERRORS_MODE)
        found = []
        flag = 0

        if AbstractCommand.is_in_parsed_arguments("-i", "--ignore-case", self.parsed_arguments):
            flag = re.IGNORECASE

        for num, line in enumerate(text.splitlines()):
            if re.search(pattern, line, flags=flag) is not None:
                found.append(f"{num + 1}: {line}")
        if len(found) > 0:
            self.logger.print(f"file: {file}")
            for line in found:
                self.logger.print(line)