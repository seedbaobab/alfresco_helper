from abc import ABC

from api.mvc.controller.project.project_controller import ProjectController
from api_core.api import Api
from api_core.exception.api_exception import ApiException


class AlfrescoHelperApi(Api, ABC):
    """
    Class for the AlfrescoHelper API.
    """

    def __init__(self, path_to_api_folder: str):
        super().__init__(path_to_api_folder, "Alfresco Helper v1.0.0")

    def init_controllers(self):
        """
        Initialize the list of controllers
        """
        self.service.add(ProjectController())

    def _execute(self, controller: str, command: str, arguments: list[str]):
        """
        Execute the command.
        :param controller: The name of the controller.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        if controller.__eq__("project"):
            self.__execute_project_command(command, arguments)

    def __execute_project_command(self, command: str, arguments: list[str]):
        """
        Interpret the command for a project.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        controller: ProjectController = self.service.get("project")

        if command.__eq__("new"):
            controller.new()

        elif command.__eq__("man"):

            if len(arguments).__eq__(1):
                controller.man(arguments[0])

            elif len(arguments).__eq__(0):
                controller.man()
        else:
            raise ApiException("The command '{0}_{1}' has been defined but not implemented.".format(command, "project"))
