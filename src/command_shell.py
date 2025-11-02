from pathlib import Path

from src.common.logger import Logger
from src.common.context import Context
from src.common.lexer import Lexer
from src.exception.shell_exception import ShellException
from src.factories.command_factory import AbstractCommandFactory
from src.utils.path_utils import PathUtils


class CommandShell:
    lexer: Lexer
    command_factory: AbstractCommandFactory
    context: Context

    EXIT_COMMAND = "exit"
    TILDA = "~"

    def __init__(self, command_factory: AbstractCommandFactory, lexer: Lexer, logger: Logger):
        self.command_factory = command_factory
        self.lexer = lexer
        self.context = Context()
        self.logger = logger

    def run(self):
        self._start_shell_loop()

    def _start_shell_loop(self):
        while True:
            formatted_current_directory = "➜ " + self._get_path_to_cwd(str(self.context.current_directory)) + " "
            user_input = input(formatted_current_directory)
            if user_input == "":
                continue

            lexed_arguments = self.lexer.lexing(user_input)
            self._replace_tilda(lexed_arguments.get_arguments())

            if lexed_arguments.get_command() == self.EXIT_COMMAND:
                break

            try:
                self.logger.info(user_input)
                command = self.command_factory.create_command(lexed_arguments.get_command())
                self._write_history(self.context.HISTORY_PATH, user_input)
                command.execute(lexed_arguments, self.context)
            except ShellException as exception:
                self.logger.print(exception.message)
                self.logger.error(exception.message)
            except Exception as exception:
                self.logger.print(str(exception))
                self.logger.error(str(exception))


    def _replace_tilda(self, lexed_arguments: list[str]) -> None:
        for i in range(len(lexed_arguments)):
            if lexed_arguments[i][0] == CommandShell.TILDA:
                lexed_arguments[i] = lexed_arguments[i].replace(CommandShell.TILDA, str(self.context.HOME))

    def _get_path_to_cwd(self, path_as_str: str) -> str:
        return path_as_str.replace(str(self.context.HOME), CommandShell.TILDA)

    def _write_history(self, path: Path, line: str) -> None:
        filemode = "a"
        input_arguments = self.lexer.lexing(line)
        arguments = input_arguments.get_arguments()
        for i in range(len(arguments)):
            cur_path = PathUtils.get_resolved_path(Path(arguments[i]))
            if PathUtils.is_path_exists(cur_path):
                arguments[i] = str(cur_path)
        with open(path, filemode) as file:
            file.write(f"{input_arguments.get_command()} {" ".join(input_arguments.get_arguments())}\n")
