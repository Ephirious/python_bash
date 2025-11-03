from shlex import split
from src.common.input_arguments import InputArguments

class Lexer:
    def __init__(self):
        """
        Initialize the lexer instance.
        :return: None
        :rtype: None
        """
        pass

    def lexing(self, input_line: str):
        """
        Tokenize the input line into command and arguments.
        :param input_line: Raw command line string.
        :type input_line: str
        :return: Structured command and arguments container.
        :rtype: InputArguments
        """
        arguments = split(input_line, posix=True)
        command = arguments[0]
        other_arguments = arguments[1:]
        return InputArguments(command, other_arguments)