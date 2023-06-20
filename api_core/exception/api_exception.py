from __future__ import annotations

from typing import Optional

from api_core.mvc.service.data.manual_model import ManualModel


class ApiException(Exception):
    """
    Custom exception for Api errors.
    """

    def __init__(self, message: str, manual: list[ManualModel] | Optional[ManualModel] = None):
        """
        Initialize a new instance of "ApiException" class.
        :param message: The message error.
        :param manual The manual(s) bound(s) to the exception.
        """
        super().__init__(message)
        self.__has_manual: bool = False if manual is None else True
        self.__manuals: list[ManualModel] | Optional[ManualModel] = manual

    @property
    def has_manual(self):
        """
        Check if the exception is bound to a manual.
        :return: True if the exception is bound to a manual; otherwise false.
        """
        return self.__has_manual

    @property
    def manuals(self) -> list[ManualModel] | Optional[ManualModel]:
        return self.__manuals
