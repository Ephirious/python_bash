from pathlib import Path

from src.commands.abstract_commands import AbstractCommand
from src.commands.command_mv import CommandMV
from src.commands.command_rm import CommandRM
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.common.parser import Parser
from src.exception.command_exception import UnexpectedArgumentsException
from src.exception.shell_exception import ShellException
from src.utils.path_utils import PathUtils


class CommandUndo(AbstractCommand):
    OPTIONS: set[Option] = {
        Option("Показать список всех опций", "-h", "--help", False, True)
    }

    def __init__(self, parser: Parser, logger: Logger):
        """
        Initialize the undo command with parser and logger.
        :param parser: Parser used to analyze command arguments.
        :type parser: Parser
        :param logger: Logger instance for output.
        :type logger: Logger
        :return: None
        :rtype: None
        """
        super().__init__(CommandUndo.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        """
        Revert the last file-manipulation command recorded in history.
        :param arguments: Parsed command arguments.
        :type arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        self.parsed_arguments = self.parser.parse(CommandUndo.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                found = self._find_last_command(context)

                if found[0] == -1:
                    self.logger.print("Not found next commands: rm, cp, mv")
                    self.logger.error("Not found next commands: rm, cp, mv")
                    return
                self._undo(found, context)

            case _:
                raise UnexpectedArgumentsException(self.parsed_arguments.position_arguments)

    def _find_last_command(self, context) -> tuple[int, str, list[str]]:
        """
        Locate the most recent rm, cp, or mv command in history.
        :param context: Shell execution context.
        :type context: Context
        :return: Tuple containing entry index, command name, and arguments.
        :rtype: tuple[int, str, list[str]]
        """
        filemode = "r"
        number = 0

        with open(context.HISTORY_PATH, filemode) as file:
            for line in file.readlines()[::-1]:
                number += 1
                split_line = line.split()
                if split_line[0] in ("rm", "cp", "mv"):
                    return number, split_line[0], split_line[1:]
        return -1, "", list()

    def _undo(self, command_as_str: tuple[int, str, list[str]], context: Context):
        """
        Perform undo logic for the provided history command entry.
        :param command_as_str: Tuple with index, command name, and arguments.
        :type command_as_str: tuple[int, str, list[str]]
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        number_command = command_as_str[0]
        command = command_as_str[1]
        arguments = command_as_str[2]
        input_arguments = InputArguments(command, arguments)

        match command:
            case "rm":
                self._undo_rm(input_arguments, context)
            case "mv":
                self._undo_mv(input_arguments, context)
            case "cp":
                self._undo_cp(input_arguments, context)

        self._remove_entry(number_command, context)


    def _remove_entry(self, number: int, context: Context):
        """
        Remove a history entry by its sequential number.
        :param number: Entry number to remove.
        :type number: int
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        valid_entries = []
        with open(context.HISTORY_PATH, "r") as file:
            for num, line in enumerate(file.readlines()):
                if number == num + 1:
                    continue
                valid_entries.append(line)
        with open(context.HISTORY_PATH, "w") as file:
            file.writelines(valid_entries)

    def _log_if_command_was_invalid(self, command):
        """
        Log that the referenced command could not be replayed.
        :param command: Command name that failed to replay.
        :type command: str
        :return: None
        :rtype: None
        """
        self.logger.print(f"Last {command} command was invalid")
        self.logger.error(f"Last {command} command was invalid")

    def _log_if_command_called_with_help(self, command):
        """
        Log that the referenced command was invoked with help flags.
        :param command: Command name associated with help invocation.
        :type command: str
        :return: None
        :rtype: None
        """
        self.logger.print(f"Last {command} command was called with flag -h or --help")
        self.logger.error(f"Last {command} command was called with flag -h or --help")

    def _log_if_file_not_found_in_trash(self, filename: str):
        """
        Log that the expected file was not found in the trash directory.
        :param filename: Name of the missing file.
        :type filename: str
        :return: None
        :rtype: None
        """
        self.logger.print(f"This file or directory not found in the .trash directory: {filename}")
        self.logger.error(f"This file or directory not found in the .trash directory: {filename}")

    def _log_if_file_already_exists(self, filename: str, parent: Path):
        """
        Log that the undo operation cannot proceed because a file exists.
        :param filename: Name of the conflicting file.
        :type filename: str
        :param parent: Parent directory where the conflict occurred.
        :type parent: Path
        :return: None
        :rtype: None
        """
        self.logger.print(f"Can't undo rm operation for {filename}, cause it already exists: in {parent}")
        self.logger.error(f"Can't undo rm operation for {filename}, cause it already exists: in {parent}")

    def _undo_rm(self, input_arguments: InputArguments, context: Context):
        """
        Undo the effects of the last rm command.
        :param input_arguments: Arguments from the rm command.
        :type input_arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        parsed_for_rm = ParsedArguments([], set(), {})
        try:
            parsed_for_rm = self.parser.parse(CommandRM.OPTIONS, input_arguments)
        except ShellException:
            self._log_if_command_was_invalid("rm")
            return

        if self.is_in_parsed_arguments("-h", "--help", parsed_for_rm):
            self._log_if_command_called_with_help("rm")
            return

        for path_as_str in parsed_for_rm.position_arguments:
            path = PathUtils.get_resolved_path(Path(path_as_str))
            parent = path.parent
            name = path.name

            if PathUtils.is_path_exists(parent):
                path_in_trash = context.TRASH_DIR_PATH / name
                if not PathUtils.is_path_exists(path_in_trash):
                    self._log_if_file_not_found_in_trash(name)
                    return
                elif PathUtils.is_path_exists(path):
                    self._log_if_file_already_exists(name, parent)
                    return
                else:
                    PathUtils.move(path_in_trash, parent)

    def _undo_mv(self, input_arguments: InputArguments, context: Context):
        """
        Undo the effects of the last mv command.
        :param input_arguments: Arguments from the mv command.
        :type input_arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        parsed_for_mv = ParsedArguments([], set(), {})
        try:
            parsed_for_mv = self.parser.parse(CommandMV.OPTIONS, input_arguments)
        except ShellException:
            self._log_if_command_was_invalid("mv")
            return

        if self.is_in_parsed_arguments("-h", "--help", parsed_for_mv):
            self._log_if_command_called_with_help("mv")
            return

        count_position_arguments = len(parsed_for_mv.position_arguments)

        match count_position_arguments:
            case 2:
                src = Path(parsed_for_mv.position_arguments[0])
                dest = Path(parsed_for_mv.position_arguments[1])
                if str(dest)[0] != "/":
                    if PathUtils.is_path_exists(src.parent):
                        PathUtils.move(src.parent / dest, src.parent / src.name)
                    else:
                        self._log_if_command_was_invalid("mv")
                elif str(dest)[0] == "/" and str(src)[0] == "/":
                    PathUtils.move(dest / src.name, src.parent / src.name)
                else:
                    self._log_if_command_was_invalid("mv")
            case _:
                dest = Path(parsed_for_mv.position_arguments[-1])
                if str(dest)[0] != "/":
                    self._log_if_command_was_invalid("mv")
                    return
                for path_as_str in parsed_for_mv.position_arguments[:-1]:
                    if path_as_str[0] == "/":
                        src = Path(path_as_str)
                        PathUtils.move(dest / src.name, src.parent / src.name)

    def _undo_cp(self, input_arguments: InputArguments, context: Context):
        """
        Undo the effects of the last cp command.
        :param input_arguments: Arguments from the cp command.
        :type input_arguments: InputArguments
        :param context: Shell execution context.
        :type context: Context
        :return: None
        :rtype: None
        """
        parsed_for_cp = ParsedArguments([], set(), {})
        try:
            parsed_for_cp = self.parser.parse(CommandMV.OPTIONS, input_arguments)
        except ShellException:
            self._log_if_command_was_invalid("cp")
            return

        if self.is_in_parsed_arguments("-h", "--help", parsed_for_cp):
            self._log_if_command_called_with_help("cp")
            return

        self._remove_if2(parsed_for_cp.position_arguments, lambda x: not PathUtils.is_path_exists(x))

        count_position_arguments = len(parsed_for_cp.position_arguments)

        match count_position_arguments:
            case 0 | 1:
                self._log_if_command_was_invalid("cp")
            case _:
                parsed_for_cp.options_without_argument.add("-r")
                command_rm = CommandRM(self.parser, self.logger)
                dest = Path(parsed_for_cp.position_arguments[-1])
                new_paths = list([str(dest / Path(x).name) for x in parsed_for_cp.position_arguments[:-1]])
                new_input_arguments = InputArguments("rm", new_paths)
                command_rm.execute(new_input_arguments, context)
