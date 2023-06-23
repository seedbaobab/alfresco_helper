import re
from abc import ABC
from typing import Optional

from api.mvc.controller.aspect.i_aspect_controller import IAspectController
from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.controller.data.data_controller import DataController
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_type import DataType
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.service.data.aspect_service import AspectService
from api.mvc.view.aspect_view import AspectView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.helper.string_helper import StringHelper


# from api_core.helper.string_helper import StringHelper


class AspectController(DataController, IAspectController, ABC):
    """
    Controller class used to manage API project's aspect.
    """

    def __init__(self, pc: IProjectController, cmc: IContentModelController):
        """
        Initialize a new instance of AspectController class.
        :param pc: A project controller.
        :param cmc: A content-model controller.
        """
        super().__init__("aspect", AspectService(), AspectView(ConstantHelper.SCREEN_SIZE), pc, cmc)
        # self.__pc: IProjectController = pc
        # self.__cmc: IContentModelController = cmc
        # self.__cmfs: ContentModelFileService = ContentModelFileService()

    def new(self, content_model_name: str):
        """
        Attempts to create a new aspect.
        :param content_model_name: The full name of the content model.
        """
        view: AspectView = self._view
        service: AspectService = self._service

        project: ProjectModel = self._pc.get_project()
        content_model: ContentModel = self._cmc.get_content_model(project, content_model_name)

        view.info("Creating a new aspect")
        (name, title, description) = view.enter_aspect_data()

        self.__check_name(name)

        if self._cmfs.find_aspect(content_model, name) is not None:
            raise ApiException("There is already an aspect of the name '{0}' in the content model '{1}'."
                               .format(name, content_model.complete_name))

        if self._cmfs.find_aspect(content_model, name) is not None:
            raise ApiException("There is already a type of the name '{0}' in the content model '{1}'."
                               .format(name, content_model.complete_name))

        service.new(content_model, name, title, description)
        view.success("Aspect '{0}' was successfully created in content model '{1}'.".format(name, content_model_name))

    # def __get_aspect(self, content_model: ContentModel, name: Optional[str]) -> Optional[AspectModel]:
    #     if StringHelper.is_empty(name):
    #         return None
    #     filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
    #
    #     # Verification that the aspect exists.
    #     if self._cmfs.find_aspect(content_model, name) is None:
    #         raise ApiException("There is no aspect named '{0}' in content model '{1}' in file '{2}'."
    #                            .format(name, content_model.complete_name, filename))
    #
    #     # Verification that the aspect has been declared only once in the file.
    #     aspects_name: list[str] = self._cmfs.get_aspects_name(content_model)
    #     if aspects_name.count(name).__gt__(1):
    #         raise ApiException("Aspect '{0}' was declared more than once in content model '{1}' in file '{2}'."
    #                            .format(name, content_model.complete_name, filename))
    #
    #     # Verification that there is no circular inheritance.
    #     ancestors: list[str] = self.__check_ancestors(content_model, DataType.ASPECT.name, name,
    #                                                   "{0}:{1}".format(content_model.prefix, name))
    #     self._check_mandatory_aspects(content_model, name, "{0}:{1}".format(content_model.prefix, name), ancestors)
    #
    #     aspect: AspectModel = AspectModel(name,
    #                                       self._cmfs.get_aspect_title(content_model, name),
    #                                       self._cmfs.get_aspect_description(content_model, name))
    #     aspect.parent(self.__get_aspect(content_model, self._cmfs.get_aspect_parent(content_model, name)))
    #     for mandatory_aspect in self._cmfs.get_aspect_mandatory_aspects(content_model, name):
    #         aspect.add_mandatory_aspect(self.__get_aspect(content_model, mandatory_aspect))
    #
    #     return aspect

    def get_aspect(self, content_model: ContentModel, name: str) -> Optional[AspectModel]:
        """
        Retrieves the data model of an Alfresco AIO get_aspect.
        :param content_model: The aspect's content-model.
        :param name: The aspect name.
        :return: The data model of an aspect.
        """
        self._view.info("Retrieving the aspect data model.")
        return self._get(content_model, DataType.ASPECT.value, name)
        # filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        #
        # # Verification that the aspect exists.
        # if self._cmfs.find_aspect(content_model, name) is None:
        #     return None
        #     # raise ApiException("There is no aspect named '{0}' in content model '{1}' in file '{2}'."
        #     #                    .format(name, content_model.complete_name, filename))
        #
        # # Verification that the aspect has been declared only once in the file.
        # aspects_name: list[str] = self._cmfs.get_aspects_name(content_model)
        # if aspects_name.count(name).__gt__(1):
        #     raise ApiException("Aspect '{0}' was declared more than once in content model '{1}' in file '{2}'."
        #                        .format(name, content_model.complete_name, filename))
        #
        # # Verification that there is no circular inheritance.
        # ancestors: list[str] = self.__check_ancestors(content_model, DataType.ASPECT.name, name,
        #                                               "{0}:{1}".format(content_model.prefix, name))
        # self._check_mandatory_aspects(content_model, name, "{0}:{1}".format(content_model.prefix, name), ancestors)
        #
        # aspect: AspectModel = AspectModel(name,
        #                                   self._cmfs.get_aspect_title(content_model, name),
        #                                   self._cmfs.get_aspect_description(content_model, name))
        # aspect.parent(self.__get_aspect(content_model, self._cmfs.get_aspect_parent(content_model, name)))
        # for mandatory_aspect in self._cmfs.get_aspect_mandatory_aspects(content_model, name):
        #     aspect.add_mandatory_aspect(self.__get_aspect(content_model, mandatory_aspect))
        #
        # return aspect

    def _check_mandatory_aspects(self, content_model: ContentModel, source: str, complete_name: Optional[str],
                                 ancestors: list[str], mandatory: list[str] = []):
        if complete_name is None:
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

        mandatory.append(name)
        if mandatory.count(name).__gt__(1):
            raise ApiException("Aspect '{0}' appears twice in the list of mandatory aspects of aspect '{1}' (by "
                               "inheritance or directly).".format(name, source))

        if len(ancestors).__gt__(1):
            mandatory_ancestors: list[str] = self.__check_ancestors(content_model, DataType.ASPECT.name, name,
                                                                    complete_name)
            for mandatory_ancestor in mandatory_ancestors:
                if ancestors.count(mandatory_ancestor).__gt__(0) or mandatory.count(mandatory_ancestor).__gt__(0):
                    raise ApiException(
                        "Aspect '{0}' appears twice in the list of mandatory aspects of aspect '{1}' "
                        "(by inheritance or directly) by aspect '{2}'."
                        .format(mandatory_ancestor, source, name))
                mandatory.append(mandatory_ancestor)

        for mandatory_aspect in self._cmfs.get_aspect_mandatory_aspects(content_model, name):
            self._check_mandatory_aspects(content_model, source, mandatory_aspect, ancestors, mandatory)

    @staticmethod
    def __check_name(value: str):
        """
        Verifies that the name put in parameter is valid; otherwise it throws an ApiException.
        :param value: The name to test.
        """
        # Verification that it is not empty or null.
        if StringHelper.is_empty(value):
            raise ApiException("The aspect name cannot be null or empty.")

        # Check that there are no spaces.
        elif StringHelper.has_space(value):
            raise ApiException("The aspect name cannot contain spaces.")

        # Check that there are no special characters.
        elif re.match("[a-zA-Z0-9]+$", value) is None:
            raise ApiException("The aspect name cannot contain any special"
                               " (example of a valid aspect name: 'securityClassified').")
