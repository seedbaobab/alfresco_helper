from api.mvc.controller.content_model.i_content_model_controller import IContentModelController
from api.mvc.controller.project.i_project_controller import IProjectController
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.service.data.type_service import TypeService
from api.mvc.model.service.file.content_model_service import ContentModelFileService
from api.mvc.view.aspect_view import AspectView
from api_core.exception.api_exception import ApiException
from api_core.helper.constant_helper import ConstantHelper
from api_core.mvc.controller.controller import Controller


class TypeController(Controller):
    """
    Controller class used to manage API project's type.
    """

    def __init__(self, pc: IProjectController, cmc: IContentModelController):
        """
        Initialize a new instance of AspectController class.
        :param pc: A project controller.
        :param cmc: A content-model controller.
        """
        super().__init__("type", TypeService(), AspectView(ConstantHelper.SCREEN_SIZE))
        self.__pc: IProjectController = pc
        self.__cmc: IContentModelController = cmc
        self.__cmfs: ContentModelFileService = ContentModelFileService()

    def new(self, content_model_name: str):
        """
        Attempts to create a new content model in the project.
        :param content_model_name: The full name of the content model.
        """
        view: AspectView = self._view
        service: TypeService = self._service

        project: ProjectModel = self.__pc.get_project()
        content_model: ContentModel = self.__cmc.get_content_model(project, content_model_name)

        view.info("Creating a new type")
        (name, title, description) = view.enter_aspect_data()

        if self.__cmfs.find_aspect(content_model, name) is not None:
            raise ApiException("There is already an aspect of the name '{0}' in the content model '{1}'."
                               .format(name, content_model.complete_name))

        if self.__cmfs.find_aspect(content_model, name) is not None:
            raise ApiException("There is already a type of the name '{0}' in the content model '{1}'."
                               .format(name, content_model.complete_name))

        service.new(content_model, name, title, description)
        view.success("Aspect '{0}' was successfully created in content model '{1}'.".format(name, content_model_name))
