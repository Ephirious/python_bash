from shlex import split
from src.common.input_arguments import InputArguments

class Lexer:
    def __init__(self):
        pass

    def lexing(self, input_line: str):
        arguments = split(input_line, posix=True)
        command = arguments[0]
        other_arguments = arguments[1:]
        return InputArguments(command, other_arguments)
