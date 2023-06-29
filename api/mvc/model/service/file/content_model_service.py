from typing import Optional
from xml.etree.ElementTree import Element, Comment

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.data_type import DataType
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

    def extract_content_model_prefix(self, content_model_file_path: str) -> str:
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

    def extract_content_model_name(self, content_model_file_path: str) -> str:
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

    def find_data(self, content_model: ContentModel, typology: str, data: str) -> Optional[Element]:
        """
        Finds data's node in its content model.
        :param content_model: A data model of a content-model.
        :param typology: The data typology.
        :param data: The name of the data.
        :return: The data node, otherwise None.
        """
        return self._get_root(content_model.path).find(".//{0}{3}s/{0}{3}[@name='{1}:{2}']".format(
            self.get_namespace("xmlns"), content_model.prefix, data, typology))

    def find_aspect(self, content_model: ContentModel, aspect: str) -> Optional[Element]:
        """
        Finds an aspect's node in its content model.
        :param content_model: A data model of a content-model.
        :param aspect: The name of the aspect.
        :return: The aspect node, otherwise None.
        """
        return self._get_root(content_model.path).find(".//{0}aspects/{0}aspect[@name='{1}:{2}']".format(
            self.get_namespace("xmlns"), content_model.prefix, aspect))

    def get_aspects_name(self, content_model: ContentModel) -> list[str]:
        """
        Finds an all aspects name in its content model.
        :param content_model: A data model of a content-model.
        :return: The list of aspects name.
        """
        aspects: list[str] = []
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        for aspect in self._get_root(content_model.path).findall(".//{0}aspects/{0}aspect".format(
                self.get_namespace("xmlns"))):
            aspects.append(self.__extract_aspect_name(aspect, filename))
        return aspects

    def get_data_names(self, content_model: ContentModel, typology: str) -> list[str]:
        """
        Finds an all aspects name in its content model.
        :param typology: The type of the data to get.
        :param content_model: A data model of a content-model.
        :return: The list of aspects name.
        """
        data_names: list[str] = []
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        for data in self._get_root(content_model.path).findall(".//{0}{1}s/{0}{1}".format(
                self.get_namespace("xmlns"), typology)):
            data_names.append(self.__extract_data_name(data, typology, filename))
        return data_names

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
            description_node.text = description
            type_node.append(description_node)

        properties: Element = Element("properties")
        type_node.append(properties)

        types: Element = root.find(".//{0}types".format(xmlns, content_model.prefix, type_node))
        if types is None:
            aspects = Element("types")
            aspects.append(type_node)
        else:
            types.append(type_node)
            root.append(types)

        self._write(root, content_model.path)

    def add_property(self, content_model: ContentModel, data: DataModel, name: str, title: Optional[str],
                     description: Optional[str], typology: str, mandatory: bool):
        root: Element = self._get_root(content_model.path)
        # Create the property
        prop: Element = Element("property")
        prop.set("name", "{0}:{1}".format(content_model.prefix, name))

        # Set the property's title.
        if not StringHelper.is_empty(title):
            title_node: Element = Element("title")
            title_node.text = title
            prop.append(title_node)

        # Set the property's description.
        if not StringHelper.is_empty(description):
            description_node: Element = Element("description")
            description_node.text = description
            prop.append(description_node)

        # Set the property's type.
        type_node: Element = Element("type")
        type_node.text = "d:{0}".format(typology)
        prop.append(type_node)

        # Set the property's mandatory.
        mandatory_node: Element = Element("mandatory")
        mandatory_node.text = "true" if mandatory else "false"
        prop.append(mandatory_node)

        data_node: Optional[Element] = root.find(".//{0}{3}s/{0}{3}[@name='{1}:{2}']"
                                                 .format(self.get_namespace("xmlns"), content_model.prefix, data.name,
                                                         data.typology))

        add_to_data: bool = False
        properties_node: Element = data_node.find(".//{0}properties".format(self.get_namespace("xmlns")))
        if properties_node is None:
            properties_node = Element("properties")
            add_to_data = True

        properties_node.append(prop)
        if add_to_data:
            data_node.append(properties_node)

        self._write(root, content_model.path)

    def add_extension(self, content_model: ContentModel, source: DataModel, parent: DataModel):
        namespace: str = self.get_namespace("xmlns")
        root: Element = self._get_root(content_model.path)

        source_node: Element = root.find(".//{0}{1}s/{0}{1}[@name='{2}:{3}']"
                                         .format(namespace, source.typology, content_model.prefix, source.name))
        parent_node: Optional[Element] = source_node.find("./{0}parent".format(namespace))

        add_parent: bool = True if parent_node is None else False
        if add_parent:
            parent_node = Element("parent")
        parent_node.text = "{0}:{1}".format(content_model.prefix, parent.name)
        if add_parent:
            source_node.insert(self.__get_properties_node_index(source_node), parent_node)

        self._write(root, content_model.path)

    def add_mandatory(self, content_model: ContentModel, source: DataModel, mandatory: DataModel):
        namespace: str = self.get_namespace("xmlns")
        root: Element = self._get_root(content_model.path)

        source_node: Element = root.find(".//{0}{1}s/{0}{1}[@name='{2}:{3}']"
                                         .format(namespace, source.typology, content_model.prefix, source.name))
        mandatory_node: Optional[Element] = source_node.find("./{0}mandatory-aspects".format(namespace))

        aspect: Element = Element("aspect")
        aspect.text = "{0}:{1}".format(content_model.prefix, mandatory.name)

        add_mandatory_node: bool = True if mandatory_node is None else False
        if add_mandatory_node:
            mandatory_node = Element("mandatory-aspects")
        mandatory_node.append(aspect)
        if add_mandatory_node:
            source_node.append(mandatory_node)

        self._write(root, content_model.path)

    def get_aspect_description(self, content_model: ContentModel, name: str) -> Optional[str]:
        """
        Retrieve the value of the description node of an aspect node.
        :param content_model: A data model of a content-model.
        :param name: The name of the aspect node.
        :return: The value of the aspect's description node.
        """
        return self.__get_data_description(content_model, DataType.ASPECT.name, name)

    def get_type_description(self, content_model: ContentModel, name: str) -> Optional[str]:
        """
        Retrieve the value of the description node of a type node.
        :param content_model: A data model of a content-model.
        :param name: The name of the type node.
        :return: The value of the type's description node.
        """
        return self.__get_data_description(content_model, DataType.TYPE.name, name)

    def get_aspect_title(self, content_model: ContentModel, name: str) -> Optional[str]:
        """
        Retrieve the value of the title node of an aspect node.
        :param content_model: A data model of a content-model.
        :param name: The name of the aspect node.
        :return: The value of the aspect's title node.
        """
        return self.__get_data_title(content_model, DataType.ASPECT.name, name)

    def get_aspect_parent(self, content_model: ContentModel, name: str) -> Optional[str]:
        """
        Retrieve the value of the parent node of an aspect node.
        :param content_model: A data model of a content-model.
        :param name: The name of the aspect node.
        :return: The value of the aspect's parent node.
        """
        return self.get_data_parent(content_model, DataType.ASPECT.value, name)

    def get_aspect_mandatory_aspects(self, content_model: ContentModel, name: str) -> list[str]:
        return self.__get_data_mandatory_aspects(content_model, DataType.ASPECT.value, name)

    def get_type_title(self, content_model: ContentModel, name: str) -> Optional[str]:
        """
        Retrieve the value of the title node of a type node.
        :param content_model: A data model of a content-model.
        :param name: The name of the type node.
        :return: The value of the type's title node.
        """
        return self.__get_data_title(content_model, DataType.TYPE.name, name)

    def get_type_parent(self, content_model: ContentModel, name: str) -> Optional[str]:
        """
        Retrieve the value of the title node of a type node.
        :param content_model: A data model of a content-model.
        :param name: The name of the type node.
        :return: The value of the type's title node.
        """
        return self.__get_data_title(content_model, DataType.TYPE.name, name)

    def __extract_aspect_name(self, aspect: Element, filename: str) -> str:
        """
        Extracts the aspect node name.
        :param aspect: The aspect node.
        :return: The aspect name.
        """
        return self.__extract_data_name(aspect, DataType.ASPECT.name, filename)

    def get_type_mandatory_aspects(self, content_model: ContentModel, name: str) -> list[str]:
        return self.__get_data_mandatory_aspects(content_model, DataType.TYPE.value, name)

    def __extract_type_name(self, type_node: Element, filename: str) -> str:
        """
        Extracts the aspect node name.
        :param type_node: The type node.
        :return: The type name.
        """
        return self.__extract_data_name(type_node, DataType.TYPE.value, filename)

    @staticmethod
    def __extract_data_name(data: Element, typology: str, filename: str) -> str:
        """
        Extracts the aspect node name.
        :param data: The aspect model.
        :return: The aspect name.
        """
        # Verification that the attribute exists.
        if not ("name" in data.attrib):
            raise ApiException("There is {1} in file '{0}' that has not been defined correctly. It lacks the "
                               "'name' attribute."
                               .format(filename, "an aspect" if typology.__eq__("aspect") else "a type"))

        # Verification that the attribute has a value.
        if StringHelper.is_empty(data.attrib["name"]):
            raise ApiException("There is {1} in file '{0}' that has not been defined correctly. The 'name' "
                               "attribute is null or empty."
                               .format(filename, "an aspect" if typology.__eq__("aspect") else "a type"))

        # Data recovery.
        try:
            return data.attrib["name"].rsplit(":", 1)[1]
        except IndexError:
            raise ApiException("There is {1} in file '{0}' whose name attribute was not set correctly. The "
                               "attribute value must be composed as follows: prefix:name"
                               .format(filename, "an aspect" if typology.__eq__("aspect") else "a type"))

    @staticmethod
    def __extract_property_name(prop: Element, filename: str) -> str:
        """
        Extracts the aspect node name.
        :param prop: The property node.
        :return: The aspect name.
        """
        # Verification that the attribute exists.
        if not ("name" in prop.attrib):
            raise ApiException("There is a property in file '{0}' that has not been defined correctly. It lacks the "
                               "'name' attribute."
                               .format(filename))

        # Verification that the attribute has a value.
        if StringHelper.is_empty(prop.attrib["name"]):
            raise ApiException("There is a property in file '{0}' that has not been defined correctly. The 'name' "
                               "attribute is null or empty."
                               .format(filename))

        # Data recovery.
        try:
            return prop.attrib["name"].rsplit(":", 1)[1]
        except IndexError:
            raise ApiException("There is a property in file '{0}' whose name attribute was not set correctly. The "
                               "attribute value must be composed as follows: prefix:name"
                               .format(filename))

    def __get_data_description(self, content_model: ContentModel, typology: str, name: str) -> Optional[str]:
        """
        Retrieve the value of the description node of a data node (aspect or type).
        :param content_model: A data model of a content-model.
        :param typology: The type of the node (aspect or type).
        :param name: The name of the data node.
        :return: The value of the data node description node.
        """
        description: Element = self._get_root(content_model.path) \
            .find(".//{0}{1}s/{0}{1}[@name='{2}:{3}']/{0}description"
                  .format(self.get_namespace("xmlns"), typology, content_model.prefix, name))
        return None if description is None else description.text

    def __get_data_title(self, content_model: ContentModel, typology: str, name: str) -> Optional[str]:
        """
        Retrieve the value of the title node of a data node (aspect or type).
        :param content_model: A data model of a content-model.
        :param typology: The type of the node (aspect or type).
        :param name: The name of the data node.
        :return: The value of the data node title node.
        """
        title: Element = self._get_root(content_model.path) \
            .find(".//{0}{1}s/{0}{1}[@name='{2}:{3}']/{0}title"
                  .format(self.get_namespace("xmlns"), typology, content_model.prefix, name))
        return None if title is None else title.text

    def get_data_parent(self, content_model: ContentModel, typology: str, name: str) -> Optional[str]:
        """
        Retrieve the value of the parent node of a data node (aspect or type).
        :param content_model: A data model of a content-model.
        :param typology: The type of the node (aspect or type).
        :param name: The name of the data node.
        :return: The value of the data node title node.
        """
        parent: Element = self._get_root(content_model.path) \
            .find(".//{0}{1}s/{0}{1}[@name='{2}:{3}']/{0}parent"
                  .format(self.get_namespace("xmlns"), typology, content_model.prefix, name))
        return None if parent is None else parent.text

    def __get_data_mandatory_aspects(self, content_model: ContentModel, typology: str, name: str) -> list[str]:
        result: list[str] = []
        root: Element = self._get_root(content_model.path)
        mandatory_aspects: list[Element] = root.findall(".//{0}{1}s/{0}{1}[@name='{2}:{3}']/{0}mandatory-aspects"
                                                        "/{0}aspect".format(self.get_namespace("xmlns"), typology,
                                                                            content_model.prefix, name))
        for mandatory_aspect in mandatory_aspects:
            result.append(mandatory_aspect.text)
        return result

    def __get_properties_node_index(self, data_node: Element) -> int:
        namespace: str = self.get_namespace("xmlns")
        children: list[Element] = data_node.findall(".//{0}*".format(namespace))
        maximum: int = len(children)
        index: int = 0

        while index.__lt__(maximum) and children[index].tag.__ne__("{0}properties".format(namespace)):
            index += 1

        return index if index.__lt__(maximum) else (index - 1)

    def get_properties(self, content_model: ContentModel) -> list[str]:
        result: list[str] = []
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        root: Element = self._get_root(content_model.path)
        for prop in root.findall(".//{0}aspects/{0}aspect/{0}properties/{0}property".format(
                self.get_namespace("xmlns"))):
            result.append(self.__extract_property_name(prop, filename))
        for prop in root.findall(".//{0}types/{0}type/{0}properties/{0}property".format(
                self.get_namespace("xmlns"))):
            result.append(self.__extract_property_name(prop, filename))
        return result
