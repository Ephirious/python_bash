class InputArguments:
    command: str
    arguments: list[str]

    def __init__(self, command: str, arguments: list[str]):
        """
        Initialize the input arguments container.
        :param command: Command name extracted from input.
        :type command: str
        :param arguments: Remaining arguments for the command.
        :type arguments: list[str]
        :return: None
        :rtype: None
        """
        self.command = command
        self.arguments = arguments

    def get_command(self) -> str:
        """
        Retrun the command name.
        :return: Parsed command name.
        :rtype: str
        """
        return self.command

    def get_arguments(self) -> list[str]:
        """
        Retrun the command arguments.
        :return: List of command arguments.
        :rtype: list[str]
        """
        return self.arguments