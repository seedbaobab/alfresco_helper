from __future__ import annotations

from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from api_core.exception.api_exception import ApiException
from api_core.helper.string_helper import StringHelper


class XmlFileService:
    """
    Service class for managing XML files.
    """

    def __init__(self, namespace: str | None):
        """
        Initialize a new instance of 'XmlFileService' class.
        :param namespace: The XML namespace.
        """
        self.namespace: str | None = namespace

    @staticmethod
    def clean_blank_line(xml_path: str):
        """
        Remove blank line of pom.
        :param xml_path: A project's pom path.
        """
        buffer: str = ""
        with open(xml_path, "r") as reader:
            for line in reader:
                if line.strip():
                    buffer += line

        with open(xml_path, "w") as writer:
            writer.write(buffer)

    @staticmethod
    def _write_xml_pretty(root: Element, path: str, xml_declaration: bool):
        xml_str = minidom.parseString(ElementTree.tostring(root, xml_declaration=xml_declaration)). \
            toprettyxml(indent="   ")
        with open(path, "wb") as f:
            f.write(xml_str.encode('utf-8'))

    @staticmethod
    def _extract_xmlns(pom_root: Element) -> str:
        """
        Get the xml xmlns if it exists.
        :param pom_root: The xml root element.
        :return: The pom xmlns found.
        """
        if pom_root.tag[0].__eq__("{"):
            return pom_root.tag[0: pom_root.tag.rindex("}") + 1]
        raise ApiException("The xml file has no xmlns set.")

    def _get_root(self, xml_file_path: str) -> Element:
        """
        Get the XML root node.
        :param xml_file_path: Path to the xml file.
        :return: The xml root node.
        """
        if not StringHelper.is_empty(self.namespace):
            ElementTree.register_namespace('', self.namespace)
        # Return the xml root node.
        return ElementTree.parse(xml_file_path).getroot()
