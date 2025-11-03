from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import (
    NotEnoughOptionException,
    NotEnoughArgumentsException,
)
from src.utils.path_utils import PathUtils


class CommandRM(AbstractCommand):
    OPTIONS = {
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Рекурсивное удаление каталога вместе с содержимым", "-r", "--recursive", False, True),
    }
    NEGATIVE_ANSWER = "n"
    POSITIVE_ANSWER = "y"

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the rm command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandRM.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        Remove files or directories by moving them to the trash directory.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandRM.OPTIONS, arguments)
        if self.output_help_if_need():
            return
        CommandRM._create_trash(context.TRASH_DIR_PATH)
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_presence)
        self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_root_directory)
        self._remove_directions_if_r_not_exist()

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                raise NotEnoughArgumentsException()
            case _:
                if self._ask_user() == CommandRM.NEGATIVE_ANSWER:
                    return

                for path_as_str in self.parsed_arguments.position_arguments:
                    path = PathUtils.get_resolved_path(Path(path_as_str))
                    if PathUtils.is_path_exists(context.TRASH_DIR_PATH / path.name):
                        PathUtils.remove(context.TRASH_DIR_PATH / path.name)
                    PathUtils.move(path, context.HOME / Context.TRASH_DIR_PATH)

    @staticmethod
    def _create_trash(path: Path) -> None:
        """
        Ensure that the trash directory exists.
        :param path: Path to the trash directory.
        :type path: Path
        :return: None
        :rtype: None
        """
        PathUtils.mkdir(path, True)

    def _remove_directions_if_r_not_exist(self) -> int:
        """
        Remove directory paths when recursive removal is not requested.
        :return: Count of removed directory paths.
        :rtype: int
        """
        if not AbstractCommand.is_in_parsed_arguments("-r", "--recursive", self.parsed_arguments):
            removed_paths = []
            for path_as_str in self.parsed_arguments.position_arguments:
                path = PathUtils.get_resolved_path(Path(path_as_str))
                if PathUtils.is_directory(path):
                    removed_paths.append(path_as_str)
                    exception_message = NotEnoughOptionException.MESSAGE + f"-r for {str(path)}"
                    self.logger.print(exception_message)
                    self.logger.error(exception_message)
            for removed_path_as_str in removed_paths:
                self.parsed_arguments.position_arguments.remove(removed_path_as_str)
            return len(removed_paths)
        return 0

    def _ask_user(self) -> str:
        """
        Request confirmation from the user before removing paths.
        :return: User confirmation answer.
        :rtype: str
        """
        while True:
            user_answer = input("Do you really want to remove the trash? [y/n]: ")
            if user_answer.lower() == "y" or user_answer.lower() == "n":
                return user_answer