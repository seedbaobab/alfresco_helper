from api.mvc.model.data.i_content_model import IContentModel


class IDataModel:
    def __init__(self, icm: IContentModel):
        self.__icm: IContentModel = icm

    @property
    def prefix(self) -> str:
        """
        Get the data name.
        :return: The data name.
        """
        return self.__icm.prefix

