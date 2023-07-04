import os
import re
from abc import ABC
from typing import Optional

from api.mvc.controller.aspect.i_aspect_controller import IAspectController
from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.service.file.bootstrap_service import BootstrapFileService
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api.mvc.model.service.data.content_model_service import ContentModelService
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.model.service.file.share_slingshot_app_context import ShareSlingshotApplicationContext
from api_core.helper.file_folder_helper import FileFolderHelper
from api.mvc.view.content_model_view import ContentModelView
from api_core.helper.constant_helper import ConstantHelper
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel
from api_core.exception.api_exception import ApiException
from api_core.mvc.controller.controller import Controller
from api_core.helper.string_helper import StringHelper


class ContentModelController(Controller, IContentModelController, ABC):
    """
    Controller class used to manage API project's content-model.
    """

    def __init__(self, pc: IProjectController, api_template_folder: str):
        """
        Initialize a new instance of ProjectController class.
        :param pc: A project controller.
        :param api_template_folder: The template folder path.
        """
        super().__init__("model", ContentModelService(api_template_folder),
                         ContentModelView(ConstantHelper.SCREEN_SIZE))
        self.__pc: IProjectController = pc
        self.__as: Optional[IAspectController] = None
        self.__bfs: BootstrapFileService = BootstrapFileService()
        self.cmfs: ContentModelFileService = ContentModelFileService()

    @property
    def aspect_controller(self) -> IAspectController:
        return self.__as

    @aspect_controller.setter
    def aspect_controller(self, value: IAspectController):
        self.__as = value

    def new(self):
        """
        Attempts to create a new content model in the project.
        """
        vw: ContentModelView = self._view
        service: ContentModelService = self._service

        # Get and check of the project.
        project: ProjectModel = self.__pc.get_project()

        vw.info("Create of a content model.")
        (prefix, name, description, last_name, first_name) = vw.enter_content_model_data()

        # Verification of the validity of the prefix.
        self.__check_prefix(prefix)
        (prefix_exists, cm_file) = service.is_prefix_exists(project, prefix)
        if prefix_exists:
            raise ApiException("The prefix is already used in the content model file '{0}'.".format(cm_file))

        # Verification of the validity of the name.
        self.__check_name(name)
        (name_exists, cm_file) = service.is_name_exists(project, prefix)
        if name_exists:
            raise ApiException("The name is already used in the content model file '{0}'.".format(cm_file))

        # Creation of the content model.
        content_model: ContentModel = service.new(project, prefix, name, description,
                                                  self.__format_author(last_name, first_name))

        vw.success("The content model '{0}' has been created successfully in '{1}'."
                   .format(content_model.complete_name,
                           FileFolderHelper.extract_filename_from_path(content_model.path)))
        self.__pc.load()

    def get_content_model(self, project: ProjectModel, content_model: str, verbose: bool = True) -> ContentModel:
        """
        Retrieves the data model of an Alfresco AIO project.
        :param project: The content-model's project.
        :param content_model: The content-model complete name (prefix:name) of the Alfresco AIO project.
        :param verbose: Indicates whether notification messages are displayed or not.
        :return: The data model of an Alfresco AIO project.
        """
        if verbose:
            self._view.info("Retrieving the content-model data model.")

        name: str = self.__extract_name(content_model)
        prefix: str = self.__extract_prefix(content_model)
        (content_model_exists, filepath) = self.__is_content_model_exists(project, prefix, name)

        if not content_model_exists:
            raise ApiException("There is no content-model named '{0}' in the project.".format(content_model))

        if verbose:
            self._view.success("Content-model '{0}' was successfully retrieved.".format(content_model))

        return ContentModel(project, prefix, name, filepath)

    def load_content_model(self, project: ProjectModel, content_model_file_path: str) -> ContentModel:
        """
        Loads a content model by its file.
        :param project: The content-model's project.
        :param content_model_file_path: The absolute path to the content model file.
        :return: The data model of an Alfresco AIO project.
        """
        prefix: str = self.cmfs.extract_content_model_prefix(content_model_file_path)
        name: str = self.cmfs.extract_content_model_name(content_model_file_path)

        self._view.info("Loading content model '{0}:{1}'.".format(prefix, name))
        content_model: ContentModel = self.get_content_model(project, "{0}:{1}".format(prefix, name), False)
        for aspect in self.cmfs.get_aspects_name(content_model):
            content_model.add_aspect(self.__as.load_aspect(content_model, aspect))

        self._view.success("Content model '{0}' (from '{1}') was loaded successfully."
                           .format(content_model.complete_name,
                                   FileFolderHelper.extract_filename_from_path(content_model.path)))
        return content_model

    def generate_platform_message_file(self, content_model: ContentModel):
        # File name retrieval for error message purposes.
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.platform_message_file_path)
        # Display on the output console of an appropriate message.
        self._view.info("Generating message file '{0}' from content model '{1}'."
                        .format(filename, content_model.complete_name))
        #
        content: str = "# This file must contain tags from the content model '{0}' ('{1}')\n\n" \
            .format(content_model.name, content_model.complete_name)

        # Retrieval of aspect properties.
        for aspect in content_model.aspects:
            content += self.__as.get_aspect_definition_platform_message_file(content_model, aspect)

        # Writing file.
        if len(content_model.aspects).__gt__(0):
            FileFolderHelper.write_file(content_model.platform_message_file_path, content)
            self._view.success("Generation of message file '{0}' for content model '{1}' was successful."
                               .format(filename, content_model.complete_name))
        else:
            self._view.warning("No file '{0}' generated because the content model is empty.".format(filename))

    def add_share_file_message_labels(self, project: ProjectModel, content_model: ContentModel):
        """
        Adds the content model to the bootstrap file.
        :param project: The content-model's project.
        :param content_model: The content-model complete name of the Alfresco AIO project.
        """
        service: ContentModelService = self._service
        destination_filename: str = FileFolderHelper.extract_filename_from_path(
            project.share_slingshot_application_context_filepath)
        source_filename: str = FileFolderHelper.extract_filename_from_path(content_model.share_message_file_path)
        self._view.info("Adding message file '{0}' to file '{0}'.".format(source_filename, destination_filename))
        service.add_share_file_message_labels(project, content_model)
        self._view.success("Adding message file '{0}' to file '{1}' was successful."
                           .format(source_filename, destination_filename))

    def add_content_model_in_bootstrap(self, project: ProjectModel, content_model: ContentModel):
        """
        Adds the content model to the bootstrap file.
        :param project: The content-model's project.
        :param content_model: The content-model complete name of the Alfresco AIO project.
        """
        self._view.info("Adding content model '{0}' in bootstrap file.".format(content_model.complete_name))
        # Added content model in bootstrap file.
        self.__bfs.add_content_model(project, content_model)
        # Added content model 'message' file in bootstrap file.
        if FileFolderHelper.is_file_exists(content_model.platform_message_file_path):
            self.__bfs.add_message_content_model(project, content_model)
        self._view.success(
            "Successfully added content model '{0}' to bootstrap file.".format(content_model.complete_name))

    def generate_share_message_file(self, project: ProjectModel, content_model: ContentModel):
        # File name retrieval for error message purposes.
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.share_message_file_path)
        # Display on the output console of an appropriate message.
        self._view.info("Generating share message file '{0}' from content model '{1}'."
                        .format(filename, content_model.complete_name))
        #
        content: str = "# Content-model '{0}' ('{1}')\n\n".format(content_model.name, content_model.complete_name)

        # Retrieval of aspect properties.
        for aspect in content_model.aspects:
            content += self.__as.get_aspect_definition_share_message_file(content_model, aspect)

        # Writing file.
        if len(content_model.aspects).__gt__(0):
            FileFolderHelper.write_file(content_model.share_message_file_path, content)
            self._view.success("Generating share message file '{0}' for content model '{1}' was successful."
                               .format(filename, content_model.complete_name))

            self.add_share_file_message_labels(project, content_model)
        else:
            self._view.warning("No file '{0}' generated because the content model is empty.".format(filename))

    def __is_content_model_exists(self, project: ProjectModel, prefix: str, name: str) -> tuple[bool, str]:
        """
        Checks in the project if the content model identified by its full name exists within it.
        :param project: The content model's project data model.
        :param prefix: The content model prefix.
        :param name:The content model name.
        :return: A tuple consisting of a boolean indicating whether the content model exists, and the name of the file
         defining it or None.
        """
        contents: list[str] = FileFolderHelper.get_contents(project.content_model_folder)
        index: int = 0
        cm_filepath: Optional[str] = None
        maximum: int = len(contents)
        while index.__lt__(maximum) and cm_filepath is None:
            filepath: str = "{0}{1}{2}".format(project.content_model_folder, os.sep, contents[index])
            if prefix.__eq__(self.cmfs.extract_content_model_prefix(filepath)) and \
                    name.__eq__(self.cmfs.extract_content_model_name(filepath)):
                cm_filepath = filepath
            else:
                index += 1
        return index.__lt__(maximum), cm_filepath

    @staticmethod
    def __check_prefix(value: str):
        """
        Verifies that the prefix put in parameter is valid; otherwise it throws an ApiException.
        :param value: The prefix to test.
        """
        # Verification that it is not empty or null.
        if StringHelper.is_empty(value):
            raise ApiException("The content model prefix cannot be null or empty.")

        # Check that there are no spaces.
        elif StringHelper.has_space(value):
            raise ApiException("The content model prefix cannot contain spaces.")

        # Check that there are no special characters.
        elif re.match("[a-z0-9]+$", value) is None:
            raise ApiException("The content model prefix cannot contain any special or uppercase characters."
                               " (example of a valid content-model prefix: 'acme').")

    @staticmethod
    def __format_author(last_name: str, firstname: str) -> Optional[str]:
        """
        Format data about the author of the content model.
        :param last_name: The author's last name.
        :param firstname: The author's first name.
        :return: The author's name formatted.
        """
        result: Optional[str] = None
        if not StringHelper.is_empty(last_name):
            result = last_name.upper()
        if not StringHelper.is_empty(firstname):
            if result is not None:
                result += " {0}".format(firstname.title())
            else:
                result = firstname.title()
        return result

    @staticmethod
    def __check_name(value: str):
        """
        Verifies that the name put in parameter is valid; otherwise it throws an ApiException.
        :param value: The name to test.
        """
        # Verification that it is not empty or null.
        if StringHelper.is_empty(value):
            raise ApiException("The content model name cannot be null or empty.")

        # Check that there are no spaces.
        elif StringHelper.has_space(value):
            raise ApiException("The content model name cannot contain spaces.")

        # Check that there are no special characters.
        elif re.match("[a-zA-Z0-9]+$", value) is None:
            raise ApiException("The content model name cannot contain any special"
                               " (example of a valid content-model name: 'contentModel').")

    def __extract_name(self, content_model: str) -> str:
        """
        Extracts the name from the full name of a content model.
        :param content_model: The full name of a content model.
        :return: The name from the full name of a content model
        """""
        content_model_decomposed: list[str] = content_model.rsplit(":", 1)
        # Checking content model name composition.
        if len(content_model_decomposed).__ne__(2):
            raise ApiException("The content model name is invalid. It must consist of two elements as follows: "
                               "prefix:name.")
        # Prefix retrieval.
        name: str = content_model_decomposed[1]
        # Check the name.
        self.__check_name(name)
        # Return of the result.
        return name

    def __extract_prefix(self, content_model: str) -> str:
        """
        Extracts the prefix from the full name of a content model.
        :param content_model: The full name of a content model.
        :return: The prefix from the full name of a content model
        """""
        content_model_decomposed: list[str] = content_model.rsplit(":", 1)
        # Checking content model name composition.
        if len(content_model_decomposed).__ne__(2):
            raise ApiException("The content model name is invalid. It must consist of two elements as follows: "
                               "prefix:name.")
        # Prefix retrieval.
        prefix: str = content_model_decomposed[0]
        # Verification of the composition of the prefix.
        self.__check_prefix(prefix)
        # Return of the result.
        return prefix
