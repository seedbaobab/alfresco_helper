class ManualArgumentModel:
    """
    Model class for a manual argument.
    """

    def __init__(self, name: str, description: str, typology: str):
        """
        Initialize a new instance of class "ManualArgumentModel".
        :param name: The name of the argument.
        :param typology: The typology of the argument.
        :param description: The argument description.
        """
        self.__name: str = name
        self.__typology = typology
        self.__description: str = description

    @property
    def name(self) -> str:
        """
        Get the argument name.
        :return: The argument name.
        """
        return self.__name

    @property
    def typology(self) -> str:
        """
        Get the argument name.
        :return: The argument name.
        """
        return self.__typology

    @property
    def description(self) -> str:
        """
        Get the argument description.
        :return: The argument description.
        """
        return self.__description
