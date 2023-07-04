from abc import abstractmethod, ABC
from typing import Optional

from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel


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

    @abstractmethod
    def load_aspect(self, content_model: ContentModel, name: str) -> AspectModel:
        """
        Load the appearance of a content-model.
        :param content_model: The aspect's content-model.
        :param name: The aspect name.
        :return: The data model of an aspect.
        """
        pass

    @abstractmethod
    def add_aspect_in_share_config_file(self, project: ProjectModel, content_model: ContentModel,
                                        aspect: AspectModel):
        pass

    @abstractmethod
    def add_aspect_properties_in_share_config_file(self, project: ProjectModel, aspect: AspectModel):
        pass

    def get_aspect_definition_platform_message_file(self, content_model: ContentModel, aspect: AspectModel):
        pass

    def get_aspect_definition_share_message_file(self, content_model: ContentModel, aspect: AspectModel) -> str:
        pass
