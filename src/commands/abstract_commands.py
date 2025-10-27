from abc import ABC, abstractmethod

from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.exception.parsing_option_exception import (
    UnknownOptionException,
    InvalidRequiredOptionPositionException,
    ParseUnexpectedArgumentException,
    NotArgumentForOptionException, OptionRepeatException
)


class AbstractCommand(ABC):
    available_options: set[Option]
    parsed_arguments: ParsedArguments

    BEGINNING_OPTION_CHAR = '-'

    def __init__(self, options: set[Option], arguments: InputArguments):
        self.available_options = options
        self.parsed_arguments = self._get_parsed_input_arguments(arguments)

    @abstractmethod
    def execute(self):
        pass

    def _get_parsed_input_arguments(self, input_arguments: InputArguments) -> ParsedArguments:
        arguments = input_arguments.get_arguments()

        position = list()
        option_without_arguments: set[Option] = set()
        option_with_arguments: dict[Option, str] = dict()

        i = 0
        len_arguments = len(arguments)
        while i < len_arguments:
            current_argument = arguments[i]
            if self._is_option(current_argument):
                self._check_correctness_option(current_argument)
                if self._is_single_option(current_argument):
                    self._check_repeatable(current_argument, option_without_arguments, option_with_arguments)
                    if self._is_option_required_argument(current_argument):
                        self._add_required_argument_option(current_argument, arguments, i, option_with_arguments)
                        i += 1
                    else:
                        option_without_arguments.add(self._get_option_by_str(current_argument))
                else:
                    self._add_multiple_option(current_argument, arguments, i, option_without_arguments, option_with_arguments)
                    i += 1
            else:
                position.append(current_argument)
            i += 1

        return ParsedArguments(position, option_without_arguments, option_with_arguments)


    @staticmethod
    def _is_option(argument: str) -> bool:
        return argument[0] == AbstractCommand.BEGINNING_OPTION_CHAR

    def _is_single_option(self, argument: str) -> bool:
        if not self._is_option(argument):
            raise ParseUnexpectedArgumentException(argument)
        return ((self._is_option(argument) and len(argument) == 2) or
                (self._is_option(argument) and argument[1] == AbstractCommand.BEGINNING_OPTION_CHAR))

    def _is_multiple_option(self, argument: str) -> bool:
        if not self._is_option(argument):
            raise ParseUnexpectedArgumentException(argument)
        return (not self._is_single_option(argument) and
                argument[1] != AbstractCommand.BEGINNING_OPTION_CHAR)

    def _is_multiple_option_required_argument(self, option: str) -> bool:
        if not self._is_multiple_option(option):
            raise ParseUnexpectedArgumentException(option)
        last_option = option[-1]
        return self._is_option_required_argument(last_option)

    def _split_multiple_option(self, argument: str) -> list[str]:
        if not self._is_multiple_option(argument):
            raise ParseUnexpectedArgumentException(argument)

        result = list()
        for option in argument[1:]:
            result.append(AbstractCommand.BEGINNING_OPTION_CHAR + option)
        return result

    def _is_available_option(self, argument: str) -> bool:
        if self._is_option(argument):
            for option in self.available_options:
                if option.get_short_name() == argument or option.get_full_name() == argument:
                    return True
        return False

    def _is_option_required_argument(self, argument: str) -> bool:
        if self._is_option(argument):
            for option in self.available_options:
                if option.get_short_name() == argument or option.get_full_name() == argument:
                    return option.is_required_argument()
        return False


    def _check_correctness_option(self, argument: str) -> None:
        if not self._is_option(argument):
            raise ParseUnexpectedArgumentException(argument)

        if self._is_single_option(argument):
            if not self._is_available_option(argument):
                raise UnknownOptionException(argument)
        else:
            len_multiple_option = len(argument)
            for i in range(1, len_multiple_option):
                current_option = AbstractCommand.BEGINNING_OPTION_CHAR + argument[i]
                if not self._is_available_option(current_option):
                    raise UnknownOptionException(argument)
                if (self._is_option_required_argument(current_option) and
                    i != len_multiple_option - 1):
                    raise InvalidRequiredOptionPositionException(argument)

    def _check_next_argument_for_required_option(self, argument: str) -> None:
        if self._is_option(argument):
            raise NotArgumentForOptionException(argument)

    def _get_option_by_str(self, argument: str) -> Option:
        for option in self.available_options:
            if option.get_short_name() == argument or option.get_full_name() == argument:
                return option
        raise UnknownOptionException(argument)

    def _add_required_argument_option(self,
                                      option: str,
                                      arguments: list[str],
                                      pos: int,
                                      dict_with_options: dict[Option, str]) -> None:
        arguments_len = len(arguments)
        if pos + 1 >= arguments_len:
            raise NotArgumentForOptionException(arguments[pos])
        if self._is_option(arguments[pos + 1]):
            raise NotArgumentForOptionException(arguments[pos])
        current_option = self._get_option_by_str(option)
        value = arguments[pos + 1]
        dict_with_options[current_option] = value

    def _add_multiple_option(self,
                             options: str,
                             arguments: list[str],
                             pos: int,
                             set_options: set[Option],
                             dict_options: dict[Option, str]) -> None:
        split_options = self._split_multiple_option(options)
        for i in range(len(split_options) - 1):
            self._check_repeatable(split_options[i], set_options, dict_options)
            option = self._get_option_by_str(split_options[i])
            set_options.add(option)
        if self._is_option_required_argument(split_options[-1]):
            self._add_required_argument_option(split_options[-1], arguments, pos, dict_options)
        else:
            option = self._get_option_by_str(split_options[-1])
            set_options.add(option)

    def _check_repeatable(self, option: str, set_option: set[Option], dict_option: dict[Option, str]) -> None:
        current_option = self._get_option_by_str(option)
        if not current_option.is_repeatable():
            if current_option in set_option or current_option in dict_option:
                raise OptionRepeatException(option)