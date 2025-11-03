from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.utils.path_utils import PathUtils


class CommandLS(AbstractCommand):
    OPTIONS = {
        Option("Показать список файлов в директории", "-l", "--list", False, True),
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Включить в список скрытые файлы", "-a", "--all", False, True)
    }
    DIRECTORY_EMOJI = "🗂"
    FILE_EMOJI = "📄"
    UNEXPECTED_TYPE = "❔"

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the ls command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandLS.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        List directory contents according to provided options.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandLS.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        removed = self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_presence)
        removed += self._remove_if(self.parsed_arguments.position_arguments, PathUtils.check_readable)

        if removed != 0 and len(self.parsed_arguments.position_arguments) == 0:
            return

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                PathUtils.check_presence(context.current_directory)
                PathUtils.check_readable(context.current_directory)
                directory_content = PathUtils.get_directory_content(context.current_directory)
                self._output_content(directory_content, self.parsed_arguments, False)
            case _:
                is_write_path = count_position_arguments != 1
                for path in self.parsed_arguments.position_arguments:
                    current_path = PathUtils.get_resolved_path(Path(path))
                    if Path(current_path).is_file():
                        self.logger.print(current_path.name)
                        continue
                    directory_content = PathUtils.get_directory_content(current_path)
                    self._output_content(directory_content, self.parsed_arguments, is_write_path)


    def _output_content(self, paths: list[Path], parsed_arguments: ParsedArguments, is_write_path_name: bool) -> None:
        """
        Render directory contents based on selected output mode.
        :param paths: Collection of paths to display.
        :type paths: list[Path]
        :param parsed_arguments: Parsed command arguments.
        :type parsed_arguments: ParsedArguments
        :param is_write_path_name: Flag indicating whether to prefix directory names.
        :type is_write_path_name: bool
        :return: None
        :rtype: None
        """
        if AbstractCommand.is_in_parsed_arguments("-l", "--list", parsed_arguments):
            program_output = self._get_ls_output_with_l_option(paths, is_write_path_name)
            self.logger.print(program_output)
        else:
            program_output = self._get_ls_output_without_l_option(paths, is_write_path_name)
            self.logger.print(program_output)

    @staticmethod
    def _get_path_name_with_emoji(path: Path) -> str:
        """
        Represent the path name with an emoji for its type.
        :param path: Path to represent.
        :type path: Path
        :return: String containing emoji and path name.
        :rtype: str
        """
        if path.is_dir():
            return f"{CommandLS.DIRECTORY_EMOJI} {path.name} "
        elif path.is_file():
            return f"{CommandLS.FILE_EMOJI}{path.name} "
        return f"{CommandLS.UNEXPECTED_TYPE}{path.name} "

    def _get_ls_output_without_l_option(self,paths: list[Path], is_write_path_name: bool) -> str:
        """
        Build the ls output string without the long listing format.
        :param paths: Collection of paths to display.
        :type paths: list[Path]
        :param is_write_path_name: Flag indicating whether to prefix directory names.
        :type is_write_path_name: bool
        :return: Concatenated listing output.
        :rtype: str
        """
        result = []
        if is_write_path_name:
            result.append(paths[0].parent.name + ":\n")
        for path in paths:
            if path.name[0] == ".":
                if AbstractCommand.is_in_parsed_arguments("-a", "--all", self.parsed_arguments):
                    result.append(CommandLS._get_path_name_with_emoji(path))
            else:
                result.append(CommandLS._get_path_name_with_emoji(path))
        return "".join(result)

    def _get_ls_output_with_l_option(self, paths: list[Path], is_write_path_name: bool) -> str:
        """
        Build the ls output string with the long listing format.
        :param paths: Collection of paths to display.
        :type paths: list[Path]
        :param is_write_path_name: Flag indicating whether to prefix directory names.
        :type is_write_path_name: bool
        :return: Concatenated long listing output.
        :rtype: str
        """
        result = []

        align_link = AbstractCommand._get_max_length(paths, PathUtils.get_count_links)
        align_owner = AbstractCommand._get_max_length(paths, PathUtils.get_owner)
        align_group = AbstractCommand._get_max_length(paths, PathUtils.get_group)
        align_bytes = AbstractCommand._get_max_length(paths, PathUtils.get_bytes_size)

        if is_write_path_name:
            result.append(paths[0].parent.name + ":\n")

        for path in paths:
            if path.name[0] == ".":
                if AbstractCommand.is_in_parsed_arguments("-a", "--all", self.parsed_arguments):
                    result.append(self._get_formatted_string_for_l_option(path, align_link, align_owner, align_group, align_bytes))
            else:
                result.append(self._get_formatted_string_for_l_option(path, align_link, align_owner, align_group, align_bytes))
        return "".join(result)

    def _get_formatted_string_for_l_option(self,
                                           path: Path,
                                           align_link: int,
                                           align_owner: int,
                                           align_group: int,
                                           align_bytes: int
    ) -> str:
        """
        Format a single entry for the long listing output.
        :param path: Path to format.
        :type path: Path
        :param align_link: Alignment width for link count.
        :type align_link: int
        :param align_owner: Alignment width for owner name.
        :type align_owner: int
        :param align_group: Alignment width for group name.
        :type align_group: int
        :param align_bytes: Alignment width for byte size.
        :type align_bytes: int
        :return: Formatted listing string for the path.
        :rtype: str
        """
        return (
            f"{PathUtils.get_filemode(path)} "
            f"{PathUtils.get_count_links(path):>{align_link}} "
            f"{PathUtils.get_owner(path):>{align_owner}} "
            f"{PathUtils.get_group(path):<{align_group}} "
            f"{PathUtils.get_bytes_size(path):>{align_bytes}} "
            f"{PathUtils.get_last_change_time(path).strftime('%Y-%m-%d %H:%M:%S')} "
            f"{PathUtils.get_path_name(path)} \n"
        )