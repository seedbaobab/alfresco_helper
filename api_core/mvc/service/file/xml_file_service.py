from __future__ import annotations

from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from api_core.exception.api_exception import ApiException


class XmlFileService:
    """
    Service class for managing XML files.
    """

    def __init__(self, use_xml_declaration: bool, namespaces: Optional[dict[str, str]]):
        """
        Initialize a new instance of 'XmlFileService' class.
        :type use_xml_declaration: Indicates whether the file must declare its version of XML.
        :param namespaces: The XML namespace.
        """
        self.__indent: str = "   "
        self.__use_xml_declaration: bool = use_xml_declaration
        self.__namespaces: Optional[dict[str, str]] = namespaces

    @property
    def namespaces(self) -> Optional[list[tuple[str, str]]]:
        return None if self.__namespaces is None else self.__namespaces.items()

    def get_namespace(self, prefix: str):
        return "{" + self.__namespaces[prefix] + "}"

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

    def _write(self, root: Element, path: str):
        tree = ElementTree.ElementTree(root)
        ElementTree.indent(tree, self.__indent)
        tree.write(path, encoding="utf-8", xml_declaration=self.__use_xml_declaration)

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
        if self.__namespaces is not None:
            for item in self.__namespaces.items():
                ElementTree.register_namespace('', item[1])
        # Return the xml root node.
        return ElementTree.parse(xml_file_path).getroot()
