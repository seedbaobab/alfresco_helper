import os


class IProjectModel:
    def __init__(self, path: str, artifact_id: str):
        """
        :param path: The project path.
        :param artifact_id: The project artifact id.
        """
        self._path: str = path
        self._artifact_id: str = artifact_id
        self.__content_model_message_absolute_folder_path: str = "{1}{0}{2}-platform{0}src{0}main{0}resources{0}" \
                                                                 "alfresco{0}module{0}{2}-platform{0}messages"\
            .format(os.sep, self._path, self._artifact_id)

        self.__share_messages_folder: str = "{1}{0}{2}-share{0}src{0}main{0}resources{0}alfresco{0}web-extension{0}" \
                                            "messages".format(os.sep, self._path, self._artifact_id)

    @property
    def content_model_message_absolute_folder_path(self) -> str:
        return self.__content_model_message_absolute_folder_path

    @property
    def share_messages_folder(self) -> str:
        return self.__share_messages_folder
