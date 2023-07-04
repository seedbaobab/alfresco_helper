from __future__ import annotations

from abc import ABC
from typing import Optional


from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.data.property_model import PropertyModel

from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api.mvc.model.service.file.share_config_service import ShareConfigFileService
from api_core.mvc.service.model.service import Service


class PropertyService(Service, ABC):

    def __init__(self):
        super().__init__("property")
        self.__cmfs: ContentModelFileService = ContentModelFileService()
        self.__scfs: ShareConfigFileService = ShareConfigFileService()

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()

    def new(self, content_model: ContentModel, data: DataModel, name: str, title: Optional[str],
            description: Optional[str], typology: str, mandatory: bool):
        self.__cmfs.add_property(content_model, data, name, title, description, typology, mandatory)

    def add_property_in_share_config_file(self, project: ProjectModel, data: DataModel, property_model: PropertyModel):
        self.__scfs.add_property(project, data, property_model)
        pass

    def __new_manual(self):
        """
        Add the new property model command in manual.
        """
        self._ms.new_manual("new", "Create a property into an aspect or a type.")
        self._ms.add_call()
        self._ms.add_argument("cm_prefix:cm_name", "The complete content-model name", "str")
        self._ms.add_argument("data_name", "The name of the data (aspect or type) to add the property to", "str")

        self._ms.save()
