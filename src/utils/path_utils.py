import os
import shutil
import tarfile
import zipfile
from datetime import datetime
from pathlib import Path
from stat import filemode

from src.exception.command_exception import (
    NotAccessToReadException,
    NotAccessToWriteException,
    NotEnoughPermissionToRemoveException,
    NotTypeDirectoryException,
    NotTypeFileException,
)
from src.exception.path_utils_exception import InvalidPathException


class PathUtils:
    @staticmethod
    def check_presence(path : Path) -> None:
        """
        Ensure that the provided path exists on the filesystem.
        :param path: Filesystem path to validate.
        :type path: Path
        :return: None
        :rtype: None
        """
        if not path.exists(follow_symlinks=False):
            raise InvalidPathException(path)

    @staticmethod
    def check_presence_file(path:Path) -> None:
        """
        Ensure that the provided path exists and points to a file.
        :param path: Filesystem path that should reference a file.
        :type path: Path
        :return: None
        :rtype: None
        """
        PathUtils.check_presence(path)
        if not path.is_file():
            raise NotTypeFileException(path.name)

    @staticmethod
    def check_presence_directory(path:Path) -> None:
        """
        Ensure that the provided path exists and points to a directory.
        :param path: Filesystem path that should reference a directory.
        :type path: Path
        :return: None
        :rtype: None
        """
        PathUtils.check_presence(path)
        if not path.is_dir():
            raise NotTypeDirectoryException(path.name)

    @staticmethod
    def get_filemode(path: Path) -> str:
        """
        Retrieve the POSIX file mode string for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: POSIX permission string for the path.
        :rtype: str
        """
        return filemode(path.lstat().st_mode)

    @staticmethod
    def get_count_links(path: Path) -> int:
        """
        Retrieve the number of hard links for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Number of hard links referencing the path.
        :rtype: int
        """
        return path.lstat().st_nlink

    @staticmethod
    def get_bytes_size(path: Path) -> int:
        """
        Retrieve the size in bytes for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Size of the path in bytes.
        :rtype: int
        """
        return path.lstat().st_size

    @staticmethod
    def get_last_change_time(path: Path) -> datetime:
        """
        Retrieve the last change timestamp for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Datetime of the last metadata change.
        :rtype: datetime
        """
        return datetime.fromtimestamp(path.lstat().st_ctime)

    @staticmethod
    def get_owner(path: Path) -> str:
        """
        Retrieve the owner name for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Owner of the filesystem path.
        :rtype: str
        """
        return path.owner(follow_symlinks=False)

    @staticmethod
    def get_group(path: Path) -> str:
        """
        Retrieve the group name for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Group owning the filesystem path.
        :rtype: str
        """
        return path.group(follow_symlinks=False)

    @staticmethod
    def get_path_name(path: Path) -> str:
        """
        Retrieve the name component for the path.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Final path component as a string.
        :rtype: str
        """
        PathUtils.check_presence(path)
        return path.name

    @staticmethod
    def get_cwd():
        """
        Retrieve the current working directory.
        :return: Current working directory path.
        :rtype: Path
        """
        return Path.cwd()

    @staticmethod
    def get_resolved_path(path: Path) -> Path:
        """
        Resolve the provided path to an absolute form.
        :param path: Filesystem path to resolve.
        :type path: Path
        :return: Resolved absolute path.
        :rtype: Path
        """
        path = path.resolve()
        return path

    @staticmethod
    def is_absolute(path: Path):
        """
        Determine whether the path is absolute.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Flag indicating whether the path is absolute.
        :rtype: bool
        """
        return path.is_absolute()

    @staticmethod
    def get_directory_content(path: Path) -> list[Path]:
        """
        Retrieve the content listing for a directory.
        :param path: Directory path to inspect.
        :type path: Path
        :return: List of paths contained within the directory.
        :rtype: list[Path]
        """
        return list(path.iterdir())

    @staticmethod
    def copy_file(src_path: Path, dest_path: Path) -> None:
        """
        Copy a file from the source path to the destination path.
        :param src_path: Source file path.
        :type src_path: Path
        :param dest_path: Destination file path.
        :type dest_path: Path
        :return: None
        :rtype: None
        """
        shutil.copy(src_path, dest_path)

    @staticmethod
    def copytree(src_path: Path, dest_path: Path) -> None:
        """
        Copy a directory tree from source to destination.
        :param src_path: Source directory path.
        :type src_path: Path
        :param dest_path: Destination directory path.
        :type dest_path: Path
        :return: None
        :rtype: None
        """
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)

    @staticmethod
    def is_file(path: Path) -> bool:
        """
        Determine whether the path references a file.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Flag indicating if the path is a file.
        :rtype: bool
        """
        return path.is_file()

    @staticmethod
    def is_directory(path: Path) -> bool:
        """
        Determine whether the path references a directory.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Flag indicating if the path is a directory.
        :rtype: bool
        """
        return path.is_dir()

    @staticmethod
    def is_path_exists(path: Path) -> bool:
        """
        Determine whether the path exists on the filesystem.
        :param path: Filesystem path to inspect.
        :type path: Path
        :return: Flag indicating if the path exists.
        :rtype: bool
        """
        return path.exists(follow_symlinks=False)

    @staticmethod
    def check_readable(path: Path) -> None:
        """
        Ensure that the path is readable by the current user.
        :param path: Filesystem path to validate.
        :type path: Path
        :return: None
        :rtype: None
        """
        if not os.access(path, os.R_OK):
            raise NotAccessToReadException(str(path))

    @staticmethod
    def check_writable(path: Path) -> None:
        """
        Ensure that the path is writable by the current user.
        :param path: Filesystem path to validate.
        :type path: Path
        :return: None
        :rtype: None
        """
        if not os.access(path, os.W_OK):
            raise NotAccessToWriteException(str(path))

    @staticmethod
    def move(src: Path, dest: Path) -> None:
        """
        Move a filesystem entry from the source path to the destination path.
        :param src: Source filesystem path.
        :type src: Path
        :param dest: Destination filesystem path.
        :type dest: Path
        :return: None
        :rtype: None
        """
        shutil.move(src, dest)

    @staticmethod
    def remove(src: Path) -> None:
        """
        Remove the filesystem entry at the provided path.
        :param src: Filesystem path to remove.
        :type src: Path
        :return: None
        :rtype: None
        """
        src.unlink()

    @staticmethod
    def mkdir(path: Path, ok_exists: bool) -> None:
        """
        Create a directory at the provided path.
        :param path: Directory path to create.
        :type path: Path
        :param ok_exists: Flag indicating whether existing directories are allowed.
        :type ok_exists: bool
        :return: None
        :rtype: None
        """
        path.mkdir(exist_ok=ok_exists)

    @staticmethod
    def check_root_directory(path: Path) -> None:
        """
        Ensure that the path resides within the user's home directory.
        :param path: Filesystem path to validate.
        :type path: Path
        :return: None
        :rtype: None
        """
        path = PathUtils.get_resolved_path(path)
        if not path.is_relative_to(Path.home()):
            raise NotEnoughPermissionToRemoveException(str(path))

    @staticmethod
    def create_tar_archive(archive_name: str, files: list[Path]) -> None:
        """
        Create a gzipped tar archive from the provided files.
        :param archive_name: Name of the archive to create.
        :type archive_name: str
        :param files: Files to include in the archive.
        :type files: list[Path]
        :return: None
        :rtype: None
        """
        with tarfile.open(archive_name, "w:gz") as tar:
            for file in files:
                tar.add(file, arcname=file.name)

    @staticmethod
    def untar_archive(archive_name: str) -> None:
        """
        Extract the contents of a gzipped tar archive.
        :param archive_name: Name of the archive to extract.
        :type archive_name: str
        :return: None
        :rtype: None
        """
        with tarfile.open(archive_name, "r:gz") as tar:
            tar.extractall()

    @staticmethod
    def create_zip_archive(archive_name: str, files: list[Path]) -> None:
        """
        Create a ZIP archive from the provided files.
        :param archive_name: Name of the archive to create.
        :type archive_name: str
        :param files: Files to include in the archive.
        :type files: list[Path]
        :return: None
        :rtype: None
        """
        with zipfile.ZipFile(archive_name, "w") as zip:
            for file in files:
                zip.write(file, arcname=file.name)

    @staticmethod
    def unzip_archive(archive_name: str) -> None:
        """
        Extract the contents of a ZIP archive.
        :param archive_name: Name of the archive to extract.
        :type archive_name: str
        :return: None
        :rtype: None
        """
        with zipfile.ZipFile(archive_name, "r") as zip:
            zip.extractall()

    @staticmethod
    def get_all_files_in_path(path: Path) -> list[Path]:
        return list(
            [cur_path for cur_path in path.rglob("*") if cur_path.is_file()]
        )