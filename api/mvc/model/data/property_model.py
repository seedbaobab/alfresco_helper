from api.mvc.model.data.i_data_model import IDataModel
from api_core.helper.string_helper import StringHelper


class PropertyModel:
    """
    Data model for Property.
    """

    def __init__(self, data: IDataModel, name: str, title: str, description: str, mandatory: bool, typology: str):
        """
        Initialize a new instance of PropertyModel class.
        :param name: The name of the property.
        :param title: The title of the property.
        :param description: The description of the property.
        :param mandatory: Indicate if the property is mandatory.
        :param typology: The typology of the property.
        """
        self.__name: str = name
        self.__title: str = title
        self.__typology: str = typology
        self.__mandatory: bool = mandatory
        self.__data_model: IDataModel = data
        self.__description: str = description

    @property
    def label_id(self) -> str:
        return "form.field.label.{0}.{1}".format(self.__data_model.prefix, StringHelper.to_camel_case(self.__name))

    @property
    def name(self) -> str:
        return self.__name

    @property
    def title(self) -> str:
        return self.__title

    @property
    def typology(self) -> str:
        return self.__typology

    @property
    def complete_name(self) -> str:
        return "{0}:{1}".format(self.__data_model.prefix, self.__name)
