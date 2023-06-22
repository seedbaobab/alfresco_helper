from abc import abstractmethod, ABC
from typing import Optional

from api.mvc.model.data.project_model import ProjectModel


class IContentModelController(ABC):
    """
    General content-model controller.
    """

    @abstractmethod
    def get_content_model(self, project: ProjectModel, content_model: str) -> ContentModel:
        """
        Retrieves the data model of an Alfresco AIO project.
        :param project: The content-model's project.
        :param content_model: The content-model complete name of the Alfresco AIO project.
        :return: The data model of an Alfresco AIO project.
        """
        pass
