from xml.etree.ElementTree import Element, Comment

from api.mvc.model.data.project_model import ProjectModel
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.service.file.xml_file_service import XmlFileService


class ServiceContextFileService(XmlFileService):
    """

    """

    def __init__(self):
        """

        """
        super().__init__(True, {"xmlns": "http://www.springframework.org/schema/beans"})

    def reset(self, project: ProjectModel):
        """
        Reset the 'service-context.xml' file of the platform project of the alfresco project.
        :param project: The project data model.
        """
        # Delete file.
        FileFolderHelper.remove_file(project.service_context_filepath)

        # File rewritten.
        # Creating the 'alfresco-config' node.
        root: Element = Element("beans")
        root.set("xmlns", "http://www.springframework.org/schema/beans")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "http://www.springframework.org/schema/beans "
                                       "http://www.springframework.org/schema/beans/spring-beans-3.0.xsd")

        self._write(root, project.service_context_filepath)
