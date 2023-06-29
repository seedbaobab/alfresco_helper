from abc import ABC

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
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

    def extend(self, content_model: ContentModel, source: DataModel, parent: DataModel):
        self.__cmfs.add_extension(content_model, source, parent)

    def mandatory(self, content_model: ContentModel, source: DataModel, mandatory: DataModel):
        self.__cmfs.add_mandatory(content_model, source, mandatory)

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

    def __extend_manual(self):
        """
        Add the 'extend' type command in manual.
        """
        self._ms.new_manual("extend", "Extend the first type to the second in the content-model.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.add_argument("aspect_name", "The name of the aspect whose parent must be modified", "str")
        self._ms.add_argument("parent_aspect_name", "The parent aspect name", "str")
        self._ms.save()

    def __mandatory_manual(self):
        """
        Add the 'mandatory' type command in manual.
        """
        self._ms.new_manual("mandatory", "Adds a mandatory aspect to a type.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.add_argument("type_name", "The name of the type whose parent must be modified", "str")
        self._ms.add_argument("mandatory_aspect_name", "The name of the new mandatory aspect.", "str")
        self._ms.save()