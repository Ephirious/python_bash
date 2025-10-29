from src.exception.shell_exception import ShellException


class UnknownCommand(ShellException):
    MESSAGE = "Unknown command: "

    def __init__(self, command: str):
        super().__init__(self.MESSAGE + command)