from abc import ABC

class ShellException(Exception, ABC):
    message: str

    def __init__(self, message: str):
        self.message = message

    def get_message(self):
        return self.message