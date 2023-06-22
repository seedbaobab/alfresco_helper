from typing import Optional
from xml.etree.ElementTree import Element

from api.mvc.model.data.content_model import ContentModel
from api_core.exception.api_exception import ApiException
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.helper.string_helper import StringHelper
from api_core.mvc.service.file.xml_file_service import XmlFileService


class ContentModelFileService(XmlFileService):
    """
    Class used to manage content-model XML files.
    """

    def __init__(self):
        """
        Initialize a new instance of 'ContentModelService' class.
        """
        super().__init__("http://www.alfresco.org/model/dictionary/1.0")

    def extract_prefix(self, content_model_file_path: str) -> str:
        """
        Extracts the content model prefix.
        :param content_model_file_path: The path to the content model file.
        :return: The content model prefix.
        """
        root: Element = self._get_root(content_model_file_path)
        filename: str = FileFolderHelper.extract_filename_from_path(content_model_file_path)

        # Verification that the attribute exists.
        if not ("name" in root.attrib):
            raise ApiException("Content model file '{0}' does not have the necessary 'namespace' node."
                               .format(filename))
        # Verification that the attribute has a value.
        if StringHelper.is_empty(root.attrib["name"]):
            raise ApiException("The 'name' attribute of the content model file '{0}' is not entered. The latter is "
                               "mandatory.".format(filename))
        # Data recovery.
        try:
            return root.attrib["name"].rsplit(":", 1)[0]
        except IndexError:
            raise ApiException("The value of the 'name' attribute of the source node is invalid. This must be composed "
                               "as follows: prefix:name")

    def extract_name(self, content_model_file_path: str) -> str:
        """
        Extracts the content model name.
        :param content_model_file_path: The path to the content model file.
        :return: The content model name.
        """
        root: Element = self._get_root(content_model_file_path)
        filename: str = FileFolderHelper.extract_filename_from_path(content_model_file_path)

        # Verification that the attribute exists.
        if not ("name" in root.attrib):
            raise ApiException("Content model file '{0}' does not have the necessary 'namespace' node."
                               .format(filename))
        # Verification that the attribute has a value.
        if StringHelper.is_empty(root.attrib["name"]):
            raise ApiException("The 'name' attribute of the content model file '{0}' is not entered. The latter is "
                               "mandatory.".format(filename))
        # Data recovery.
        try:
            return root.attrib["name"].rsplit(":", 1)[1]
        except IndexError:
            raise ApiException("The value of the 'name' attribute of the source node is invalid. This must be composed "
                               "as follows: prefix:name")

    def find_aspect(self, content_model: ContentModel, aspect: str) -> Optional[Element]:
        """
        Finds an aspect's node in its content model.
        :param content_model: A content model data model.
        :param aspect: The name of the aspect.
        :return: The aspect node otherwise None.
        """
        root: Element = self._get_root(content_model.path)
        xmlns: str = self._extract_xmlns(root)

        return root.find(".//{0}aspects/{0}aspect[@name='{1}:{2}']".format(xmlns, content_model.prefix, aspect))

    def find_type(self, content_model: ContentModel, aspect: str) -> Optional[Element]:
        root: Element = self._get_root(content_model.path)
        xmlns: str = self._extract_xmlns(root)

        return root.find(".//{0}types/{0}type[@name='{1}:{2}']".format(xmlns, content_model.prefix, aspect))

    def add_aspect(self, content_model: ContentModel, name: str, title: str, description: str):
        root: Element = self._get_root(content_model.path)
        xmlns: str = self._extract_xmlns(root)

        aspect: Element = Element("aspect")
        aspect.set("name", "{0}:{1}".format(content_model.prefix, name))

        if not StringHelper.is_empty(title):
            title_node: Element = Element("title")
            title_node.text = title
            aspect.append(title_node)

        if not StringHelper.is_empty(description):
            description_node: Element = Element("description")
            description_node.text = description_node
            aspect.append(description_node)

        properties: Element = Element("properties")
        aspect.append(properties)

        aspects: Element = root.find(".//{0}aspects".format(xmlns, content_model.prefix, aspect))
        if aspects is None:
            aspects = Element("aspects")
            aspects.append(aspect)
        else:
            aspects.append(aspect)
            root.append(aspects)

        self._write_xml_pretty(root, content_model.path, True)
        self.clean_blank_line(content_model.path)

    def add_type(self, content_model: ContentModel, name: str, title: str, description: str):
        root: Element = self._get_root(content_model.path)
        xmlns: str = self._extract_xmlns(root)

        type_node: Element = Element("type")
        type_node.set("name", "{0}:{1}".format(content_model.prefix, name))

        if not StringHelper.is_empty(title):
            title_node: Element = Element("title")
            title_node.text = title
            type_node.append(title_node)

        if not StringHelper.is_empty(description):
            description_node: Element = Element("description")
            description_node.text = description_node
            type_node.append(description_node)

        properties: Element = Element("properties")
        type_node.append(properties)

        types: Element = root.find(".//{0}types".format(xmlns, content_model.prefix, type_node))
        if types is None:
            aspects = Element("aspects")
            aspects.append(type_node)
        else:
            types.append(type_node)
            root.append(types)

        self._write_xml_pretty(root, content_model.path, True)
        self.clean_blank_line(content_model.path)