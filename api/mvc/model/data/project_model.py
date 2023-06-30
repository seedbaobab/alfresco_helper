import os

from api.mvc.model.data.content_model import ContentModel


class ProjectModel:
    """
    Data model for a project.
    """

    def __init__(self, sdk: str, group_id: str, artifact_id: str, path: str):
        """
        Initialize a new instance of the 'ProjectModel' class.
        :param sdk: The project SDK.
        :param group_id: The project group id.
        :param artifact_id: The project artifact id.
        :param path: The project path.
        """
        self.__sdk: str = sdk
        self.__path: str = path
        self.__group_id: str = group_id
        self.__artifact_id: str = artifact_id
        self.__content_models: list[ContentModel] = []
        self.__pom_path: str = "{1}{0}pom.xml".format(os.sep, self.__path)
        self.__content_model_folder_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}module{0}" \
                                                "{2}-platform{0}model".format(os.sep, self.__path, self.__artifact_id)
        self.__content_model_relative_folder_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}" \
                                                         "module{0}{2}-platform{0}model".format(os.sep, self.__path,
                                                                                                self.__artifact_id)

    @property
    def artifact_id(self) -> str:
        return self.__artifact_id

    @property
    def content_model_folder(self) -> str:
        return self.__content_model_folder_path

    @property
    def content_model_relative_folder_path(self) -> str:
        return self.__content_model_relative_folder_path

    def add_content_model(self, content_model: ContentModel):
        self.__content_models.append(content_model)
