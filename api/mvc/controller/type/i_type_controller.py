from abc import abstractmethod, ABC
from typing import Optional

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.type_model import TypeModel


class ITypeController(ABC):
    """
    General type controller.
    """

    @abstractmethod
    def get_type(self, content_model: ContentModel, name: str) -> Optional[TypeModel]:
        """
        Retrieves the data model of an Alfresco AIO type.
        :param content_model: The aspect's content-model.
        :param name: The type name.
        :return: The data model of a type.
        """
        pass
