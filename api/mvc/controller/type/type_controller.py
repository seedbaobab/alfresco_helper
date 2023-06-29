from abc import ABC
from typing import Optional

from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.controller.data.data_controller import DataController
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.controller.type.i_type_controller import ITypeController
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_type import DataType
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.data.type_model import TypeModel
from api.mvc.model.service.data.type_service import TypeService
from api.mvc.view.type_view import TypeView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper
from api_core.helper.file_folder_helper import FileFolderHelper


class TypeController(DataController, ITypeController, ABC):
    """
    Controller class used to manage API project's type.
    """

    def __init__(self, pc: IProjectController, cmc: IContentModelController):
        """
        Initialize a new instance of TypeController class.
        :param pc: A project controller.
        :param cmc: A content-model controller.
        """
        super().__init__("type", TypeService(), TypeView(ConstantHelper.SCREEN_SIZE), pc, cmc)
        # self.__pc: IProjectController = pc
        # self.__cmc: IContentModelController = cmc
        # self.__cmfs: ContentModelFileService = ContentModelFileService()

    def new(self, content_model_name: str):
        """
        Attempts to create a new type.
        :param content_model_name: The full name of the content model.
        """
        view: TypeView = self._view
        service: TypeService = self._service

        project: ProjectModel = self._pc.get_project()
        content_model: ContentModel = self._cmc.get_content_model(project, content_model_name)

        view.info("Creating a new type")
        (name, title, description) = view.enter_aspect_data()

        if self._cmfs.find_aspect(content_model, name) is not None:
            raise ApiException("There is already an aspect of the name '{0}' in the content model '{1}'."
                               .format(name, content_model.complete_name))

        if self._cmfs.find_aspect(content_model, name) is not None:
            raise ApiException("There is already a type of the name '{0}' in the content model '{1}'."
                               .format(name, content_model.complete_name))

        service.new(content_model, name, title, description)
        view.success("Aspect '{0}' was successfully created in content model '{1}'.".format(name, content_model_name))

    def extend(self, content_model_name: str, type_name: str, parent_type_name: str):
        """
        Extends a data type to another data type.
        :param content_model_name: The full name of the content model.
        :param type_name: The name of the type to extend.
        :param parent_type_name:The name of the parent type.
        """
        project: ProjectModel = self._pc.get_project()
        content_model: ContentModel = self._cmc.get_content_model(project, content_model_name)
        self._view.info("Extended type '{0}' to type '{1}'.".format(type_name, parent_type_name))
        self._extend(content_model, DataType.TYPE.value, type_name, parent_type_name)
        self._view.success("Type '{0}' was successfully extended to type '{1}'."
                           .format(type_name, parent_type_name))

    def mandatory(self, content_model_name: str, type_name: str, mandatory_aspect_name: str):
        self._view.info("Add aspect '{0}' to the list of mandatory aspects of type '{1}'."
                        .format(mandatory_aspect_name, type_name))
        project: ProjectModel = self._pc.get_project()
        content_model: ContentModel = self._cmc.get_content_model(project, content_model_name)
        self._add_mandatory(content_model, DataType.ASPECT.value, type_name, mandatory_aspect_name)
        self._view.success("Aspect '{0}' was successfully added to the list of required aspects for type '{1}'."
                           .format(mandatory_aspect_name, type_name))

    def get_type(self, content_model: ContentModel, name: str) -> Optional[TypeModel]:
        """
        Retrieves the data model of an Alfresco AIO type.
        :param content_model: The type's content-model.
        :param name: The type name.
        :return: The data model of a type.
        """
        self._view.info("Retrieving the type data model.")
        return self._get(content_model, DataType.TYPE.value, name)

    def _check_mandatory_aspects(self, content_model: ContentModel, source: str, complete_name: Optional[str],
                                 ancestors: list[str], mandatory: list[str]) -> list[str]:
        # todo : Check the method
        if complete_name is None:
            mandatory.pop(0)
            return mandatory

        name: str = complete_name.rsplit(":", 1)[1]
        if self._cmfs.find_aspect(content_model, name) is None:
            raise ApiException(
                "Aspect '{0}' has a required aspect '{1}' which does not exist in content model '{2}' "
                "in file '{3}'.".format(mandatory[len(mandatory) - 1], name, content_model.complete_name,
                                        FileFolderHelper.extract_filename_from_path(content_model.path)))

        if ancestors.count(name).__gt__(0):
            raise ApiException(
                "The aspect '{0}' is declared in the ancestors of the aspect '{0}'. It cannot therefore"
                " be one of its mandatory aspects (direct or by inheritance)."
                .format(name, source))

        if mandatory.count(name).__gt__(0):
            raise ApiException("Aspect '{0}' appears twice in the list of mandatory aspects of aspect '{1}' (by "
                               "inheritance or directly).".format(name, source))

        mandatory.append(name)
        if len(ancestors).__gt__(1):
            mandatory_ancestors: list[str] = self.__check_ancestors(content_model, DataType.ASPECT.name, name,
                                                                    complete_name, [])
            for mandatory_ancestor in mandatory_ancestors:
                if ancestors.count(mandatory_ancestor).__gt__(0) or mandatory.count(mandatory_ancestor).__gt__(0):
                    raise ApiException(
                        "Aspect '{0}' appears twice in the list of mandatory aspects of aspect '{1}' "
                        "(by inheritance or directly) by aspect '{2}'."
                        .format(mandatory_ancestor, source, name))
                mandatory.append(mandatory_ancestor)

        if name.__eq__(source):
            for mandatory_aspect in self._cmfs.get_type_mandatory_aspects(content_model, name):
                self._check_mandatory_aspects(content_model, source, mandatory_aspect, ancestors, mandatory)

        else:
            for mandatory_aspect in self._cmfs.get_aspect_mandatory_aspects(content_model, name):
                self._check_mandatory_aspects(content_model, source, mandatory_aspect, ancestors, mandatory)

        return mandatory
