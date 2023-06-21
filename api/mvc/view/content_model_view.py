from api_core.mvc.view.view import View


class ContentModelView(View):
    """
    View for the content_model controller.
    """

    def enter_content_model_data(self) -> tuple[str, str]:
        """
        Allows the user to enter content_model data.
        :return: A tuple composed of 3 strings in this order: sdk, group id, artifact id.
        """
        return self.__get_prefix(), self.__get_name()

    def __get_prefix(self) -> str:
        """
        Retrieves the value of the prefix to use to generate a content_model.
        :return: The value of the prefix to use to generate the content_model.
        """
        return self.get_input("Please enter the prefix of the content_model ")

    def __get_name(self) -> str:
        """
        Retrieves the value of the name to use to generate a content_model.
        :return: The value of the name to use to generate the content_model.
        """
        return self.get_input("Please enter the name of the content_model ")
