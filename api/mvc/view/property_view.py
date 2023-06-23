from api_core.mvc.view.view import View


class PropertyView(View):
    """
    View for the aspect controller.
    """

    def __get_name(self) -> str:
        """
        Retrieves the name of the aspect to use to generate an aspect.
        :return: The name of the aspect to use to generate an aspect.
        """
        return self.get_input("Please enter the name value of your property")

    def __get_title(self) -> str:
        """
        Retrieves the value of the title to use to generate an aspect.
        :return: The value of the title to use to generate an aspect.
        """
        return self.get_input("Please enter the title value of your property")

    def __get_description(self) -> str:
        """
        Retrieves the value of the description to use to generate a description.
        :return: The value of the description to use to generate a description.
        """
        return self.get_input("Please enter the description value of your property")

    def __get_type(self) -> str:
        return self.get_input("Please enter the type value of your property")

    def __get_mandatory(self) -> bool:
        return self.get_bool_input("Please indicate if the property is mandatory ('y' or 'n')")

    def enter_property_data(self) \
            -> tuple[str, str, str, str, bool]:
        """
        Allows the user to enter property into data.
        :return: A tuple composed of 3 strings in this order: name, title, description.
        """
        return self.__get_name(), self.__get_title(), self.__get_description(), \
            self.__get_type(), self.__get_mandatory()
