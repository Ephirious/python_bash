from pathlib import Path

from src.exception.shell_exception import ShellException


class InvalidPathException(ShellException):
    MESSAGE = "Next path is not exist: "

    def __init__(self, path : Path) -> None:
        super().__init__(self.MESSAGE + str(path))