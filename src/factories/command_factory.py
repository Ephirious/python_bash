from abc import ABC, abstractmethod

class AbstractCommandFactory(ABC):
    #command: di

    @abstractmethod
    def create_command(self):
        pass