from src.commands.abstract_commands import AbstractCommand
from src.common.context import Context
from src.common.input_arguments import InputArguments
from src.common.logger import Logger
from src.common.option import Option
from src.common.parser import Parser
from src.exception.command_exception import UnexpectedArgumentsException


class CommandHistory(AbstractCommand):
    OPTIONS: set[Option] = {
        Option("Показать список всех опций", "-h", "--help", False, True),
        Option("Показать последние n записей", "-n", "--number", True, False)
    }

    def __init__(self, parser: Parser, logger: Logger):
        super().__init__(CommandHistory.OPTIONS, parser, logger)

    def execute(self, arguments: InputArguments, context: Context):
        self.parsed_arguments = self.parser.parse(CommandHistory.OPTIONS, arguments)
        if self.output_help_if_need():
            return

        count_position_arguments = len(self.parsed_arguments.position_arguments)

        match count_position_arguments:
            case 0:
                entries = []
                if self.is_in_parsed_arguments("-n", "--number", self.parsed_arguments):
                    count_entries = int(self._get_options_arguments("-n", "--number"))
                    entries = self._get_entries(context, count_entries)
                else:
                    entries = self._get_entries(context)
                for num, entry in enumerate(entries):
                    self.logger.print(f"{num + 1}: {entry[:-1]}")

            case _:
                raise UnexpectedArgumentsException(self.parsed_arguments.position_arguments)

    def _get_entries(self, context: Context, count = 0):
        if count == 0:
            return context.HISTORY_PATH.open("r").readlines()
        else:
            return context.HISTORY_PATH.open("r").readlines()[-count:]
