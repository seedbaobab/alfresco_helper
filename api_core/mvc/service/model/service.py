from __future__ import annotations

from abc import ABC, abstractmethod

from api_core.mvc.service.data.manual_model import ManualModel


class Service(ABC):
    """
    Base class for services.
    """

    def __init__(self, service_name: str):
        """
        Initialize a new instance of 'Service' class.
        :param: The service name.
        """
        self._ms: ManualService = ManualService(service_name)
        self.init_manual()
        self.__man_manual()

    @abstractmethod
    def init_manual(self):
        """
        Initializes the service manual.
        """
        pass

    def is_command_valid(self, command: str, arguments: list[str]) -> bool:
        """
        Checks if a command is valid.
        :param command: The command to check.
        :param arguments: The arguments accompanying the command.
        :return: True if the command exists in the service otherwise False.
        """
        return self._ms.is_command_valid(command, arguments)

    def is_command_exists(self, command: str) -> bool:
        """
        Indicates whether the manual for an order exists in the service.
        :param command: The requested command.
        :return: True if the manual exists otherwise false.
        """
        return self._ms.is_command_exists(command)[0]

    def man(self, command: str | None = None) -> list[ManualModel] | ManualModel:
        """
        Get the definition from one or all manual.
        :param command: The name of the manual to retrieve.
        :return: The manual definition requested.
        """
        return self._ms.get_manual(command)

    def __man_manual(self):
        self._ms.new_manual("man", "Display the manual for a command.")
        self._ms.add_call()
        self._ms.add_call()
        self._ms.add_argument("command", "The manual command to display.", "str")
        self._ms.save()
