from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import (
    NotEnoughArgumentsException,
)
from src.utils.path_utils import PathUtils


class CommandMV(AbstractCommand):
    OPTIONS = {
        Option("Показать список всех опций", "-h", "--help", False, True)
    }

    def __init__(self, parser: Parser, logger: Logger):
        super().__init__(CommandMV.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        self.parsed_arguments = self.parser.parse(CommandMV.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        correct_paths = self.parsed_arguments.position_arguments[:-1]
        self._remove_if(correct_paths, PathUtils.check_presence)
        correct_paths.append(self.parsed_arguments.position_arguments[-1])

        count_position_arguments = len(correct_paths)


        match count_position_arguments:
            case 0 | 1:
                raise NotEnoughArgumentsException()
            case 2:
                src = PathUtils.get_resolved_path(Path(correct_paths[0]))
                dest = PathUtils.get_resolved_path(Path(correct_paths[1]))

                if not PathUtils.is_path_exists(dest):
                    PathUtils.check_writable(context.current_directory)

                PathUtils.move(src, dest)
            case _:
                dest = PathUtils.get_resolved_path(Path(correct_paths[-1]))
                PathUtils.check_presence(dest)
                PathUtils.check_writable(dest)

                for src_as_str in correct_paths[:-1]:
                    src = PathUtils.get_resolved_path(Path(src_as_str))
                    PathUtils.move(src, dest)
