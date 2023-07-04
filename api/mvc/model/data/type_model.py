from __future__ import annotations

from typing import Optional

from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.data_type import DataType
from api.mvc.model.data.i_content_model import IContentModel


class TypeModel(DataModel):
    """
    Data model for aspects.
    """

    def __init__(self, icm: IContentModel, name: str, title: Optional[str], description: Optional[str]):
        """
        Initialize a new instance of 'TypeModel' class.
        :param name: The aspect name.
        :param title: The aspect title.
        :param description: The aspect description.
        """
        super().__init__(icm, name, title, description, DataType.ASPECT)

        self.parent = None
        self.mandatory = []
