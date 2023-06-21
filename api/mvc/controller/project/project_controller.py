import re

from api.mvc.model.service.project_service import ProjectService

from api.mvc.view.project_view import ProjectView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper
from api_core.helper.string_helper import StringHelper
from api_core.mvc.controller.controller import Controller


class ProjectController(Controller):
    """
    Controller class used to manage API projects.
    """

    def __init__(self):
        """
        Initialize a new instance of ProjectController class.
        """
        super().__init__("project", ProjectService(), ProjectView(ConstantHelper.SCREEN_SIZE))

    def new(self):
        """
        Create a new Alfresco AIO project in the current directory.
        """
        ps: ProjectService = self._service
        pv: ProjectView = self._view

        self._view.info("Creation of an Alfresco All-In-One project.")

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

        # Check if it has the good version.
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

        # Check if it has the good version.
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

        # Check if it has the good version.
        elif re.match("[a-z0-9\-]+$", value) is None:
            raise ApiException("The AIO project artifact ID cannot contain special characters or upper case (example "
                               "of a valid artifact id name: 'display-of-acts').")
