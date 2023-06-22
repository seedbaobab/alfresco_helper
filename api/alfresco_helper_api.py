from abc import ABC

from api.mvc.controller.aspect.aspect_controller import AspectController
from api.mvc.controller.content_model.content_model_controller import ContentModelController
from api.mvc.controller.project.project_controller import ProjectController
from api_core.exception.api_exception import ApiException
from api_core.api import Api


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
        pc: ProjectController = ProjectController()
        cmc: ContentModelController = ContentModelController(pc, self.template_folder)

        self.service.add(pc)
        self.service.add(cmc)

    def _execute(self, controller: str, command: str, arguments: list[str]):
        """
        Execute the command.
        :param controller: The name of the controller.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        if controller.__eq__("project"):
            self.__execute_project_command(command, arguments)
        elif controller.__eq__("model"):
            self.__execute_model_command(command, arguments)

    def __execute_aspect_command(self, command: str, arguments: list[str]):
        """
        Interpret the command for an aspect.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        controller: AspectController = self.service.get("aspect")

        # Create a new content-model.
        if command.__eq__("new"):
            controller.new(arguments[0])

        # Access to the model commands manual.
        elif command.__eq__("man"):
            if len(arguments).__eq__(1):
                controller.man(arguments[0])
            elif len(arguments).__eq__(0):
                controller.man()
        else:
            raise ApiException("The command '{0}_{1}' has been defined but not implemented.".format(command, "project"))

    def __execute_model_command(self, command: str, arguments: list[str]):
        """
        Interpret the command for a content-model.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        controller: ContentModelController = self.service.get("model")

        # Create a new content-model.
        if command.__eq__("new"):
            controller.new()

        # Access to the model commands manual.
        elif command.__eq__("man"):
            if len(arguments).__eq__(1):
                controller.man(arguments[0])
            elif len(arguments).__eq__(0):
                controller.man()
        else:
            raise ApiException("The command '{0}_{1}' has been defined but not implemented.".format(command, "project"))

    def __execute_project_command(self, command: str, arguments: list[str]):
        """
        Interpret the command for a project.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        controller: ProjectController = self.service.get("project")

        # Create a new project.
        if command.__eq__("new"):
            controller.new()

        # Access to the project orders manual.
        elif command.__eq__("man"):
            if len(arguments).__eq__(1):
                controller.man(arguments[0])
            elif len(arguments).__eq__(0):
                controller.man()
        else:
            raise ApiException("The command '{0}_{1}' has been defined but not implemented.".format(command, "project"))