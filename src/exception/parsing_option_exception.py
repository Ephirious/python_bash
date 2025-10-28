from src.exception.shell_exception import ShellException

class UnknownOptionException(ShellException):
    MESSAGE = "Unknown option: "

    def __init__(self, option: str):
        super().__init__(UnknownOptionException.MESSAGE + option)


class InvalidRequiredOptionPositionException(ShellException):
    MESSAGE = "Invalid option position: "
    def __init__(self, option: str):
        super().__init__(InvalidRequiredOptionPositionException.MESSAGE + option)


class ParseUnexpectedArgumentException(ShellException):
    MESSAGE = "Unexpected argument while parsing: "

    def __init__(self, argument: str):
        super().__init__(ParseUnexpectedArgumentException.MESSAGE + argument)


class NotArgumentForOptionException(ShellException):
    MESSAGE = "There is no argument for the option "

    def __init__(self, option: str):
        super().__init__(NotArgumentForOptionException.MESSAGE + option)


class OptionRepeatException(ShellException):
    MESSAGE = "This option can't be repeated: "

    def __init__(self, option: str):
        super().__init__(OptionRepeatException.MESSAGE + option)

class ParseInvalidPositionException(ShellException):
    MESSAGE = "Invalid position while parsing"

    def __init__(self):
        super().__init__(ParseInvalidPositionException.MESSAGE)