from __future__ import annotations

from typing import Optional

from api_core.exception.api_exception import ApiException
from api_core.mvc.service.data.manual_model import ManualModel
from api_core.mvc.service.model.service import Service
from api_core.mvc.view.view import View


class Controller:
    """
    Base class for application controllers.
    """

    def __init__(self, name: str, service: Service, view: View):
        """
        Initialize a new instance of 'Controller' class.
        :param name: Controller name.
        """
        self._name: str = name
        self._view: View = view
        self._service: Service = service

    @property
    def name(self) -> str:
        """
        Getter of the class instance value __NAME.
        :return: The class instance value __NAME.
        """
        return self._name

    def get_man(self, command: str) -> list[ManualModel] | ManualModel:
        """
        Get the definition from one or all manual.
        :param command: The name of the manual to retrieve.
        :return: The manual definition requested.
        """
        return self._service.man(command)

    def is_command_valid(self, command: str, arguments: list[str]) -> bool:
        """
        Checks if a command is valid.
        :param command: The command to check.
        :param arguments: The arguments accompanying the command.
        :return: True if the command exists in the service otherwise False.
        """
        return self._service.is_command_valid(command, arguments)

    def man(self, command: Optional[str] = None):
        """
        print on the standard output the manual requested.
        """
        if command is None:
            manuals: list[ManualModel] = self._service.man()
            for man in manuals:
                self._view.manual(man.to_str())
        elif self._service.is_command_exists("{0}_{1}".format(command, self._name)):
            self._view.manual(self._service.man(command).to_str())
        else:
            raise ApiException("Command '{0}_{1}' does not exist".format(command, self._name))
