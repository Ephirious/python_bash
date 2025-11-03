class ParsedArguments:
    position_arguments: list[str]
    options_without_argument: set[str]
    options_with_argument: dict[str, str]

    def __init__(self,
                 position_arguments: list[str],
                 options_without_arguments: set[str],
                 options_with_arguments: dict[str, str]):
        """
        Initialize the parsed arguments container.
        :param position_arguments: Collected positional arguments.
        :type position_arguments: list[str]
        :param options_without_arguments: Options provided without values.
        :type options_without_arguments: set[str]
        :param options_with_arguments: Options mapped to their argument values.
        :type options_with_arguments: dict[str, str]
        :return: None
        :rtype: None
        """
        self.position_arguments = position_arguments
        self.options_without_argument = options_without_arguments
        self.options_with_argument = options_with_arguments

    def get_position_arguments(self) -> list[str]:
        """
        Retrieve the collected positional arguments.
        :return: List of positional arguments.
        :rtype: list[str]
        """
        return self.position_arguments

    def get_options_without_argument(self) -> set[str]:
        """
        Retrieve options supplied without arguments.
        :return: Set of option names without arguments.
        :rtype: set[str]
        """
        return self.options_without_argument

    def get_options_with_argument(self) -> dict[str, str]:
        """
        Retrieve options supplied with arguments.
        :return: Mapping of option names to argument values.
        :rtype: dict[str, str]
        """
        return self.options_with_argument

    def __eq__(self, other):
        """
        Compare parsed arguments instances for equality.
        :param other: Object to compare against.
        :type other: Any
        :return: Flag indicating if the parsed arguments are equal.
        :rtype: bool
        """
        return (isinstance(other, ParsedArguments) and
                self.position_arguments == other.position_arguments and
                self.options_without_argument == other.options_without_argument and
                self.options_with_argument == other.options_with_argument)
