import pytest

from src.exception.parsing_option_exception import UnknownOptionException, InvalidRequiredOptionPositionException, \
    NotArgumentForOptionException, OptionRepeatException
from tests.command_test import CommandTest
from src.common.lexer import Lexer
from src.common.option import Option
from src.common.parsed_arguments import ParsedArguments


@pytest.mark.parametrize(
    "input_line, result",
    [
        [
            "test -l -a -r",
            ParsedArguments(
                list(),
                {
                    Option("Показать список файлов в директории", "-l", "--list", False, False),
                    Option("Показать скрытые файлы", "-a", "--all", False, False),
                    Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
                },
                {}
            )
        ],
        [
            "test --list --all --recursive",
            ParsedArguments(
                list(),
                {
                    Option("Показать список файлов в директории", "-l", "--list", False, False),
                    Option("Показать скрытые файлы", "-a", "--all", False, False),
                    Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
                },
                {}
            )
        ],
        [
            "test -lar",
            ParsedArguments(
                list(),
                {
                    Option("Показать список файлов в директории", "-l", "--list", False, False),
                    Option("Показать скрытые файлы", "-a", "--all", False, False),
                    Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
                },
                {}
            )
        ],
        [
            "test -lan 10",
            ParsedArguments(
                list(),
                {
                    Option("Показать список файлов в директории", "-l", "--list", False, False),
                    Option("Показать скрытые файлы", "-a", "--all", False, False),
                },
                {
                    Option("Задать количество строк для вывода", "-n", "--lines", True, False): "10",
                }
            )
        ],
        [
            "test -o output.txt -h -t",
            ParsedArguments(
                list(),
                {
                    Option("Вывести размер файлов в человеко-читаемом виде", "-h", "--human-readable", False, False),
                    Option("Отсортировать вывод по времени изменения", "-t", "--time", False, False),
                },
                {
                    Option("Сохранить результат в указанный файл", "-o", "--output", True, False): "output.txt",
                }
            )
        ],
        [
            "test --output result.log --human-readable --time",
            ParsedArguments(
                list(),
                {
                    Option("Вывести размер файлов в человеко-читаемом виде", "-h", "--human-readable", False, False),
                    Option("Отсортировать вывод по времени изменения", "-t", "--time", False, False),
                },
                {
                    Option("Сохранить результат в указанный файл", "-o", "--output", True, False): "result.log",
                }
            )
        ],
        [
            "test -e .txt -e .md -e .pdf",
            ParsedArguments(
                list(),
                set(),
                {
                    Option("Применить фильтр по расширению файла", "-e", "--extension", True, True): ".pdf",
                }
            )
        ],
        [
            'test --pattern "report 2025" -i',
            ParsedArguments(
                list(),
                {
                    Option("Игнорировать регистр при поиске", "-i", "--ignore-case", False, False),
                },
                {
                    Option("Указать шаблон для поиска", "-p", "--pattern", True, False): "report 2025",
                }
            )
        ],
        [
            "test --max-depth 3 -r -d",
            ParsedArguments(
                list(),
                {
                    Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
                    Option("Отобразить только директории", "-d", "--dirs", False, False),
                },
                {
                    Option("Задать максимальную глубину рекурсии", "-D", "--max-depth", True, False): "3",
                }
            )
        ],
        [
            "test -V -D 2 --lines 50",
            ParsedArguments(
                list(),
                {
                    Option("Показать подробный отчёт о действиях", "-V", "--verbose", False, False),
                },
                {
                    Option("Задать максимальную глубину рекурсии", "-D", "--max-depth", True, False): "2",
                    Option("Задать количество строк для вывода", "-n", "--lines", True, False): "50",
                }
            )
        ],
        [
            'test -c -m --pattern "[A-Z]{3}[0-9]{2}"',
            ParsedArguments(
                list(),
                {
                    Option("Подсветить совпадения цветом", "-c", "--color", False, False),
                    Option("Вывести только совпадения", "-m", "--matches-only", False, False),
                },
                {
                    Option("Указать шаблон для поиска", "-p", "--pattern", True, False): "[A-Z]{3}[0-9]{2}",
                }
            )
        ],
        [
            "test --format table --output out.txt",
            ParsedArguments(
                list(),
                set(),
                {
                    Option("Задать формат вывода", "-F", "--format", True, False): "table",
                    Option("Сохранить результат в указанный файл", "-o", "--output", True, False): "out.txt",
                }
            )
        ],
        [
            "test -t -n 100 --dirs",
            ParsedArguments(
                list(),
                {
                    Option("Отсортировать вывод по времени изменения", "-t", "--time", False, False),
                    Option("Отобразить только директории", "-d", "--dirs", False, False),
                },
                {
                    Option("Задать количество строк для вывода", "-n", "--lines", True, False): "100",
                }
            )
        ],
        [
            "test -a -e jpg -e png --recursive --max-depth 1",
            ParsedArguments(
                list(),
                {
                    Option("Показать скрытые файлы", "-a", "--all", False, False),
                    Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
                },
                {
                    Option("Применить фильтр по расширению файла", "-e", "--extension", True, True): "png",
                    Option("Задать максимальную глубину рекурсии", "-D", "--max-depth", True, False): "1",
                }
            )
        ],
        [
            "test -r -D 0",
            ParsedArguments(
                list(),
                {
                    Option("Рекурсивно обойти подкаталоги", "-r", "--recursive", False, False),
                },
                {
                    Option("Задать максимальную глубину рекурсии", "-D", "--max-depth", True, False): "0",
                }
            )
        ],
        [
            "test -h -t -v",
            ParsedArguments(
                list(),
                {
                    Option("Вывести размер файлов в человеко-читаемом виде", "-h", "--human-readable", False, False),
                    Option("Отсортировать вывод по времени изменения", "-t", "--time", False, False),
                    Option("Показать версии программы", "-v", "--version", False, False),
                },
                {}
            )
        ],
        [
            "test -q --color",
            ParsedArguments(
                list(),
                {
                    Option("Не выводить сообщения об ошибках", "-q", "--quiet", False, False),
                    Option("Подсветить совпадения цветом", "-c", "--color", False, False),
                },
                {}
            )
        ],
        [
            "test --format json --quiet --dirs",
            ParsedArguments(
                list(),
                {
                    Option("Не выводить сообщения об ошибках", "-q", "--quiet", False, False),
                    Option("Отобразить только директории", "-d", "--dirs", False, False),
                },
                {
                    Option("Задать формат вывода", "-F", "--format", True, False): "json",
                }
            )
        ],
        [
            "test -F csv -o out.csv -e csv",
            ParsedArguments(
                list(),
                set(),
                {
                    Option("Задать формат вывода", "-F", "--format", True, False): "csv",
                    Option("Сохранить результат в указанный файл", "-o", "--output", True, False): "out.csv",
                    Option("Применить фильтр по расширению файла", "-e", "--extension", True, True): "csv",
                }
            )
        ],
    ]
)
def test_parser_with_valid_arguments(input_line, result):
    lexer = Lexer()
    argument_line = lexer.lexing(input_line)
    test_command = CommandTest(argument_line)
    assert test_command.get_parsed_arguments() == result

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
        ["test -n", NotArgumentForOptionException],
        ["test --lines", NotArgumentForOptionException],
        ["test -o", NotArgumentForOptionException],
        ["test --output", NotArgumentForOptionException],
        ["test -D", NotArgumentForOptionException],
        ["test --max-depth", NotArgumentForOptionException],
        ["test -e", NotArgumentForOptionException],
        ["test --extension", NotArgumentForOptionException],
        ["test -p", NotArgumentForOptionException],
        ["test --pattern", NotArgumentForOptionException],
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
        ["test -e jpg -e", NotArgumentForOptionException],
    ]
)
def test_parser_invalid_arguments_raise(input_line, exc):
    lexer = Lexer()
    with pytest.raises(exc):
        argument_line = lexer.lexing(input_line)
        command_test = CommandTest(argument_line)
        command_test.get_parsed_arguments()
