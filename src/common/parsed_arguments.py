class ParsedArguments:
    position_arguments: list[str]
    options_without_argument: set[str]
    options_with_argument: dict[str, str]

    def __init__(self,
                 position_arguments: list[str],
                 options_without_arguments: set[str],
                 options_with_arguments: dict[str, str]):
        self.position_arguments = position_arguments
        self.options_without_argument = options_without_arguments
        self.options_with_argument = options_with_arguments

    def get_position_arguments(self) -> list[str]:
        return self.position_arguments

    def get_options_without_argument(self) -> set[str]:
        return self.options_without_argument

    def get_options_with_argument(self) -> dict[str, str]:
        return self.options_with_argument

    def __eq__(self, other):
        return (isinstance(other, ParsedArguments) and
                self.position_arguments == other.position_arguments and
                self.options_without_argument == other.options_without_argument and
                self.options_with_argument == other.options_with_argument)