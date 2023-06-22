from __future__ import annotations

from typing import Optional

from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.data_type import DataType


class TypeModel(DataModel):
    """
    Data model for aspects.
    """

    def __init__(self, name: str, title: Optional[str], description: Optional[str]):
        """
        Initialize a new instance of 'TypeModel' class.
        :param name: The aspect name.
        :param title: The aspect title.
        :param description: The aspect description.
        """
        super().__init__(name, title, description, DataType.ASPECT)

        self.parent = None
        self.mandatory = []
