from abc import ABC, abstractmethod

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.property_model import PropertyModel


class IPropertyController(ABC):
    """
    Contractual interface for property controllers.
    """

    @abstractmethod
    def load_property(self, content_model: ContentModel, data: DataModel, property_name: str) -> PropertyModel:
        """
        Loads a property from a data model.
        :param content_model: The data's content-model.
        :param data: The owner data of the property.
        :param property_name: The property name.
        :return: A data model for the property.
        """
        pass
