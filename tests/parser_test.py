import pytest

from src.common.option import Option
from src.common.parser import Parser
from src.exception.parsing_option_exception import (
    UnknownOptionException,
    InvalidRequiredOptionPositionException,
    NotArgumentForOptionException,
    OptionRepeatException,
    ParseInvalidPositionException,
)
from src.common.lexer import Lexer
from src.common.parsed_arguments import ParsedArguments

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


@pytest.mark.parametrize(
    "input_line, result",
    [
        [
            "test -l -a -r",
            ParsedArguments(list(), {"-l", "-a", "-r"}, {})
        ],
        [
            "test --list --all --recursive",
            ParsedArguments(list(), {"--list", "--all", "--recursive"}, {})
        ],
        [
            "test -lar",
            ParsedArguments(list(), {"-l", "-a", "-r"}, {})
        ],
        [
            "test -lan 10",
            ParsedArguments(list(), {"-l", "-a"}, {"-n": "10"})
        ],
        [
            "test -o output.txt -h -t",
            ParsedArguments(list(), {"-h", "-t"}, {"-o": "output.txt"})
        ],
        [
            "test --output result.log --human-readable --time",
            ParsedArguments(list(), {"--human-readable", "--time"}, {"--output": "result.log"})
        ],
        [
            "test -e .txt -e .md -e .pdf",
            ParsedArguments(list(), set(), {"-e": ".pdf"})
        ],
        [
            'test --pattern "report 2025" -i',
            ParsedArguments(list(), {"-i"}, {"--pattern": "report 2025"})
        ],
        [
            "test --max-depth 3 -r -d",
            ParsedArguments(list(), {"-r", "-d"}, {"--max-depth": "3"})
        ],
        [
            "test -V -D 2 --lines 50",
            ParsedArguments(list(), {"-V"}, {"-D": "2", "--lines": "50"})
        ],
        [
            'test -c -m --pattern "[A-Z]{3}[0-9]{2}"',
            ParsedArguments(list(), {"-c", "-m"}, {"--pattern": "[A-Z]{3}[0-9]{2}"})
        ],
        [
            "test --format table --output out.txt",
            ParsedArguments(list(), set(), {"--format": "table", "--output": "out.txt"})
        ],
        [
            "test -t -n 100 --dirs",
            ParsedArguments(list(), {"-t", "--dirs"}, {"-n": "100"})
        ],
        [
            "test -a -e jpg -e png --recursive --max-depth 1",
            ParsedArguments(list(), {"-a", "--recursive"}, {"-e": "png", "--max-depth": "1"})
        ],
        [
            "test -r -D 0",
            ParsedArguments(list(), {"-r"}, {"-D": "0"})
        ],
        [
            "test -h -t -v",
            ParsedArguments(list(), {"-h", "-t", "-v"}, {})
        ],
        [
            "test -q --color",
            ParsedArguments(list(), {"-q", "--color"}, {})
        ],
        [
            "test --format json --quiet --dirs",
            ParsedArguments(list(), {"--quiet", "--dirs"}, {"--format": "json"})
        ],
        [
            "test -F csv -o out.csv -e csv",
            ParsedArguments(list(), set(), {"-F": "csv", "-o": "out.csv", "-e": "csv"})
        ]
    ]
)
def test_parser_with_valid_arguments(input_line, result):
    lexer = Lexer()
    argument_line = lexer.lexing(input_line)
    parser = Parser()
    parsed_arguments = parser.parse(OPTIONS, argument_line)
    assert parsed_arguments == result

@pytest.mark.parametrize(
    "input_line, exc",
    [
        ["test -z", UnknownOptionException],
        ["test --unknown", UnknownOptionException],
        ["test --listt", UnknownOptionException],
        ["test -nl 10", InvalidRequiredOptionPositionException],
        ["test -anl 10", InvalidRequiredOptionPositionException],
        ["test -De 3", InvalidRequiredOptionPositionException],
        ["test -pe pattern", InvalidRequiredOptionPositionException],
        ["test -el jpg", InvalidRequiredOptionPositionException],
        ["test -n", ParseInvalidPositionException],
        ["test --lines", ParseInvalidPositionException],
        ["test -o", ParseInvalidPositionException],
        ["test --output", ParseInvalidPositionException],
        ["test -D", ParseInvalidPositionException],
        ["test --max-depth", ParseInvalidPositionException],
        ["test -e", ParseInvalidPositionException],
        ["test --extension", ParseInvalidPositionException],
        ["test -p", ParseInvalidPositionException],
        ["test --pattern", ParseInvalidPositionException],
        ["test -n -a", NotArgumentForOptionException],
        ["test -o -l", NotArgumentForOptionException],
        ["test -D -r", NotArgumentForOptionException],
        ["test -e -t", NotArgumentForOptionException],
        ["test -p --time", NotArgumentForOptionException],
        ["test -n10", InvalidRequiredOptionPositionException],
        ["test -D2", InvalidRequiredOptionPositionException],
        ["test -l -l", OptionRepeatException],
        ["test --time --time", OptionRepeatException],
        ["test -n 1 -n 2", OptionRepeatException],
        ["test --format csv --format tsv", OptionRepeatException],
        ["test -o a.txt -o b.txt", OptionRepeatException],
        ["test -v -v", OptionRepeatException],
        ["test -q -q", OptionRepeatException],
        ["test -d -d", OptionRepeatException],
        ["test -h -h", OptionRepeatException],
        ["test -e jpg -e", ParseInvalidPositionException],
    ]
)
def test_parser_invalid_arguments_raise(input_line, exc):
    lexer = Lexer()
    parser = Parser()
    with pytest.raises(exc):
        argument_line = lexer.lexing(input_line)
        parser.parse(OPTIONS, argument_line)
