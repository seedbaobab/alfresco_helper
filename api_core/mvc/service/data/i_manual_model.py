from api_core.mvc.service.data.manual_argument_model import ManualArgumentModel


class IManualModel:
    """
    Model class for a manual command for a ManualCallModel instance.
    """

    def __init__(self):
        """
        Initialize a new instance of IManualModel class.
        """
        self._arguments: dict[str, ManualArgumentModel] = {}

    def add_argument(self, argument: ManualArgumentModel):
        """
        Add an argument to the manual.
        :param argument The argument to add to the model.
        """
        if argument.name not in self._arguments.keys():
            self._arguments[argument.name] = argument
