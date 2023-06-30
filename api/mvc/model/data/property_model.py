class PropertyModel:
    """
    Data model for Property.
    """

    def __init__(self, name: str, title: str, description: str, mandatory: bool, typology: str):
        """
        Initialize a new instance of PropertyModel class.
        :param name: The name of the property.
        :param title: The title of the property.
        :param description: The description of the property.
        :param mandatory: Indicate if the property is mandatory.
        :param typology: The typology of the property.
        """
        self.__name: str = name
        self.__title: str = title
        self.__typology: str = typology
        self.__mandatory: bool = mandatory
        self.__description: str = description

    @property
    def name(self) -> str:
        return self.__name
