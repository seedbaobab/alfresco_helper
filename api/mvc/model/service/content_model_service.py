from abc import ABC

from api_core.mvc.service.model.service import Service


class ContentModel(Service, ABC):
    """
    Class providing services for managing project's content-model.
    """

    def __init__(self):
        super().__init__("model")

    def new(self):
        pass

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()

    def __new_manual(self):
        """
        Add the new content-model command in manual.
        """
        self._ms.new_manual("new", "Create a new content model.")
        self._ms.add_call()
        self._ms.save()
