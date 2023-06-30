from api.mvc.model.data.aspect_model import AspectModel


class ContentModel:
    """
    Data model for a content_model.
    """

    def __init__(self, prefix: str, name: str, path: str):
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
        self.complete_name = "{0}:{1}".format(prefix, name)

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
