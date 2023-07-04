from abc import abstractmethod, ABC
from typing import Optional

from api.mvc.model.data.project_model import ProjectModel


class IProjectController(ABC):
    """
    General project controller.
    """

    @abstractmethod
    def get_project(self, artifact_id: Optional[str] = None, verbose: bool = True) -> ProjectModel:
        """
        Retrieves the data model of an Alfresco AIO project.
        :param artifact_id: The artifact id of the Alfresco AIO project.
        :param verbose: Indicates whether notification messages are displayed or not.
        :return: The data model of an Alfresco AIO project.
        """
        pass

    def load(self):
        """
        Loads and generates the necessary project files.
        """
        pass
