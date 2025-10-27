class InputArguments:
    command: str
    arguments: list[str]

    def __init__(self, command: str, arguments: list[str]):
        self.command = command
        self.arguments = arguments

    def get_command(self) -> str:
        return self.command

    def get_arguments(self) -> list[str]:
        return self.arguments
