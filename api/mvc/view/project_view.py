from api_core.mvc.view.view import View


class ProjectView(View):
    """
    View for the project controller.
    """

    def enter_project_data(self):
        """
        Allows the user to enter project data.
        :return: A tuple composed of 3 strings in this order: sdk, group id, artifact id.
        """
        return self.__get_sdk(), self.__get_group_id(), self.__get_artifact_id()

    def __get_sdk(self) -> str:
        """
        Retrieves the value of the SDK to use to generate an Alfresco All-In-One project.
        :return: The value of the SDK to use to generate an Alfresco All-In-One project.
        """
        return self.get_input("Please enter the sdk version to use for your Alfresco All-In-One project")

    def __get_group_id(self) -> str:
        """
        Retrieves the value of the group id to use to generate an Alfresco All-In-One project.
        :return: The value of the group id to use to generate an Alfresco All-In-One project.
        """
        return self.get_input("Please enter the group id value of your Alfresco All-In-One project")

    def __get_artifact_id(self) -> str:
        """
        Retrieves the value of the artifact id to use to generate an Alfresco All-In-One project.
        :return: The value of the artifact id to use to generate an Alfresco All-In-One project.
        """
        return self.get_input("Please enter the artifact id value of your Alfresco All-In-One project")
