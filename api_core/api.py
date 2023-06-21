import os
from abc import ABC, abstractmethod

from api_core.helper.constant_helper import ConstantHelper
from api_core.mvc.view.view import View


class Api(ABC):
    """
    Base class for the API.
    """

    def __init__(self, path_to_api_folder: str, api_name: str):
        """
        Initialize a new instance of 'API' class.
        :param api_name: API name.
        :param path_to_api_folder: The API folder path.
        """
        # The API name.
        self._NAME: str = api_name
        #
        self._SERVICE: ControllerService = ControllerService()

        self.view: View = View(ConstantHelper.SCREEN_SIZE)

        # Initialization of application controllers.
        self.init_controllers()

    @property
    def data_folder_path(self) -> str:
        """
        Access method to instance property '_DATA_FOLDER_PATH'.
        :return: The value of the '_DATA_FOLDER_PATH' instance property.
        """
        return self._DATA_FOLDER_PATH

    @property
    def licence_folder_path(self) -> str:
        """
        Access method to instance property '_LICENCE_FOLDER_PATH'.
        :return: The value of the '_LICENCE_FOLDER_PATH' instance property.
        """
        return self._LICENCE_FOLDER_PATH

    @property
    def template_folder_path(self) -> str:
        return self._TEMPLATE_FOLDER_PATH

    @property
    def resources_folder_path(self) -> str:
        """
        Access method to instance property '_RESOURCES_FOLDER_PATH'.
        :return: The value of the '_RESOURCES_FOLDER_PATH' instance property.
        """
        return self._RESOURCES_FOLDER_PATH

    @property
    def service(self) -> ControllerService:
        """
        Access method to instance property '_SERVICE'.
        :return: The value of the '_SERVICE' instance property.
        """
        return self._SERVICE

    @abstractmethod
    def init_controllers(self):
        """
        Initialize the list of controllers
        """
        pass

    def interpret(self, tokens: list[str]):
        """
        Interprets a list of tokens.
        :param tokens: The list of tokens to interpret.
        """
        self.view.main_title(self._NAME)
        try:
            (controller, command, arguments) = self.__extract_token_datas(tokens)
            self._execute(controller, command, arguments)
        except ApiException as e1:
            self.view.exception(e1)
        self.view.end_title(self._NAME)

    @abstractmethod
    def _execute(self, controller: str, command: str, arguments: list[str]):
        """
        Execute the command.
        :param controller: The name of the controller.
        :param command: The name of the command.
        :param arguments: The list of arguments.
        """
        pass

    def __extract_token_datas(self, tokens: list[str]) -> tuple[str, str, list[str]]:
        if len(tokens).__lt__(1):
            raise ApiException("Please enter a command to execute.")
        try:
            # Data extraction.
            (controller_name, command, arguments) = (tokens[0].rsplit("_")[1], tokens[0].rsplit("_")[0], tokens[1:])
            # Checking the existence of the controller.
            if not self._SERVICE.exists(controller_name):
                raise ApiException("'{0}' is not a valid command.".format(" ".join(tokens)))
            # Verification of the validity of the command.
            controller: Controller = self._SERVICE.get(controller_name)
            if not controller.is_command_valid(command, arguments):
                raise ApiException("The '{1}_{0}' command was not called correctly. Here is the manual for it:"
                                   .format(controller_name, command), controller.get_man(command))
            return controller_name, command, arguments
        except IndexError:
            raise ApiException("The command is malformed. Normally the command should be composed like this: "
                               "[command]_[controller] [arguments]*")
