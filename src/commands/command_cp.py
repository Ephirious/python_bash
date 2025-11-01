from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.exception.command_exception import (
    NotEnoughArgumentsException,
    NotEnoughOptionException,
    NotTypeFileException,
)
from src.utils.path_utils import PathUtils


class CommandCP(AbstractCommand):
    OPTIONS = {
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Рекурсивное копирование каталога вместе с содержимым", "-r", "--recursive", False, True)
    }

    def __init__(self, parser: Parser, logger: Logger):
        super().__init__(CommandCP.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        self.parsed_arguments = self.parser.parse(CommandCP.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        correct_paths = self.parsed_arguments.position_arguments[:-1]
        self._remove_if(correct_paths, PathUtils.check_presence)
        self._remove_if(correct_paths, PathUtils.check_readable)
        correct_paths.append(self.parsed_arguments.position_arguments[-1])
        self._check_dest(correct_paths[-1])

        count_position_arguments = len(correct_paths)

        match count_position_arguments:
            case 0 | 1:
                raise NotEnoughArgumentsException()
            case 2:
                src = PathUtils.get_resolved_path(Path(correct_paths[0]))
                dest = PathUtils.get_resolved_path(Path(correct_paths[1]))
                self._copy_src_to_dest(src, dest, context)
            case _:
                dest = PathUtils.get_resolved_path(Path(correct_paths[-1]))
                PathUtils.check_presence_directory(Path(dest))

                for path in correct_paths[:-1]:
                    path_src = PathUtils.get_resolved_path(Path(path))
                    self._copy_src_to_dest(path_src, dest, context)


    def _is_recursive_enable(self, parsed_arguments: ParsedArguments) -> bool:
        return self.is_in_parsed_arguments("-r", "--recursive", parsed_arguments)

    def _copy_src_to_dest(self, src: Path, dest: Path, context: Context) -> None:
        if PathUtils.is_file(src):
            if PathUtils.is_directory(dest):
                PathUtils.copy_file(src, dest)
            elif not PathUtils.is_path_exists(dest):
                if str(dest).find("/") != -1:
                    raise NotTypeFileException(str(dest))
                PathUtils.copy_file(src, context.current_directory / dest)
        elif self._is_recursive_enable(self.parsed_arguments):
            PathUtils.copytree(src, dest)
        else:
            raise NotEnoughOptionException("-r")

    def _check_dest(self, dest: str) -> None:
        path = PathUtils.get_resolved_path(Path(dest))
        if PathUtils.is_path_exists(path) and PathUtils.is_directory(path):
            PathUtils.check_writable(path)