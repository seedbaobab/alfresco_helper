from api_core.mvc.view.view import View


class AspectView(View):
    """
    View for the aspect controller.
    """

    def __get_name(self) -> str:
        """
        Retrieves the name of the aspect to use to generate an aspect.
        :return: The name of the aspect to use to generate an aspect.
        """
        return self.get_input("Please enter the name value of your aspect")

    def __get_title(self) -> str:
        """
        Retrieves the value of the title to use to generate an aspect.
        :return: The value of the title to use to generate an aspect.
        """
        return self.get_input("Please enter the title value of your aspect")

    def __get_description(self) -> str:
        """
        Retrieves the value of the description to use to generate a description.
        :return: The value of the description to use to generate a description.
        """
        return self.get_input("Please enter the description value of your aspect")

    def enter_aspect_data(self) -> tuple[str, str, str]:
        """
        Allows the user to enter aspect data.
        :param content_model: The content-model data model.
        :param service: The aspect management service.
        :return: A tuple composed of 3 strings in this order: name, title, description.
        """
        return self.__get_name(), self.__get_title(), self.__get_description()
