from __future__ import annotations

from api_core.exception.api_exception import ApiException
from api_core.mvc.service.data.manual_argument_model import ManualArgumentModel
from api_core.mvc.service.data.manual_call_model import ManualCallModel
from api_core.mvc.service.data.manual_model import ManualModel


class ManualService:
    """
    Manual management class.
    """

    def __init__(self, name: str):
        """
       Initialize a new instance of 'ManualService' class.
       :param name: The service name.
        """
        self.__service_name: str = name
        self.__manual_template: str = "{0}_{1}"
        self.__buffer: ManualModel | None = None
        self.__manuals: dict[str, ManualModel] = {}

    def save(self):
        """
        Save the input manual in the library.
        """
        if self.__buffer is None:
            raise ApiException("You haven't entered a manual.")
        self.__manuals[self.__buffer.name] = self.__buffer
        self.__buffer = None

    def new_manual(self, name: str, description: str):
        """
        Initialize a new manual.
        :param name: The name of the command.
        :param description: The description of the command.
        """
        if self.__buffer is not None:
            raise ApiException("The last manual created '{0}' was not added.".format(self.__buffer.name))
        self.__buffer: ManualModel = ManualModel(self.__manual_template.format(name, self.__service_name), description)

    def add_call(self):
        """
        Add a call definition to the command.
        """
        if self.__buffer is None:
            raise ApiException("You must create a new manual to add a call.")
        self.__buffer.add_call(ManualCallModel())

    def add_argument(self, name: str, description: str, typology: str):
        """
        Add an argument to the last call of the added command.
        :param name: The name of the argument.
        :param description: The description of the argument.
        :param typology: The type of the argument.
        """
        if self.__buffer is None:
            raise ApiException("You must create a new manual and at least one call to be able to add an argument.")
        elif len(self.__buffer.calls).__eq__(0):
            raise ApiException("You must create a new call to add an argument.")
        index: int = len(self.__buffer.calls) - 1
        self.__buffer.calls[index].add_argument(ManualArgumentModel(name, description, typology))

    def is_command_valid(self, command: str, arguments: list[str]) -> bool:
        """
        Checks if a command is valid.
        :param command: The command to check.
        :param arguments: The arguments accompanying the command.
        :return: True if the command exists in the service otherwise False.
        """
        (exists, manual) = self.is_command_exists(self.__manual_template.format(command, self.__service_name))
        if not exists:
            return False
        index: int = 0
        maximum: int = len(manual.calls)
        while index.__lt__(maximum) and len(manual.calls[index].arguments).__ne__(len(arguments)):
            index += 1
        return index.__lt__(maximum)

    def is_command_exists(self, manuel: str) -> tuple[bool, ManualModel | None]:
        """
        Indicates whether the manual for an order exists in the service.
        :param manuel: The requested manual.
        :return: True if the manual exists otherwise false.
        """
        return (True, self.__manuals[manuel]) if manuel in self.__manuals.keys() else (False, None)

    def get_manual(self, command: str):
        """
        Get the definition from one or all manual.
        :param command: The name of the manual to retrieve.
        :return: The manual definition requested.
        """
        if command is None:
            manuals: list[ManualModel] = []
            for key in self.__manuals.keys():
                manuals.append(self.__manuals[key])
            return manuals
        return self.__manuals.get(self.__manual_template.format(command, self.__service_name))
