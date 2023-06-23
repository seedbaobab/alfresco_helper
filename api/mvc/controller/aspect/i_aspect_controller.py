from abc import abstractmethod, ABC
from typing import Optional

from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel


class IAspectController(ABC):
    """
    General aspect controller.
    """

    @abstractmethod
    def get_aspect(self, content_model: ContentModel, name: str) -> Optional[AspectModel]:
        """
        Retrieves the data model of an Alfresco AIO get_aspect.
        :param content_model: The aspect's content-model.
        :param name: The aspect name.
        :return: The data model of an aspect.
        """
        pass
