from api.mvc.model.data.project_model import ProjectModel
from api_core.mvc.service.file.xml_file_service import XmlFileService


class ShareConfigFileService(XmlFileService):
    """

    """

    def __init__(self):
        """

        """
        super().__init__(False, None)

    def reset(self, project: ProjectModel):
        pass
