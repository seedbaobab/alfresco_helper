import re

from api.mvc.model.project_service import ProjectService
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
        self._view.sub_info("Create the project.")
        (sdk, group_id, artifact_id) = pv.enter_project_data()
        # todo Check the sdk.
        self.__check_sdk(sdk)
        # todo Check the group id
        # todo Check the artifact id.

    @staticmethod
    def __check_sdk(value: str):
        """
        Chek if the SDK value in parameter is valid other it raises an exception.
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
            raise ApiException("The SDK version of the AIO project is invalid (example: 3.4.0).")
