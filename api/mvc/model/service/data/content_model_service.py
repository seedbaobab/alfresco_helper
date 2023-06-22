import os
from abc import ABC
from typing import Optional

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.service.model.service import Service


class ContentModelService(Service, ABC):
    """
    Class providing services for managing project's content-model.
    """

    def __init__(self, api_template_folder: str):
        """
        Initialize a new instance of ContentModelService class.
        """
        super().__init__("model")
        self.__cmfs: ContentModelFileService = ContentModelFileService()
        self.__content_model_template_filepath: str = "{0}{1}content_model_template".format(api_template_folder, os.sep)

    def new(self, project: ProjectModel, prefix: str, name: str, description: Optional[str], author: Optional[str]) \
            -> ContentModel:
        # Setting the absolute path to the content model file.
        filepath: str = "{0}{1}{2}".format(project.content_model_folder, os.sep,
                                           "{0}.xml".format(name) if name.endswith("model") else
                                           "{0}-model.xml".format(name))

        # FileFolderHelper.write_file(filepath, FileFolderHelper.read_file(self.__content_model_template_filepath)
        #                             .format(prefix=prefix, name=name, upper_case_name=name.upper()))

        self.__cmfs.create_content_model(filepath, prefix, name, description, author)

        return ContentModel(prefix, name, filepath)

    def is_prefix_exists(self, project: ProjectModel, prefix: str) -> tuple[bool, Optional[str]]:
        """
        Checks if the prefix is already present in a content model definition file. It returns a tuple composed of a
        boolean of true and the name of the file if the file exists, otherwise false and None.
        :param project: A data model for the project.
        :param prefix: The content model prefix.
        :return: A tuple composed of a boolean of true and the name of the file if the file exists, otherwise false
        and None.
        """
        contents: list[str] = FileFolderHelper.get_contents(project.content_model_folder)

        index: int = 0
        cm_name: Optional[str] = None
        maximum: int = len(contents)

        while index.__lt__(maximum) and cm_name is None:
            if self.__cmfs.extract_prefix("{1}{0}{2}".format(os.sep, project.content_model_folder, contents[index])) \
                    .__eq__(prefix):
                cm_name = contents[index]
            else:
                index += 1

        return index.__lt__(maximum), cm_name

    def is_name_exists(self, project: ProjectModel, name: str) -> tuple[bool, Optional[str]]:
        """
        Checks if the prefix is already present in a content model definition file. It returns a tuple composed of a
        boolean of true and the name of the file if the file exists, otherwise false and None.
        :param project: A data model for the project.
        :param name: The content model name.
        :return: A tuple composed of a boolean of true and the name of the file if the file exists, otherwise false
        and None.
        """
        contents: list[str] = FileFolderHelper.get_contents(project.content_model_folder)

        index: int = 0
        cm_name: Optional[str] = None
        maximum: int = len(contents)

        while index.__lt__(maximum) and cm_name is None:
            if self.__cmfs.extract_name("{1}{0}{2}".format(os.sep, project.content_model_folder, contents[index])) \
                    .__eq__(name):
                cm_name = contents[index]
            else:
                index += 1

        return index.__lt__(maximum), cm_name

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()

    def __new_manual(self):
        """
        Add the new content-model command in manual.
        """
        self._ms.new_manual("new", "Create a new content model.")
        self._ms.add_call()
        self._ms.save()
