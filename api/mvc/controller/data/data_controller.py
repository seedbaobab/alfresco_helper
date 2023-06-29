from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Optional

from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.data_type import DataType
from api.mvc.model.data.type_model import TypeModel
from api.mvc.model.service.data.aspect_service import AspectService
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api_core.exception.api_exception import ApiException
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.controller.controller import Controller
from api_core.mvc.service.model.service import Service
from api_core.mvc.view.view import View


class DataController(Controller, ABC):
    """
    Controller class used to manage API project's data.
    """

    def __init__(self, name: str, service: Service, view: View, pc: IProjectController, cmc: IContentModelController):
        """
        Initialize a new instance of DataController class.
        :param name: The name of the controller.
        :param service: The controller's basic service.
        :param view: The controller's view.
        :param pc: A project controller.
        :param cmc: A content model controller.
        """
        super().__init__(name, service, view)
        self._pc: IProjectController = pc
        self._cmc: IContentModelController = cmc
        self._cmfs: ContentModelFileService = ContentModelFileService()

    def _get(self, content_model: ContentModel, data_type: str, name: str) -> Optional[DataModel]:
        """
        Retrieves the data model of an Alfresco AIO type or aspect.
        :param data_type: The type of the data.
        :param content_model: The type's content-model.
        :param name: The type or aspect name.
        :return: The data model of a type or aspect otherwise None.
        """
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)

        # Verification that the type exists.
        if self._cmfs.find_data(content_model, data_type, name) is None:
            return None

        # Verification that the aspect has been declared only once in the file.
        datas_name: list[str] = self._cmfs.get_data_names(content_model, data_type)
        if datas_name.count(name).__gt__(1):
            raise ApiException("{3} '{0}' was declared more than once in content model '{1}' in file '{2}'."
                               .format(name, content_model.complete_name, filename, data_type.title()))

        # Verification that there is no circular inheritance.
        ancestors: list[str] = self.__check_ancestors(content_model, data_type, name,
                                                      "{0}:{1}".format(content_model.prefix, name), [])
        self._check_mandatory_aspects(content_model, name, "{0}:{1}".format(content_model.prefix, name), ancestors, [])

        data: Optional[AspectModel | TypeModel] = None
        if data_type.__eq__(DataType.ASPECT.value):
            data = AspectModel(name, self._cmfs.get_aspect_title(content_model, name),
                               self._cmfs.get_aspect_description(content_model, name))
        else:
            data = TypeModel(name, self._cmfs.get_type_title(content_model, name),
                             self._cmfs.get_type_description(content_model, name))

        # Set the parent data.
        data.parent = self._get(content_model, self._cmfs.get_data_parent(content_model, data_type, name), name)

        # Set the data mandatory aspects.
        if data_type.__eq__(DataType.TYPE.value):
            for mandatory_aspect in self._cmfs.get_type_mandatory_aspects(content_model, name):
                data.add_mandatory_aspect(self._get(content_model, DataType.ASPECT.value, mandatory_aspect))
        else:
            for mandatory_aspect in self._cmfs.get_aspect_mandatory_aspects(content_model, name):
                data.add_mandatory_aspect(self._get(content_model, DataType.ASPECT.value, mandatory_aspect))

        return data

    def _extend(self, content_model: ContentModel, data_type: str, source_name: str, parent_name: str):
        """
        Method allowing a datum (aspect or type) to extend over another datum.
        :param content_model: The data content model.
        :param data_type: The type of data to bind.
        :param source_name: The name of the data to expand.
        :param parent_name: The name of the parent data.
        """
        service: AspectService = self._service
        source: DataModel = self._get(content_model, data_type, source_name)
        parent: DataModel = self._get(content_model, data_type, parent_name)
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)

        if source is None:
            raise ApiException("The '{0}' {3} does not exist in the '{1}' content-model of the '{2} file.'"
                               .format(source_name, content_model.complete_name, filename, data_type))
        elif parent is None:
            raise ApiException("The '{0}' {3} does not exist in the '{1}' content-model of the '{2} file.'"
                               .format(source_name, content_model.complete_name, filename, data_type))

        self.__check_data_link(content_model, data_type, source, parent)
        self.__check_data_link(content_model, data_type, parent, source)

        service.extend(content_model, source, parent)

    def _add_mandatory(self, content_model: ContentModel, data_type: str, source_name: str, mandatory_name: str):
        """
        Method allowing to add a "mandatory-aspect" to data (aspect or type).
        :param content_model: The data content model.
        :param data_type: The type of data to bind.
        :param source_name: The type of data to modify (the one that will include the new mandatory-aspect).
        :param mandatory_name: The name of the required aspect to add.
        """
        # Retrieving the source data model model.
        source: DataModel = self._get(content_model, data_type, source_name)
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        # Obligatory aspect recovery.
        mandatory: DataModel = self._get(content_model, DataType.ASPECT.value, mandatory_name)

        # Verification of the existence of data models.
        if source is None:
            raise ApiException("The '{0}' {3} does not exist in the '{1}' content-model of the '{2} file.'"
                               .format(source_name, content_model.complete_name, filename, data_type))
        elif mandatory is None:
            raise ApiException("The '{0}' {3} does not exist in the '{1}' content-model of the '{2} file.'"
                               .format(source_name, content_model.complete_name, filename, data_type))

        # Check that there is no circular inheritance between the two data models
        self.__check_data_link(content_model, data_type, source, mandatory)
        self.__check_data_link(content_model, data_type, mandatory, source)

        # Addition of the aspect in the list of mandatory aspects.
        self._cmfs.add_mandatory(content_model, source, mandatory)

    def __check_data_link(self, content_model: ContentModel, data_type: str, data_1: DataModel, data_2: DataModel):
        source: str = data_1.name
        complete_name: str = "{0}:{1}".format(content_model.prefix, source)

        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        ancestors: list[str] = self.__check_ancestors(content_model, data_type, source, complete_name, [])

        if data_2.name in ancestors:
            raise ApiException("The '{0}' {1} already has the '{2}' {1} for ancestor in the '{3}' file."
                               .format(data_1.name, data_type, data_2.name, filename))

        mandatory: list[str] = self._check_mandatory_aspects(content_model, source, complete_name, ancestors, [])

        if data_2.name in mandatory:
            raise ApiException("The '{0}' {1} already has the '{2}' {1} in the list of mandatory aspects (by "
                               "inheritance or directly) in the '{3}' file."
                               .format(data_1.name, data_type, data_2.name, filename))

    def __check_ancestors(self, content_model: ContentModel, typology: str, source: str, complete_name: Optional[str],
                          ancestors: list[str]) -> list[str]:
        if complete_name is None:
            # Removing the first element, which is the aspect we're trying to get.
            if len(ancestors).__gt__(0):
                ancestors.pop(0)

            return ancestors

        name: str = complete_name.rsplit(":", 1)[1]
        if self._cmfs.find_data(content_model, typology, name) is None:
            raise ApiException("There is an inheritance problem. {4} '{0}' inherits {5} '{1}' which does not "
                               "exist in content model '{2}' of file '{3}'.\n"
                               .format(ancestors[len(ancestors) - 1], name, content_model.complete_name,
                                       FileFolderHelper.extract_filename_from_path(content_model.path),
                                       typology.title(), typology))

        if ancestors.count(name).__gt__(0):
            raise ApiException("There is an inheritance problem. {3} '{0}' appears twice in the ancestors of aspect"
                               " '{1}'.\n{2}".format(name, source, " -> ".join(ancestors), typology.title()))

        ancestors.append(name)
        return self.__check_ancestors(content_model, typology, source,
                                      self._cmfs.get_aspect_parent(content_model, name), ancestors)

    @abstractmethod
    def _check_mandatory_aspects(self, content_model: ContentModel, source: str, complete_name: Optional[str],
                                 ancestors: list[str], mandatory: list[str]) -> list[str]:
        pass
