from abc import ABC


class IContentModel(ABC):

    def __init__(self, prefix: str):
        self.__prefix: str = prefix

    @property
    def prefix(self):
        return self.__prefix
