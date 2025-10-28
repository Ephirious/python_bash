from abc import ABC, abstractmethod

from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parser import Parser


class AbstractCommand(ABC):
    available_options: set[Option]
    parser: Parser

    def __init__(self, options: set[Option]):
        self.available_options = options

    @abstractmethod
    def execute(self, arguments: InputArguments):
        pass