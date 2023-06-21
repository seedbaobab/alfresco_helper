from api_core.mvc.controller.controller import Controller


class ControllerService:
    """
    Service class to manage API controllers.
    """

    def __init__(self):
        """
        Initialize a new instance of 'ControllerService' class.
        """
        self.__controllers: dict[str, Controller] = {}

    def exists(self, name: str) -> bool:
        """
        Indicate whether the controller exists in the data service.
        :param name: The name of the controller.
        :return:
        """
        return name in self.__controllers.keys()

    def add(self, controller: Controller):
        """
        Add a controller in the service.
        :param controller: The controller to add.
        """
        self.__controllers[controller.name] = controller

    def get(self, name: str) -> Controller:
        """
        Get a controller by name.
        :param name: The name of the controller.
        :return: The controller referenced by name.
        """
        return self.__controllers.get(name)
