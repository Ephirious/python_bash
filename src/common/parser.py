from src.common.input_arguments import InputArguments
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments
from src.exception.parsing_option_exception import (
    ParseInvalidPositionException,
    ParseUnexpectedArgumentException,
    NotArgumentForOptionException,
    InvalidRequiredOptionPositionException,
    UnknownOptionException, OptionRepeatException,
)


class Parser:
    _options_by_short_name: dict[str, tuple[bool, bool]]
    _options_by_full_name: dict[str, tuple[bool, bool]]

    arguments: list[str]
    pos: int
    is_next_position: bool

    position_arguments: list[str]
    options_without_arguments: set[str]
    options_with_arguments: dict[str, str]

    BEGINNING_OPTION_CHAR = '-'
    POSITIONAL_POINT = "--"

    def __init__(self):
        self.available_options = set()
        self.arguments = list()
        self.pos = 0
        self.position_arguments = list()
        self.options_without_arguments = set()
        self.options_with_arguments = dict()
        self.is_next_position = False
        self._options_by_short_name = {}
        self._options_by_full_name = {}

    def parse(self, available_options : set[Option], input_arguments : InputArguments) -> ParsedArguments:
        self.arguments = input_arguments.get_arguments()
        self._parse_option_for_dict(available_options)

        while self._is_valid_pos():
            self._parse_arguments()
            self._next()

        return ParsedArguments(self.position_arguments, self.options_without_arguments, self.options_with_arguments)

    def _parse_option_for_dict(self, available_options: set[Option]) -> None:
        for option in available_options:
            short_name = option.get_short_name()
            full_name = option.get_full_name()
            self._options_by_short_name[short_name] = (option.is_required_argument(), option.is_repeatable())
            self._options_by_full_name[full_name] = (option.is_required_argument(), option.is_repeatable())

    def _get_current(self) -> str:
        self._check_pos()
        return self.arguments[self.pos]

    def _next(self):
        self.pos += 1

    def _parse_arguments(self):
        if self._get_current() == Parser.POSITIONAL_POINT:
            self.is_next_position = True
        if self.is_next_position:
            self.position_arguments.append(self._get_current())
        else:
            arg = self._get_current()
            if self._is_option(arg):
                self._parse_option(arg)
            else:
                self.position_arguments.append(arg)

    def _parse_option(self, argument: str):
        self._check_is_option(argument)

        if self._is_single_option(argument):
            self._parse_single_option(argument)
        else:
            self._parse_multiple_option(argument)

    def _split_multiple_option(self, argument: str) -> list[str]:
        return [Parser.BEGINNING_OPTION_CHAR + x for x in argument[1:]]

    def _add_option_with_argument(self, option: str) -> None:
        self._check_pos()
        if self._is_option(self._get_current()):
            raise NotArgumentForOptionException(self._get_current())
        self.options_with_arguments[option] = self._get_current()

    def _parse_single_option(self, option: str) -> None:
        self._check_is_option(option)
        self._check_is_single_option(option)
        self._check_is_available_option(option)
        self._check_repeatable(option)

        if self._is_required_argument(option):
            self._next()
            self._add_option_with_argument(option)
        else:
            self.options_without_arguments.add(option)

    def _parse_multiple_option(self, option: str) -> None:
        self._check_is_multiple_option(option)

        split_options = self._split_multiple_option(option)
        for current_option in split_options[:len(split_options) - 1]:
            self._check_is_available_option(current_option)
            self._check_is_required_argument(current_option)
            self.options_without_arguments.add(current_option)

        self._check_is_available_option(split_options[-1])
        if self._is_required_argument(split_options[-1]):
            self._next()
            self._add_option_with_argument(split_options[-1])
        else:
            self.options_without_arguments.add(split_options[-1])

    def _is_valid_pos(self):
        return self.pos < len(self.arguments)

    def _is_option(self, argument: str) -> bool:
        return argument[0] == Parser.BEGINNING_OPTION_CHAR

    def _is_available_option(self, option: str) -> bool:
        self._check_is_option(option)
        return (option in self._options_by_short_name or
                option in self._options_by_full_name)

    def _is_long_name(self, argument: str) -> bool:
        self._check_is_option(argument)
        if (argument[0] == Parser.BEGINNING_OPTION_CHAR and
            argument[1] == Parser.BEGINNING_OPTION_CHAR):
            return True
        return False

    def _is_single_option(self, argument: str) -> bool:
        self._check_is_option(argument)
        return ((self._is_option(argument) and len(argument) == 2) or
                (self._is_option(argument) and argument[1] == Parser.BEGINNING_OPTION_CHAR))

    def _is_required_argument(self, argument: str) -> bool:
        self._check_is_option(argument)
        self._check_is_available_option(argument)
        if self._is_long_name(argument):
            return self._options_by_full_name[argument][0]
        return self._options_by_short_name[argument][0]

    def _is_repeatable(self, option: str) -> bool:
        self._check_is_option(option)
        self._is_available_option(option)
        if self._is_long_name(option):
            return self._options_by_full_name[option][1]
        return self._options_by_short_name[option][1]

    def _is_already_parsed(self, option: str) -> bool:
        self._check_is_option(option)
        return option in self.options_with_arguments or option in self.options_without_arguments

    def _check_pos(self):
        if not self._is_valid_pos():
            raise ParseInvalidPositionException()

    def _check_is_option(self, option: str) -> None:
        if not self._is_option(option):
            raise ParseUnexpectedArgumentException(option)

    def _check_is_available_option(self, option: str) -> None:
        if not self._is_available_option(option):
            raise UnknownOptionException(option)

    def _check_is_single_option(self, option: str) -> None:
        if not self._is_single_option(option):
            raise ParseUnexpectedArgumentException(option)

    def _check_repeatable(self, option: str) -> None:
        if not self._is_repeatable(option) and self._is_already_parsed(option):
            raise OptionRepeatException(option)

    def _check_is_multiple_option(self, option: str) -> None:
        if self._is_single_option(option):
            raise ParseUnexpectedArgumentException(option)

    def _check_is_required_argument(self, option: str) -> None:
        if self._is_required_argument(option):
            raise InvalidRequiredOptionPositionException(option)