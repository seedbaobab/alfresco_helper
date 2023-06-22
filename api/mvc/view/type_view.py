from api_core.mvc.view.view import View


class TypeView(View):
    """
    View for the type controller.
    """

    def __get_name(self) -> str:
        """
        Retrieves the name of the aspect to use to generate a type.
        :return: The name of the aspect to use to generate a type.
        """
        return self.get_input("Please enter the name value of your type")

    def __get_title(self) -> str:
        """
        Retrieves the value of the title to use to generate a type.
        :return: The value of the title to use to generate a type.
        """
        return self.get_input("Please enter the title value of your type")

    def __get_description(self) -> str:
        """
        Retrieves the value of the description to use to generate a description.
        :return: The value of the description to use to generate a description.
        """
        return self.get_input("Please enter the description value of your type")

    def enter_aspect_data(self) -> tuple[str, str, str]:
        """
        Allows the user to enter aspect data.
        :return: A tuple composed of 3 strings in this order: name, title, description.
        """
        return self.__get_name(), self.__get_title(), self.__get_description()
