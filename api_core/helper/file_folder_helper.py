from __future__ import annotations

import os

from api_core.exception.api_exception import ApiException


class FileFolderHelper:
    """
    Helper class for files and folders.
    """

    @staticmethod
    def list_folder(path: str) -> list[str]:
        """
        List the contents of a folder.
        :param path: The absolute path to the folder.
        :return: The list of folder contents.
        """
        if not FileFolderHelper.is_folder_exists(path):
            raise ApiException("The folder whose contents must be listed ({0}) does not exist.".format(path))
        return os.listdir(path)

    @staticmethod
    def extract_folder_from_filepath(filepath: str) -> str:
        """
        Extract the path to the file folder.
        :param filepath: The path to the file.
        :return: The path to the file folder.
        """
        return filepath.rsplit(os.sep, 1)[0]

    @staticmethod
    def extract_filename_from_path(filepath: str) -> str:
        return filepath.rsplit(os.sep, 1)[1]

    @staticmethod
    def is_file_exists(file_path: str) -> bool:
        """
        Check if the file exists.
        :param file_path: The file path to check.
        :return: True if the file exists otherwise false.
                """
        return True if (os.path.exists(file_path) and os.path.isfile(file_path)) else False

    @staticmethod
    def is_folder_exists(folder_path: str) -> bool:
        """
        Checks if a folder exists.
        :param folder_path: The path to the folder to test.
        :return: True if the folder exists otherwise false.
        """
        return True if (os.path.exists(folder_path) and os.path.isdir(folder_path)) else False

    @staticmethod
    def create_folder(folder_path: str):
        """
        Create a folder if possible.
        :param folder_path: The path of the folder to create.
        """
        if not FileFolderHelper.is_folder_exists(folder_path):
            os.makedirs(folder_path)

    @staticmethod
    def write_file(file_path_destination: str, content: str | None):
        """
        Rewrite a file or create it.
        :param file_path_destination: The destination path of the file.
        :param content: The contents of the file.
        """
        if content is not None:
            with open(file_path_destination, "w") as writer:
                writer.write(content)

    @staticmethod
    def read_file(file_path_source: str) -> str | None:
        """
        Read a file.
        :param file_path_source: The source path of the file.
        :return: The content of the file
        """
        if FileFolderHelper.is_file_exists(file_path_source):
            with open(file_path_source, "r") as reader:
                content = reader.read()
            return content
        return None

    @staticmethod
    def is_folder_has_files(folder_path: str) -> bool:
        """
        Indicates whether a folder has content.
        :param folder_path: The path to the folder to check.
        :return: True if the folder has content otherwise False.
        """
        if not FileFolderHelper.is_folder_exists(folder_path):
            return False
        return True if len(os.listdir(folder_path)).__gt__(0) else False

    @staticmethod
    def get_contents(folder_path) -> list[str]:
        """
        Retrieve the contents of a folder.
        :param folder_path: The path of the folder whose contents we want to retrieve.
        :return: An array containing file names.
        """
        return [] if not FileFolderHelper.is_folder_exists(folder_path) else os.listdir(folder_path)
