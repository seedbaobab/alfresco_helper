from abc import ABC

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api_core.mvc.service.model.service import Service


class TypeService(Service, ABC):
    """
    Class providing services for managing project's type.
    """

    def __init__(self):
        """
        Initialize a new instance of 'TypeService' class.
        """
        super().__init__("type")
        self.__cmfs: ContentModelFileService = ContentModelFileService()

    def new(self, content_model: ContentModel, name: str, title: str, description: str):
        self.__cmfs.add_type(content_model, name, title, description)

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()

    def __new_manual(self):
        """
        Add the 'new' aspect command in manual.
        """
        self._ms.new_manual("new", "Create a type in a content-model.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.save()
