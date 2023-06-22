import os
from xml.etree.ElementTree import Element

from api_core.exception.api_exception import ApiException
from api_core.helper.string_helper import StringHelper
from api_core.mvc.service.file.xml_file_service import XmlFileService


class PomService(XmlFileService):
    """
    Service class for managing POM type xml files.
    """

    def __init__(self):
        """
        Initialize a new instance of 'PomService' class.
        """
        super().__init__("http://maven.apache.org/POM/4.0.0")

    def extract_sdk(self, pom_path: str) -> str:
        """
        Extract the value contained in the 'alfresco.sdk.version' node from the pom file.
        :param pom_path: The absolute path to the pom file of the Alfresco AIO project.
        :return: The value of the 'alfresco.sdk.version' node.
        """
        root: Element = self._get_root(pom_path)
        xmlns: str = self._extract_xmlns(root)

        node: Element = root.find(".//{0}properties/{0}alfresco.sdk.version".format(xmlns))

        # Verification that the node is not empty.
        if node is None:
            raise ApiException("The pom file does not contain any 'alfresco.sdk.version' node.")

        # Verification that the node value is not empty.
        elif StringHelper.is_empty(node.text):
            raise ApiException("The 'alfresco.sdk.version' node in the pom file must have a value.")

        # return the node value.
        return node.text

    def extract_group_id(self, pom_path: str) -> str:
        """
        Extract the value contained in the 'groupId' node from the pom file.
        :param pom_path: The absolute path to the pom file of the Alfresco AIO project.
        :return: The value of the 'groupId' node.
        """
        root: Element = self._get_root(pom_path)
        xmlns: str = self._extract_xmlns(root)

        node: Element = root.find(".//{0}groupId".format(xmlns))

        # Verification that the node is not empty.
        if node is None:
            raise ApiException("The pom file does not contain any 'groupId' node.")

        # Verification that the node value is not empty.
        elif StringHelper.is_empty(node.text):
            raise ApiException("The 'groupId' node in the pom file must have a value.")

        # return the node value.
        return node.text

    def extract_artifact_id(self, pom_path: str) -> str:
        """
        Extract the value contained in the 'artifactId' node from the pom file.
        :param pom_path: The absolute path to the pom file of the Alfresco AIO project.
        :return: The value of the 'artifactId' node.
        """
        root: Element = self._get_root(pom_path)
        xmlns: str = self._extract_xmlns(root)

        node: Element = root.find(".//{0}artifactId".format(xmlns))
        # Verification that the node is not empty.
        if node is None:
            raise ApiException("The pom file does not contain any 'artifactId' node.")

        # Verification that the node value is not empty.
        elif StringHelper.is_empty(node.text):
            raise ApiException("The 'artifactId' node in the pom file must have a value.")

        # return the node value.
        return node.text
