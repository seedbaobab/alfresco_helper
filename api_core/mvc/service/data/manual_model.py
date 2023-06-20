from api_core.mvc.service.data.i_manual_model import IManualModel
from api_core.mvc.service.data.manual_argument_model import ManualArgumentModel
from api_core.mvc.service.data.manual_call_model import ManualCallModel


class ManualModel(IManualModel):
    """
    Model class for a manual command.
    """

    def __init__(self, name: str, description: str):
        """
        Initialize a new instance of ManualModel class.
        :param name: The command manual.
        :param description: The command description
        """
        super().__init__()
        self.name: str = name
        self.description: str = description
        self.calls: list[ManualCallModel] = []

    def add_call(self, call: ManualCallModel):
        """
        Add a manual for a command call.
        :param call: The data model for invoking the command.
        """
        self.calls.append(call)
        call.set_manual(self)
        for argument in call.arguments:
            if argument.name not in self._arguments.keys():
                self._arguments[argument.name] = argument

    def to_str(self) -> str:
        """
        Transform the data model to str format.
        :return: The manual madel class to str format.
        """
        result: str = "NAME : {0}\n\n".format(self.name)
        result += "CALLS: \n"
        for call in self.calls:
            result += "{0} ".format(self.name)
            for argument in call.arguments:
                result += "[{0}: {1}] ".format(argument.name, argument.typology)
            result += "\n"
        result += "\nDESCRIPTION\n{0}\n".format(self.description)

        if len(self._arguments.keys()).__gt__(0):
            result += "\nARGUMENTS\n"
            for key in self._arguments.keys():
                argument: ManualArgumentModel = self._arguments[key]
                result += "{0} [{1}] : {2}\n".format(argument.name, argument.typology, argument.description)
        return result
