
from src.exception.shell_exception import ShellException


class UnexpectedArguments(ShellException):
    MESSAGE = "Unexpected arguments: "

    def __init__(self, args: list[str]):
        super().__init__(UnexpectedArguments.MESSAGE + ", ".join(args))