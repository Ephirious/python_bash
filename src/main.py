from src.common.lexer import Lexer
from src.common.parser import Parser
from src.factories.command_factory import CommandFactoryImp
from src.command_shell import CommandShell

if __name__ == "__main__":
    lexer = Lexer()
    parser = Parser()
    factory = CommandFactoryImp(parser)
    shell = CommandShell(factory, lexer)
    shell.run()