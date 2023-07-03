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

    def extend(self, content_model_name: str, aspect_name: str, parent_aspect_name: str):
        """
        Extends a data type to another data type.
        :param content_model_name: The full name of the content model.
        :param aspect_name: The name of the type to extend.
        :param parent_aspect_name:The name of the parent type.
        """
        project: ProjectModel = self._pc.get_project()
        content_model: ContentModel = self._cmc.get_content_model(project, content_model_name)
        self._view.info("Extended aspect '{0}' to aspect '{1}'.".format(aspect_name, parent_aspect_name))
        self._extend(content_model, DataType.ASPECT.value, aspect_name, parent_aspect_name)
        self._view.success("Aspect '{0}' was successfully extended to Aspect '{1}'."
                           .format(aspect_name, parent_aspect_name))

    def mandatory(self, content_model_name: str, aspect_name: str, mandatory_aspect_name: str):
        """
        Add a required aspect to an aspect.
        :param content_model_name: The full name of the content model.
        :param aspect_name: The name of the aspect to host the new mandatory aspect.
        :param mandatory_aspect_name: The name of the new mandatory aspect.
        """
        self._view.info("Add aspect '{0}' to the list of mandatory aspects of aspect '{1}'."
                        .format(mandatory_aspect_name, aspect_name))
        project: ProjectModel = self._pc.get_project()
        content_model: ContentModel = self._cmc.get_content_model(project, content_model_name)
        self._add_mandatory(content_model, DataType.ASPECT.value, aspect_name, mandatory_aspect_name)
        self._view.success("Aspect '{0}' was successfully added to the list of required aspects for aspect '{1}'."
                           .format(mandatory_aspect_name, aspect_name))

    def get_aspect(self, content_model: ContentModel, name: str) -> Optional[AspectModel]:
        """
        Retrieves the data model of an Alfresco AIO get_aspect.
        :param content_model: The aspect's content-model.
        :param name: The aspect name.
        :return: The data model of an aspect.
        """
        # self._view.info("Retrieving the aspect '{0}' data model.".format(name))
        return self._get(content_model, DataType.ASPECT.value, name)

    def load_aspect(self, content_model: ContentModel, name: str) -> AspectModel:
        """
        Load the appearance of a content-model.
        :param content_model: The aspect's content-model.
        :param name: The aspect name.
        :return: The data model of an aspect.
        """
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        self._view.info("Loading aspect '{0}' of content model '{1}' from file '{2}'."
                        .format(name, content_model.complete_name, filename))
        aspect = self.get_aspect(content_model, name)
        self._view.success("Aspect '{0}' of content model '{1}' in file '{2}' was loaded successfully."
                           .format(name, content_model.complete_name, filename))
        return aspect

    def get_aspect_definition_platform_message_file(self, content_model: ContentModel, aspect: AspectModel) -> str:
        """
        Retrieves the look definition for the platform project's "messages" file.
        :param content_model: The aspect content model data model
        :param aspect: The aspect data model.
        :return: The definition of the aspect of the content-model.
        """
        # Cast the service to specialized service.
        service: AspectService = self._service
        # Initialization of the result with the definition of the aspect title.
        result: str = service.get_definition_platform_message_file(content_model, aspect)

        # Added property introductory comment.
        if len(aspect.properties).__gt__(0):
            result += "# Properties of aspect '{0}''.\n".format(aspect.name)

        # Add aspect properties title.
        for property_model in aspect.properties:
            result += self._prc.get_property_definition_platform_message_file(content_model, property_model)

        # If the result is not empty: add a '\n' character.
        if not StringHelper.is_empty(result):
            result += "\n"

        # Return of the result.
        return result

    def _check_mandatory_aspects(self, content_model: ContentModel, source: str, complete_name: Optional[str],
                                 ancestors: list[str], mandatory: list[str]) -> list[str]:
        """
        Check the mandatory aspects of the agent.
        :param content_model: The aspect's content-model.
        :param source: The name of the source aspect.
        :param complete_name: The full name of the aspect.
        :param ancestors: The list of ancestors of the source aspect.
        :param mandatory: The list of current mandatory aspects.
        :return: The list of mandatory aspects.
        """
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

        for mandatory_aspect in self._cmfs.get_aspect_mandatory_aspects(content_model, name):
            self._check_mandatory_aspects(content_model, source, mandatory_aspect, ancestors, mandatory)

        return mandatory

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
