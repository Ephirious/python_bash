
from src.common.context import Context
from src.common.lexer import Lexer
from src.exception.shell_exception import ShellException
from src.factories.command_factory import AbstractCommandFactory


class CommandShell:
    lexer: Lexer
    command_factory: AbstractCommandFactory
    context: Context

    EXIT_COMMAND = "exit"
    TILDA = "~"

    def __init__(self, command_factory: AbstractCommandFactory, lexer: Lexer):
        self.command_factory = command_factory
        self.lexer = lexer
        self.context = Context()


    def run(self):
        self._start_shell_loop()

    def _start_shell_loop(self):
        while True:
            formatted_current_directory = "➜ " + self._get_path_to_cwd(str(self.context.current_directory)) + " "
            user_input = input(formatted_current_directory)
            lexed_arguments = self.lexer.lexing(user_input)
            self._replace_tilda(lexed_arguments.get_arguments())

            if lexed_arguments.get_command() == self.EXIT_COMMAND:
                break

            try:
                command = self.command_factory.create_command(lexed_arguments.get_command())
                command.execute(lexed_arguments, self.context)
            except ShellException as exception:
                print(exception.message)

    def _replace_tilda(self, lexed_arguments: list[str]) -> None:
        for i in range(len(lexed_arguments)):
            if lexed_arguments[i][0] == CommandShell.TILDA:
                lexed_arguments[i] = lexed_arguments[i].replace(CommandShell.TILDA, str(self.context.HOME))

    def _get_path_to_cwd(self, path_as_str: str) -> str:
        return path_as_str.replace(str(self.context.HOME), CommandShell.TILDA)