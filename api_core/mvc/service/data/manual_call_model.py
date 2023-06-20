from __future__ import annotations

from typing import Optional

from api_core.mvc.service.data.i_manual_model import IManualModel
from api_core.mvc.service.data.manual_argument_model import ManualArgumentModel


class ManualCallModel:
    """
    Model class for a command call.
    """

    def __init__(self):
        """
        Initialize a new instance of 'ManualCallModel' class.
        """
        self.arguments: list[ManualArgumentModel] = []
        self.manual: Optional[IManualModel] = None

    def add_argument(self, argument: ManualArgumentModel):
        """
        Add an argument to the call.
        :param argument: The argument to add to the call.
        """
        self.arguments.append(argument)
        if self.manual is not None:
            self.manual.add_argument(argument)

    def set_manual(self, manual_model: IManualModel):
        """
        Set the call manual.
        :param manual_model: The call manual.
        """
        self.manual = manual_model
