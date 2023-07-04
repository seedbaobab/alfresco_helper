from abc import abstractmethod, ABC

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel


class IContentModelController(ABC):
    """
    General content-model controller.
    """

    @abstractmethod
    def get_content_model(self, project: ProjectModel, content_model: str, verbose: bool = True) -> ContentModel:
        """
        Retrieves the data model of an Alfresco AIO project.
        :param project: The content-model's project.
        :param content_model: The content-model complete name of the Alfresco AIO project.
        :param verbose: Indicates whether notification messages are displayed or not.
        :return: The data model of an Alfresco AIO project.
        """
        pass

    @abstractmethod
    def load_content_model(self, project: ProjectModel, content_model_file_path: str) -> ContentModel:
        """
        Loads a content model by its file.
        :param project: The content-model's project.
        :param content_model_file_path: The absolute path to the content model file.
        :return: The data model of an Alfresco AIO project.
        """
        pass

    @abstractmethod
    def generate_share_message_file(self, project: ProjectModel, content_model: ContentModel):
        pass

    @abstractmethod
    def add_content_model_in_bootstrap(self, project: ProjectModel, content_model: ContentModel):
        """
        Adds the content model to the bootstrap file.
        :param project: The content-model's project.
        :param content_model: The content-model complete name of the Alfresco AIO project.
        """
        pass

    @abstractmethod
    def generate_platform_message_file(self, content_model: ContentModel):
        pass

    @abstractmethod
    def add_share_file_message_labels(self, project: ProjectModel, content_model: ContentModel):
        pass
