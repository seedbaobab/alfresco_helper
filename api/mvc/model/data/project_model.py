import os

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.i_project_model import IProjectModel


class ProjectModel(IProjectModel):
    """
    Data model for a project.
    """

    def __init__(self, sdk: str, group_id: str, artifact_id: str, path: str):
        """
        Initialize a new instance of the 'ProjectModel' class.
        :param sdk: The project SDK.
        :param group_id: The project group id.
        :param path: The project path.
        """
        super().__init__(path, artifact_id)

        self.__sdk: str = sdk
        self.__path: path = path
        self.__group_id: str = group_id
        self.__content_models: list[ContentModel] = []
        self.__pom_path: str = "{1}{0}pom.xml".format(os.sep, self._path)
        self.__content_model_relative_folder_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}" \
                                                         "module{0}{2}-platform{0}model"\
            .format(os.sep, self._path, self._artifact_id)
        self.__content_model_folder_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}" \
                                                "module{0}{2}-platform{0}model".format(os.sep, self._path,
                                                                                       self._artifact_id)

        self.__content_model_message_relative_folder_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}" \
                                                                 "alfresco{0}module{0}{2}-platform{0}messages"\
            .format(os.sep, self._path, self._artifact_id)

        self.__bootstrap_file_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}module{0}{2}-" \
                                          "platform{0}context{0}bootstrap-context.xml".format(os.sep, path, artifact_id)

        self.__share_config_file: str = "{1}{0}{2}-share{0}src{0}main{0}resources{0}META-INF{0}share-config-custom.xml"\
            .format(os.sep, path, artifact_id)

        self.__integration_tests_filepath: str = "{1}{0}{2}-integration-tests{0}src".format(os.sep, path, artifact_id)

        self.__platform_java_filepath: str = "{1}{0}{2}-platform{0}src{0}main{0}java".format(os.sep, path, artifact_id)

        self.__platform_extension_folder: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}extension"\
            .format(os.sep, path, artifact_id)

        self.__service_context_filepath: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}module{0}" \
                                               "{2}-platform{0}context{0}service-context.xml"\
            .format(os.sep, path, artifact_id)

        self.__workflow_process_folder = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}module{0}" \
                                         "{2}-platform{0}workflow".format(os.sep, path, artifact_id)

        self.__share_message_folder = "{1}{0}{2}-share{0}src{0}main{0}resources{0}alfresco{0}web-extension{0}message"\
            .format(os.sep, path, artifact_id)

        self.__share_site_data_extension = "{1}{0}{2}-share{0}src{0}main{0}resources{0}alfresco{0}web-extensions{0}" \
                                           "site-data{0}extensions".format(os.sep, path, artifact_id)

        self.__platform_webscript_filepath: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}module{0}" \
                                                  "{2}-platform{0}context{0}webscript-context.xml"\
            .format(os.sep, path, artifact_id)

        self.__share_slingshot_application_context_filepath: str = "{1}{0}{2}-share{0}src{0}main{0}resources{0}" \
                                                                   "alfresco{0}web-extension{0}{2}-share-slingshot-" \
                                                                   "application-context.xml".format(os.sep, path,
                                                                                                    artifact_id)

    @property
    def platform_unit_test_folder(self) -> str:
        return "{1}{0}{2}-platform{0}src{0}test{0}java".format(os.sep, self.__path, self._artifact_id)

    @property
    def group_id(self) -> str:
        return self.__group_id

    @property
    def share_slingshot_application_context_filepath(self) -> str:
        return self.__share_slingshot_application_context_filepath

    @property
    def platform_webscript_filepath(self) -> str:
        return self.__platform_webscript_filepath

    @property
    def share_message_folder(self) -> str:
        return "{1}{0}{2}-share{0}src{0}main{0}resources{0}alfresco{0}web-extension{0}messages"\
            .format(os.sep, self.__path, self._artifact_id)

    @property
    def share_site_data_extension(self) -> str:
        return "{1}{0}{2}-share{0}src{0}main{0}resources{0}alfresco{0}web-extension{0}site-data{0}extensions"\
            .format(os.sep, self.__path, self._artifact_id)

    @property
    def workflow_process_folder(self) -> str:
        return self.__workflow_process_folder

    @property
    def service_context_filepath(self) -> str:
        return "{1}{0}{2}-platform{0}src{0}main{0}resources{0}alfresco{0}module{0}{2}-platform{0}context{0}" \
               "service-context.xml".format(os.sep, self.__path, self._artifact_id)

    @property
    def platform_extension_folder(self) -> str:
        return self.__platform_extension_folder

    @property
    def platform_java_folder(self) -> str:
        return self.__platform_java_filepath

    @property
    def integration_tests_filepath(self) -> str:
        return self.__integration_tests_filepath

    @property
    def share_config_filepath(self) -> str:
        return self.__share_config_file

    @property
    def bootstrap_filepath(self) -> str:
        return self.__bootstrap_file_path

    @property
    def artifact_id(self) -> str:
        return self._artifact_id

    @property
    def content_model_folder(self) -> str:
        return self.__content_model_folder_path

    @property
    def content_models(self) -> list[ContentModel]:
        return self.__content_models

    @property
    def content_model_relative_folder_path(self) -> str:
        return self.__content_model_relative_folder_path

    def add_content_model(self, content_model: ContentModel):
        self.__content_models.append(content_model)
