from abc import ABC

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api_core.mvc.service.model.service import Service


class AspectService(Service, ABC):
    """
    Class providing services for managing project's aspect.
    """

    def __init__(self):
        """
        Initialize a new instance of 'AspectService' class.
        """
        super().__init__("aspect")
        self.__cmfs: ContentModelFileService = ContentModelFileService()

    def new(self, content_model: ContentModel, name: str, title: str, description: str):
        self.__cmfs.add_aspect(content_model, name, title, description)
