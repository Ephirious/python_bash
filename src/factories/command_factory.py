from abc import ABC, abstractmethod

from src.commands.abstract_commands import AbstractCommand
from src.commands.command_cd import CommandCD
from src.commands.command_ls import CommandLS
from src.common.parser import Parser
from src.exception.command_factory_exception import UnknownCommand


class AbstractCommandFactory(ABC):
    parser: Parser

    def __init__(self, parser: Parser):
        self.parser = parser

    @abstractmethod
    def create_command(self, command: str) -> AbstractCommand:
        pass


class CommandFactoryImp(AbstractCommandFactory):
    COMMANDS = {
        "ls": CommandLS,
        "cd": CommandCD
    }

    def __init__(self, parser: Parser):
        super().__init__(parser)

    def create_command(self, command: str) -> AbstractCommand:
        if command in CommandFactoryImp.COMMANDS:
            return CommandFactoryImp.COMMANDS[command](self.parser)
        raise UnknownCommand(command)