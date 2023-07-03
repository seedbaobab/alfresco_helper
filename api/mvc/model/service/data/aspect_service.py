from abc import ABC

from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api_core.helper.string_helper import StringHelper
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

    def extend(self, content_model: ContentModel, source: DataModel, parent: DataModel):
        self.__cmfs.add_extension(content_model, source, parent)

    def mandatory(self, content_model: ContentModel, source: DataModel, mandatory: DataModel):
        self.__cmfs.add_mandatory(content_model, source, mandatory)

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()
        self.__extend_manual()
        self.__mandatory_manual()

    def __new_manual(self):
        """
        Add the 'new' aspect command in manual.
        """
        self._ms.new_manual("new", "Create a new aspect in a content-model.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.save()

    def __extend_manual(self):
        """
        Add the 'extend' aspect command in manual.
        """
        self._ms.new_manual("extend", "Extend the first aspect to the second in the content-model.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.add_argument("aspect_name", "The name of the aspect whose parent must be modified", "str")
        self._ms.add_argument("parent_aspect_name", "The parent aspect name", "str")
        self._ms.save()

    def __mandatory_manual(self):
        """
        Add the 'mandatory' aspect command in the manual.
        """
        self._ms.new_manual("mandatory", "Adds a mandatory aspect to an aspect.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.add_argument("aspect_name", "The name of the aspect whose parent must be modified", "str")
        self._ms.add_argument("mandatory_aspect_name", "The name of the new mandatory aspect.", "str")
        self._ms.save()

    @staticmethod
    def get_definition_platform_message_file(content_model: ContentModel, aspect: AspectModel) -> str:
        # Result initialization.
        result: str = ""
        # Verification that the aspect has a title to display.
        has_no_title: bool = StringHelper.is_empty(aspect.title)

        # Verification of the need to retrieve the necessary information.
        if has_no_title and len(aspect.properties).__eq__(0):
            return result

        # Comment to introduce the aspect.
        result += "# Labels for aspect '{0}'.\n".format(aspect.name)
        # Definition of the aspect title.
        if not has_no_title:
            result += "{0}_{1}.{2}.{0}_{3}.title={4}\n\n".format(content_model.prefix, content_model.name,
                                                                 aspect.typology, aspect.name, aspect.title)

        return result
