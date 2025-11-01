
from src.exception.shell_exception import ShellException


class UnexpectedArgumentsException(ShellException):
    MESSAGE = "Unexpected arguments: "

    def __init__(self, args: list[str]):
        super().__init__(UnexpectedArgumentsException.MESSAGE + ", ".join(args))


class NotEnoughArgumentsException(ShellException):
    MESSAGE = "Not enough arguments"

    def __init__(self):
        super().__init__(NotEnoughArgumentsException.MESSAGE)


class NotTypeFileException(ShellException):
    MESSAGE = "Not a file: "

    def __init__(self, file_name: str):
        super().__init__(NotTypeFileException.MESSAGE + file_name)


class NotTypeDirectoryException(ShellException):
    MESSAGE = "Not a directory: "

    def __init__(self, directory: str):
        super().__init__(NotTypeFileException.MESSAGE + directory)

class NotEnoughOptionException(ShellException):
    MESSAGE = "Not enough option: "

    def __init__(self, option: str):
        super().__init__(NotEnoughOptionException.MESSAGE + option)


class NotAccessToReadException(ShellException):
    MESSAGE = "Next file or directory is not readable: "

    def __init__(self, path: str):
        super().__init__(NotAccessToReadException.MESSAGE + path)


class NotAccessToWriteException(ShellException):
    MESSAGE = "Next file or directory is not writeable: "

    def __init__(self, path: str):
        super().__init__(NotAccessToWriteException.MESSAGE + path)


class NotEnoughPermissionToRemoveException(ShellException):
    MESSAGE = "Not enough permission for remove: "
    def __init__(self, path: str):
        super().__init__(NotEnoughPermissionToRemoveException.MESSAGE + path)