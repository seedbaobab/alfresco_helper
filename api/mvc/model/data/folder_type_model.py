from typing import Optional

from api.mvc.model.data.i_content_model import IContentModel
from api.mvc.model.data.property_model import PropertyModel
from api.mvc.model.data.type_model import TypeModel


class FolderTypeModel(TypeModel):
    def __init__(self, icm: IContentModel):
        super().__init__(icm, "folder", None, None)

    @property
    def complete_name(self):
        return "cm:{0}".format(self.name)

    @property
    def typology(self) -> str:
        return self.name

    @property
    def parent(self) -> str:
        return None

    @parent.setter
    def parent(self, value):
        pass

    @property
    def share_set_id(self) -> str:
        return ""

    @property
    def share_label_id(self):
        return ""

    def add_property(self, property_model: PropertyModel):
        """
        Add a property to the data model.
        :param property_model: The property to add to the property.
        """
        pass
