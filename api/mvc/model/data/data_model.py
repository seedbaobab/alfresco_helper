from typing import Optional

from api.mvc.model.data.data_type import DataType
from api.mvc.model.data.i_content_model import IContentModel
from api.mvc.model.data.i_data_model import IDataModel
from api.mvc.model.data.property_model import PropertyModel
from api_core.helper.string_helper import StringHelper


class DataModel(IDataModel):
    """
    Model class for content-model's data models.
    """

    def __init__(self, icm: IContentModel, name: str, title: Optional[str], description: Optional[str],
                 typology: DataType):
        """
        Initialize a new instance of DataModel class.
        :param name: The name of the content-model's data.
        :param title: The title of the content-model's data.
        :param description: The description of the content-model's data.
        :param typology: The typology of the content-model's data.
        """
        super().__init__(icm)
        self.__name: str = name
        self.__title: Optional[str] = title
        self.__typology: DataType = typology
        self._mandatory: list[DataModel] = []
        self.__parent: Optional[DataModel] = None
        self.__description: Optional[str] = description
        self.__properties: list[PropertyModel] = []

    @property
    def name(self) -> str:
        """
        Get the data name.
        :return: The data name.
        """
        return self.__name

    @property
    def title(self) -> str:
        """
        Get the data title.
        :return: The data title.
        """
        return self.__title

    @property
    def description(self) -> str:
        """
        Get the data description.
        :return: The data description.
        """
        return self.__description

    @property
    def properties(self) -> list[PropertyModel]:
        """
        Get the list of properties linked to the model.
        :return: The list of properties linked to the model.
        """
        return self.__properties

    @property
    def typology(self) -> str:
        return self.__typology.value

    @property
    def complete_name(self):
        return "{0}:{1}".format(self.prefix, self.__name)

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, value):
        self.__parent = value

    @property
    def mandatory(self):
        return self._mandatory

    @property
    def share_set_id(self):
        return StringHelper.to_camel_case("{0}_{1}".format(self.prefix, self.__name))

    @property
    def share_label_id(self):
        return "form.set.label.{0}.{1}".format(self.prefix, self.name)

    def add_property(self, property_model: PropertyModel):
        """
        Add a property to the data model.
        :param property_model: The property to add to the property.
        """
        self.__properties.append(property_model)

    def to_str(self) -> str:
        return "NAME: {0}\nTITLE: {1}\nTYPE: {2}".format(self.name, self.title, self.typology)
