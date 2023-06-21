from api_core.mvc.controller.controller import Controller


class ContentModelController(Controller):
    """
    Controller class used to manage API project's content-model.
    """

    def __init__(self):
        """
        Initialize a new instance of ProjectController class.
        """
        super().__init__("project", ProjectService(), ProjectView(ConstantHelper.SCREEN_SIZE))

