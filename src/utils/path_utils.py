from datetime import datetime
from pathlib import Path
from stat import filemode

from src.exception.command_exception import (
    NotTypeFileException,
    NotTypeDirectoryException,
)
from src.exception.path_utils_exception import InvalidPathException


class PathUtils:
    @staticmethod
    def check_presence(path : Path) -> None:
        if not path.exists(follow_symlinks=False):
            raise InvalidPathException(path)

    @staticmethod
    def check_presence_file(path:Path) -> None:
        PathUtils.check_presence(path)
        if not path.is_file():
            raise NotTypeFileException(path.name)

    @staticmethod
    def check_presence_directory(path:Path) -> None:
        PathUtils.check_presence(path)
        if not path.is_dir():
            raise NotTypeDirectoryException(path.name)

    @staticmethod
    def get_filemode(path: Path) -> str:
        return filemode(path.lstat().st_mode)

    @staticmethod
    def get_count_links(path: Path) -> int:
        return path.lstat().st_nlink

    @staticmethod
    def get_bytes_size(path: Path) -> int:
        return path.lstat().st_size

    @staticmethod
    def get_last_change_time(path: Path) -> datetime:
        return datetime.fromtimestamp(path.lstat().st_ctime)

    @staticmethod
    def get_owner(path: Path) -> str:
        return path.owner(follow_symlinks=False)

    @staticmethod
    def get_group(path: Path) -> str:
        return path.group(follow_symlinks=False)

    @staticmethod
    def get_path_name(path: Path) -> str:
        PathUtils.check_presence(path)
        return path.name

    @staticmethod
    def get_cwd():
        return Path.cwd()

    @staticmethod
    def get_resolved_path(path: Path) -> Path:
        path = path.resolve()
        PathUtils.check_presence(path)
        return path

    @staticmethod
    def is_absolute(path: Path):
        return path.is_absolute()

    @staticmethod
    def get_directory_content(path: Path) -> list[Path]:
        return list(path.iterdir())