from __future__ import annotations

import re
from abc import ABC
from typing import Optional

from api.mvc.controller.aspect.i_aspect_controller import IAspectController
from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.controller.property.i_property_controller import IPropertyController
from api.mvc.controller.type.i_type_controller import ITypeController
from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.data.property_model import PropertyModel
from api.mvc.model.data.type_model import TypeModel
from api.mvc.model.service.data.property_service import PropertyService
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api.mvc.view.property_view import PropertyView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.helper.string_helper import StringHelper
from api_core.mvc.controller.controller import Controller
from api_core.mvc.view.view import View


class PropertyController(Controller, IPropertyController, ABC):

    def __init__(self, pc: IProjectController, cmc: IContentModelController, ac: IAspectController,
                 tc: ITypeController):
        super().__init__("property", PropertyService(), PropertyView(ConstantHelper.SCREEN_SIZE))
        self.__cmfs: ContentModelFileService = ContentModelFileService()
        self.__cmc: IContentModelController = cmc
        self.__pc: IProjectController = pc
        self.__ac: IAspectController = ac
        self.__tc: ITypeController = tc

    def new(self, content_model_name: str, data_name: str):
        service: PropertyService = self._service
        view: PropertyView = self._view

        self._view.info("Creating a new property")
        project: ProjectModel = self.__pc.get_project()
        content_model: ContentModel = self.__cmc.get_content_model(project, content_model_name)
        data: Optional[DataModel] = self.__ac.get_aspect(content_model, data_name)
        data = self.__tc.get_type(content_model, data_name) if data is None else data

        if data is None:
            raise ApiException("There is no aspect or type named '{0}' in content-model '{1}' in file '{2}"
                               .format(data_name, content_model.complete_name,
                                       FileFolderHelper.extract_filename_from_path(content_model.path)))
        (name, title, description, typology, mandatory) = view.enter_property_data()

        self.__check_name(name)
        self.__check_property_type(typology)

        if self.__cmfs.get_properties(content_model).count(name).__gt__(0):
            raise ApiException("There is already a property named '{0}' in content model '{1}' in file '{2}'."
                               .format(name, content_model.complete_name,
                                       FileFolderHelper.extract_filename_from_path(content_model.path)))

        service.new(content_model, data, name, title, description, typology, mandatory)
        self._view.success("Property '{0}' was successfully created.".format(data_name))

    def load_property(self, content_model: ContentModel, data: DataModel, property_name: str) -> PropertyModel:
        """
        Loads a property from a data model.
        :param content_model: The data's content-model.
        :param data: The owner data of the property.
        :param property_name: The property name.
        :return: A data model for the property.
        """
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        self._view.info("Loading the property {0} from {1} {2} of content-model {3} ({4} file)"
                        .format(property_name, data.typology, data.name, content_model.complete_name, filename))
        (name, title, description, typology, mandatory) = self.__cmfs.get_property(content_model, data, property_name)
        prop: PropertyModel = PropertyModel(name, title, description, mandatory, typology)
        self._view.success("The property {0} from {1} {2} of content-model {3} ({4} file) was successfully loaded."
                           .format(property_name, data.typology, data.name, content_model.complete_name, filename))
        return prop

    def get_property_definition_platform_message_file(self, content_model: ContentModel,
                                                      property_model: PropertyModel) -> str:
        result: str = ""
        if not StringHelper.is_empty(property_model.title):
            result += "{0}_{1}.property.{0}_{2}.title={3}\n"\
                .format(content_model.prefix, StringHelper.to_camel_case(content_model.name), property_model.name,
                        property_model.title)
        return result

    @staticmethod
    def __check_name(value: str):
        """
        Verifies that the name put in parameter is valid; otherwise it throws an ApiException.
        :param value: The name to test.
        """
        # Verification that it is not empty or null.
        if StringHelper.is_empty(value):
            raise ApiException("The property name cannot be null or empty.")

        # Check that there are no spaces.
        elif StringHelper.has_space(value):
            raise ApiException("The property name cannot contain spaces.")

        # Check that there are no special characters.
        elif re.match("[a-zA-Z0-9]+$", value) is None:
            raise ApiException("The property name cannot contain any special"
                               " (example of a valid property name: 'securityClassification').")

    @staticmethod
    def __check_property_type(typology: str) -> str:
        if StringHelper.is_empty(typology):
            raise ApiException("The type of the property is invalid. It cannot be empty or None.")
        elif StringHelper.has_space(typology):
            raise ApiException("The type of the property is invalid. There can be no space in it.")
        elif (typology.__ne__("text") and typology.__ne__("int") and typology.__ne__("long")
              and typology.__ne__("float") and typology.__ne__("double") and typology.__ne__("date")
              and typology.__ne__("datetime") and typology.__ne__("boolean") and typology.__ne__("encrypted")
              and typology.__ne__("noderef")):
            raise ApiException("The type of the property is invalid. Its value must be: text, int, long, float, double,"
                               " date, datetime, boolean, encrypted or noderef.")
        return typology
