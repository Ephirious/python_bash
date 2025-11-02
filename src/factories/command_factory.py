from abc import ABC, abstractmethod

from src.commands.abstract_commands import AbstractCommand
from src.commands.command_cat import CommandCat
from src.commands.command_cd import CommandCD
from src.commands.command_cp import CommandCP
from src.commands.command_grep import CommandGrep
from src.commands.command_history import CommandHistory
from src.commands.command_ls import CommandLS
from src.commands.command_mv import CommandMV
from src.commands.command_rm import CommandRM
from src.commands.command_tar import CommandTAR
from src.commands.command_undo import CommandUndo
from src.commands.command_zip import CommandZIP
from src.common.logger import Logger
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
    logger: Logger

    COMMANDS = {
        "ls": CommandLS,
        "cd": CommandCD,
        "cat": CommandCat,
        "cp": CommandCP,
        "mv": CommandMV,
        "rm": CommandRM,
        "tar": CommandTAR,
        "zip": CommandZIP,
        "grep": CommandGrep,
        "history": CommandHistory,
        "undo": CommandUndo
    }

    def __init__(self, parser: Parser, logger: Logger):
        super().__init__(parser)
        self.logger = logger

    def create_command(self, command: str) -> AbstractCommand:
        if command in CommandFactoryImp.COMMANDS:
            return CommandFactoryImp.COMMANDS[command](self.parser, self.logger)
        raise UnknownCommand(command)