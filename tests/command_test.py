from src.commands.abstract_commands import AbstractCommand
from src.common.input_arguments import InputArguments
from src.common.lexer import Lexer
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments


class CommandTest(AbstractCommand):
    OPTIONS = {
        Option("Показать список файлов в директории", "-l", "--list", False, False),
        Option("Показать скрытые файлы", "-a", "--all", False, False),
        Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
        Option("Вывести размер файлов в человеко-читаемом виде", "-h", "--human-readable", False, False),
        Option("Принудительно удалить файлы без подтверждения", "-f", "--force", False, False),
        Option("Задать формат вывода", "-F", "--format", True, False),
        Option("Задать количество строк для вывода", "-n", "--lines", True, False),
        Option("Сохранить результат в указанный файл", "-o", "--output", True, False),
        Option("Отсортировать вывод по времени изменения", "-t", "--time", False, False),
        Option("Отобразить только директории", "-d", "--dirs", False, False),
        Option("Игнорировать регистр при поиске", "-i", "--ignore-case", False, False),
        Option("Вывести только совпадения", "-m", "--matches-only", False, False),
        Option("Показать версии программы", "-v", "--version", False, False),
        Option("Задать максимальную глубину рекурсии", "-D", "--max-depth", True, False),
        Option("Применить фильтр по расширению файла", "-e", "--extension", True, True),
        Option("Указать шаблон для поиска", "-p", "--pattern", True, False),
        Option("Не выводить сообщения об ошибках", "-q", "--quiet", False, False),
        Option("Подсветить совпадения цветом", "-c", "--color", False, False),
        Option("Показать подробный отчёт о действиях", "-V", "--verbose", False, False),
    }

    def __init__(self, input_arguments : InputArguments):
        super().__init__(CommandTest.OPTIONS, input_arguments)

    def execute(self):
        pass

    def get_parsed_arguments(self) -> ParsedArguments:
        return self.parsed_arguments