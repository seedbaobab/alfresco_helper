from typing import Optional
from xml.etree.ElementTree import Element, Comment

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
        super().__init__(True, {"xmlns": "http://www.alfresco.org/model/dictionary/1.0"})

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

    def create_content_model(self, content_model_file_path: str, prefix: str, name: str, description: Optional[str],
                             author: Optional[str]):
        model: Element = Element("model")
        model.set("name", "{0}:{1}".format(prefix, name))

        # Set xml namespace.
        if self.namespaces is not None:
            for item in self.namespaces:
                model.set(item[0], item[1])

        model.append(Comment(" Optional meta-data about the model "))

        # Set the description
        description_node: Element = Element("description")
        description_node.text = description if description is not None else "SET THE PROJECT DESCRIPTION"
        model.append(description_node)

        # Set the author
        author_node: Element = Element("author")
        author_node.text = author if author is not None else "Alfresco Helper Script 1.0.0"
        model.append(author_node)

        # Set the version
        version_node: Element = Element("version")
        version_node.text = "1.0.0"
        model.append(version_node)

        # Set the imports
        imports_node: Element = Element("imports")
        imports_node.append(Comment(" Import Alfresco Dictionary Definitions "))
        # First import
        import1: Element = Element("import")
        import1.set("uri", "http://www.alfresco.org/model/dictionary/1.0")
        import1.set("prefix", "d")
        imports_node.append(import1)

        # Second import
        import2: Element = Element("import")
        import2.set("uri", "http://www.alfresco.org/model/content/1.0")
        import2.set("prefix", "cm")
        imports_node.append(import2)

        # Set the namespaces.
        namespaces_node: Element = Element("namespaces")
        # Set a namespace
        namespace_node: Element = Element("namespace")
        namespace_node.set("uri", "http://www.{0}.org/model/content/1.0".format(name.lower()))
        namespace_node.set("prefix", prefix)
        namespaces_node.append(namespace_node)

        # Add the import to the model.
        model.append(imports_node)
        # Add the import to the model.
        model.append(Comment(" Custom namespace for the '{0}:{1}' model ".format(prefix, name)))
        model.append(namespaces_node)

        # Write the XML file.
        self._write(model, content_model_file_path)

    def find_aspect(self, content_model: ContentModel, aspect: str) -> Optional[Element]:
        """
        Finds an aspect's node in its content model.
        :param content_model: A content model data model.
        :param aspect: The name of the aspect.
        :return: The aspect node otherwise None.
        """
        return self._get_root(content_model.path).find(".//{0}aspects/{0}aspect[@name='{1}:{2}']".format(
            self.get_namespace("xmlns"), content_model.prefix, aspect))

    def find_type(self, content_model: ContentModel, type_name: str) -> Optional[Element]:
        return self._get_root(content_model.path).find(".//{0}types/{0}type[@name='{1}:{2}']".format(
            self.get_namespace("xmlns"), content_model.prefix, type_name))

    def add_aspect(self, content_model: ContentModel, name: str, title: str, description: str):
        root: Element = self._get_root(content_model.path)

        aspect: Element = Element("aspect")
        aspect.set("name", "{0}:{1}".format(content_model.prefix, name))

        if not StringHelper.is_empty(title):
            title_node: Element = Element("title")
            title_node.text = title
            aspect.append(title_node)

        if not StringHelper.is_empty(description):
            description_node: Element = Element("description")
            description_node.text = description
            aspect.append(description_node)

        properties: Element = Element("properties")
        aspect.append(properties)

        add_to_root: bool = False
        aspects: Element = root.find(".//{0}aspects".format(self.get_namespace("xmlns"), content_model.prefix, aspect))
        if aspects is None:
            aspects = Element("aspects")
            add_to_root = True

        aspects.append(Comment(" Definition of aspect '{0}'. ".format(name)))
        aspects.append(aspect)

        if add_to_root:
            root.append(aspects)

        self._write(root, content_model.path)

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

        self._write(root, content_model.path)
        self.clean_blank_line(content_model.path)
