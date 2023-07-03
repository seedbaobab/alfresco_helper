import os

from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.i_project_model import IProjectModel
from api_core.helper.string_helper import StringHelper


class ContentModel:
    """
    Data model for a content_model.
    """

    def __init__(self, project: IProjectModel, prefix: str, name: str, path: str):
        """
        Initialize a new instance of 'ContentModel' class.
        :param prefix: The content_model prefix.
        :param name: The content_model name.
        :param path: The content_model path.
        """
        self.name: str = name
        self.path: str = path
        self.prefix: str = prefix
        self.aspects: list[AspectModel] = []
        # self.types: dict[str, TypeModel] = {}
        self.complete_name: str = "{0}:{1}".format(prefix, name)
        self.platform_message_file_path: str = "{1}{0}{2}".format(os.sep,
                                                                  project.content_model_message_absolute_folder_path,
                                                                  self.__get_platform_filename())

    def __get_platform_filename(self):
        filename: str = StringHelper.to_snake_case(self.name)
        filename = filename.lower()
        print(filename)
        if not filename.endswith("-model"):
            print("true")
            filename += "-model"
        return "{0}.properties".format(filename)

    def add_aspect(self, aspect: AspectModel):
        """
        Add an aspect in the model.
        :param aspect: The aspect to add to the model.
        """
        self.aspects.append(aspect)

    # def has_aspect(self, name: str) -> bool:
    #     """
    #     Indicates whether the aspect is already loaded in the content_model.
    #     :param name: The aspect name.
    #     :return: True if the aspect is already loaded, false otherwise.
    #     """
    #     return name in self.aspects
