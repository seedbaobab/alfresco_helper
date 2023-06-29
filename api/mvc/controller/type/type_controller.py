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
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api.mvc.view.type_view import TypeView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper


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

    def get_type(self, content_model: ContentModel, name: str) -> Optional[TypeModel]:
        """
        Retrieves the data model of an Alfresco AIO type.
        :param content_model: The type's content-model.
        :param name: The type name.
        :return: The data model of a type.
        """
        self._view.info("Retrieving the type data model.")
        return self._get(content_model, DataType.TYPE.value, name)
        # filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        #
        # # Verification that the type exists.
        # if self.__cmfs.find_type(content_model, name) is None:
        #     return None
        #
        # # Verification that the aspect has been declared only once in the file.
        # types_name: list[str] = self.__cmfs.get_aspects_name(content_model)
        # if types_name.count(name).__gt__(1):
        #     raise ApiException("Type '{0}' was declared more than once in content model '{1}' in file '{2}'."
        #                        .format(name, content_model.complete_name, filename))
        #
        # # Verification that there is no circular inheritance.
        # ancestors: list[str] = self.__check_ancestors(content_model, name, "{0}:{1}".format(content_model.prefix, name))
        # self.__check_mandatory_aspects(content_model, name, "{0}:{1}".format(content_model.prefix, name), ancestors)
        #
        # aspect: TypeModel = TypeModel(name, self.__cmfs.get_type_title(content_model, name),
        #                               self.__cmfs.get_type_description(content_model, name))
        # aspect.parent(self.__get_type(content_model, self.__cmfs.get_aspect_parent(content_model, name)))
        #
        # for mandatory_aspect in self.__cmfs.get_type_mandatory_aspects(content_model, name):
        #     aspect.add_mandatory_aspect(self.__get_aspect(content_model, mandatory_aspect))
        #
        # return aspect

    def _check_mandatory_aspects(self, content_model: ContentModel, source: str, complete_name: Optional[str],
                                 ancestors: list[str], mandatory: list[str] = [])  -> list[str]:
        pass

