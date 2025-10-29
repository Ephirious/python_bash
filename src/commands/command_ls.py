from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.utils.path_utils import PathUtils


class CommandLS(AbstractCommand):
    parsed_arguments: ParsedArguments

    OPTIONS = {
        Option("Показать список файлов в директории", "-l", "--list", False, True),
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Включить в список скрытые файлы", "-a", "--all", False, True)
    }
    DIRECTORY_EMOJI = "🗂"
    FILE_EMOJI = "📄"
    UNEXPECTED_TYPE = "❔"

    def __init__(self, parser: Parser):
        super().__init__(CommandLS.OPTIONS, parser, ParsedArguments([], set(), {}))

    def execute(self, arguments: InputArguments, context: Context):
        self.parsed_arguments = self.parser.parse(CommandLS.OPTIONS, arguments)
        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                PathUtils.check_presence_directory(context.current_directory)
                directory = PathUtils.get_directory_content(context.current_directory)
                self._output_content(directory, self.parsed_arguments, False)
            case 1:
                user_path = PathUtils.get_resolved_path(Path(self.parsed_arguments.position_arguments[0]))
                directory = PathUtils.get_directory_content(user_path)
                self._output_content(directory, self.parsed_arguments, False)
            case _:
                for path in self.parsed_arguments.position_arguments:
                    current_path = PathUtils.get_resolved_path(Path(path))
                    directory = PathUtils.get_directory_content(current_path)
                    self._output_content(directory, self.parsed_arguments, True)


    def _output_content(self, paths: list[Path], parsed_arguments: ParsedArguments, is_write_path_name: bool) -> None:
        if AbstractCommand.is_in_parsed_arguments("-h", "--help", parsed_arguments):
            self.output_help()
        elif self.is_in_parsed_arguments("-l", "--list", parsed_arguments):
            print(self._get_ls_output_with_l_option(paths, is_write_path_name))
        else:
            print(self._get_ls_output_without_l_option(paths, is_write_path_name))

    @staticmethod
    def _get_path_name_with_emoji(path: Path) -> str:
        if path.is_dir():
            return f"{CommandLS.DIRECTORY_EMOJI} {path.name} "
        elif path.is_file():
            return f"{CommandLS.FILE_EMOJI}{path.name} "
        return f"{CommandLS.UNEXPECTED_TYPE}{path.name} "

    def _get_ls_output_without_l_option(self,paths: list[Path], is_write_path_name: bool) -> str:
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
        return (
            f"{PathUtils.get_filemode(path)} "
            f"{PathUtils.get_count_links(path):>{align_link}} "
            f"{PathUtils.get_owner(path):>{align_owner}} "
            f"{PathUtils.get_group(path):<{align_group}} "
            f"{PathUtils.get_bytes_size(path):>{align_bytes}} "
            f"{PathUtils.get_last_change_time(path).strftime('%Y-%m-%d %H:%M:%S')} "
            f"{PathUtils.get_path_name(path)} \n"
        )