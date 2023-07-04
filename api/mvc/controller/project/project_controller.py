import os
import re
from typing import Optional

from api.mvc.controller.aspect.i_aspect_controller import IAspectController
from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.service.data.project_service import ProjectService
from api.mvc.model.service.file.pom_service import PomService

from api.mvc.view.project_view import ProjectView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.helper.string_helper import StringHelper
from api_core.mvc.controller.controller import Controller


class ProjectController(Controller, IProjectController):
    """
    Controller class used to manage API projects.
    """

    def __init__(self):
        """
        Initialize a new instance of ProjectController class.
        """
        super().__init__("project", ProjectService(), ProjectView(ConstantHelper.SCREEN_SIZE))
        self.__ps: PomService = PomService()
        self.__cmc: Optional[IContentModelController] = None
        self.__ac: Optional[IAspectController] = None

    @property
    def aspect_controller(self) -> IAspectController:
        return self.__ac

    @aspect_controller.setter
    def aspect_controller(self, value: IAspectController):
        self.__ac = value

    @property
    def content_model_controller(self):
        return self.__cmc

    @content_model_controller.setter
    def content_model_controller(self, value: IContentModelController):
        self.__cmc = value

    def new(self):
        """
        Create a new Alfresco AIO project in the current directory.
        """
        ps: ProjectService = self._service
        pv: ProjectView = self._view

        self._view.info("Creation of an Alfresco All-In-One project.", True)

        # Retrieve and verify the data necessary for the creation of the project.
        self._view.empty()
        (sdk, group_id, artifact_id) = pv.enter_project_data()
        self._view.empty()

        # Check the sdk.
        self.__check_sdk(sdk)
        # Check the group id
        self.__check_group_id(group_id)
        # Check the artifact id.
        self.__check_artifact_id(artifact_id)

        # Creation of the project.
        result: tuple[int, str, str] = ps.new(sdk, group_id, artifact_id)

        # Checking the result of project creation.
        if result[0].__ne__(0):
            raise ApiException("An error occurred while creating the project via maven. Here is the error:\n{0}."
                               .format(result[1].decode('UTF-8')))

        self._view.success("Alfresco All-In-one project '{0}.{1}' created with SDK version {2}."
                           .format(group_id, artifact_id, sdk))
        self.raz(self.get_project(artifact_id, False))

    def get_project(self, artifact_id: Optional[str] = None, verbose: bool = True) -> ProjectModel:
        """
        Retrieves the data model of an Alfresco AIO project.
        :param artifact_id: The artifact id of the Alfresco AIO project.
        :param verbose: Indicates whether notification messages are displayed or not.
        :return: The data model of an Alfresco AIO project.
        """
        if verbose:
            self._view.info("Retrieving the project data model.")

        project_path: str = os.getcwd() if artifact_id is None else "{1}{0}{2}".format(os.sep, os.getcwd(), artifact_id)
        pom_path: str = "{1}{0}pom.xml".format(os.sep, project_path)

        # Verification that the project folder exists.
        if not FileFolderHelper.is_folder_exists(project_path):
            raise ApiException("The AIO project folder does not exist.")

        # Verification that the folder contains a pom.xml file.
        elif not FileFolderHelper.is_file_exists(pom_path):
            raise ApiException("The working directory is not an Alfresco project folder.")

        return ProjectModel(self.__ps.extract_sdk(pom_path), self.__ps.extract_group_id(pom_path),
                            self.__ps.extract_artifact_id(pom_path), project_path)

    @staticmethod
    def __check_sdk(value: str):
        """
        Check if the SDK value in parameter is valid otherwise it raises an exception.
        :param value: The SDK value.
        """
        # Check if it's empty.
        if StringHelper.is_empty(value):
            raise ApiException("The SDK version of the AIO project cannot be null or empty.")

        # Check if it has space.
        elif StringHelper.has_space(value):
            raise ApiException("The SDK version of the AIO project cannot contain spaces.")

        # Check if it has a good version.
        elif re.match("(?:(\d+\.(?:\d+\.)*\d+))", value) is None:
            raise ApiException("The SDK version of the AIO project is invalid (example of valid one: 3.4.0).")

    @staticmethod
    def __check_group_id(value: str):
        """
        Check if the group_id value in parameter is valid otherwise it raises an exception.
        :param value: The SDK value.
        """
        # Check if it's empty.
        if StringHelper.is_empty(value):
            raise ApiException("The group id of the AIO project cannot be null or empty.")

        # Check if it has space.
        elif StringHelper.has_space(value):
            raise ApiException("The group id of the AIO project cannot contain spaces.")

        # Check if it has a good version.
        elif re.match("[a-z0-9\-]+$", value) is None:
            raise ApiException("The group id cannot contain special characters or upper case  "
                               "(example of group id name: 'conseil-departemental-59').")

    @staticmethod
    def __check_artifact_id(value: str):
        """
        Check if the artifact id value in parameter is valid otherwise it raises an exception.
        :param value: The artifact id value.
        """
        # Check if it's empty.
        if StringHelper.is_empty(value):
            raise ApiException("The artifact id of the AIO project cannot be null or empty.")

        # Check if it has space.
        elif StringHelper.has_space(value):
            raise ApiException("The artifact id of the AIO project cannot contain spaces.")

        # Check that there are no special characters.
        elif re.match("[a-z0-9\-]+$", value) is None:
            raise ApiException("The AIO project artifact ID cannot contain special characters or upper case (example "
                               "of a valid artifact id name: 'display-of-acts').")

    def load(self):
        """
        Loads and generates the necessary project files.
        """
        project: ProjectModel = self.get_project(None, False)
        service: ProjectService = self._service
        self._view.info("Loading project '{0}'.".format(project.artifact_id))
        # Verify that the folder exists.
        if not FileFolderHelper.is_folder_exists(project.content_model_folder):
            raise ApiException("The folder that contain the content model files does not exist ({0})."
                               .format(project.content_model_relative_folder_path))
        # Loading content-models.
        for content in FileFolderHelper.list_folder(project.content_model_folder):
            project.add_content_model(self.__cmc.load_content_model(
                project, "{0}{1}{2}".format(project.content_model_folder, os.sep, content)))

        self._view.success("The project '{0}' has been loaded successfully.".format(project.artifact_id))

        # Project reset.
        self.reset()

        # Display on the output console of the file writing message.
        self._view.info("File generation")
        for content_model in project.content_models:
            self.__cmc.generate_platform_message_file(content_model)
            self.__cmc.add_content_model_in_bootstrap(project, content_model)

            self.__cmc.generate_share_message_file(project, content_model)

        for content_model in project.content_models:
            for aspect in content_model.aspects:
                self.__ac.add_aspect_in_share_config_file(project, content_model, aspect)

        for content_model in project.content_models:
            for aspect in content_model.aspects:
                self.__ac.add_aspect_properties_in_share_config_file(project, aspect)

    def reset(self):
        project: ProjectModel = self.get_project(None, False)
        self._view.info("Resetting project {0}.".format(project.artifact_id), True)
        service: ProjectService = self._service
        service.reset(project)
        self._view.success("Successfully reset project '{0}'.".format(project.artifact_id))

    def raz(self, project: Optional[ProjectModel] = None):
        if project is None:
            project = self.get_project(None, False)
        self._view.info("Complete reset of the project '{0}'.".format(project.artifact_id), True)
        service: ProjectService = self._service
        service.raz(project)
        self._view.success("Complete reset of project '{0}' was completed with success.".format(project.artifact_id))
