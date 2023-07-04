from typing import Optional
from xml.etree.ElementTree import Element

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.service.file.xml_file_service import XmlFileService


class BootstrapFileService(XmlFileService):
    """
    Class allowing to manage the bootstrap file of the alfresco platform project.
    """

    def __init__(self):
        """
        Initialize a new instance of 'BootstrapFileService' class.
        """
        super().__init__(True, {"xmlns": "http://www.springframework.org/schema/beans"})

    def reset(self, project: ProjectModel):
        """
        Reset the 'bootstrap-context.xml' file of the platform project of the alfresco project.
        :param project: The project data model.
        """
        # Delete file.
        FileFolderHelper.remove_file(project.bootstrap_filepath)
        # File rewritten.
        # Creating the 'beans' node.
        beans: Element = Element("beans")
        beans.set("xmlns", "http://www.springframework.org/schema/beans")
        beans.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        beans.set("xsi:schemaLocation", "http://www.springframework.org/schema/beans "
                                        "http://www.springframework.org/schema/beans/spring-beans-3.0.xsd")
        # Add node beans in the root.
        # Writing file.
        self._write(beans, project.bootstrap_filepath)

    def add_content_model(self, project: ProjectModel, content_model: ContentModel):
        """
        Add a content-model file.
        :param project: The project data model.
        :param content_model: The content model's data model.
        """
        root: Element = self._get_root(project.bootstrap_filepath)

        # Stop if the content model is already inserted.
        if self.__get_content_model(root, project, content_model, "models") is not None:
            return

        filename: str = self.__get_value_filename(content_model, "models")

        # Creation of the value to be created.
        value: Element = Element("value")
        value.text = "alfresco/module/${project.artifactId}/model/" + filename

        # Checking that the parent node of 'value' exists.
        (is_created, list_node) = self.__get_create_list_node(root, project, "models")
        list_node.append(value)

        if is_created:
            (is_created, property_node) = self.__get_create_property_node(root, project, "models")
            property_node.append(list_node)

            if is_created:
                (is_created, bean) = self.__get_create_bean_node(root, project)
                bean.append(property_node)

                if is_created:
                    root.append(bean)

        # File rewritten.
        self._write(root, project.bootstrap_filepath)

    def remove_content_model(self, project: ProjectModel, content_model: ContentModel):
        """
        Remove a content model from the bootstrap file.
        :param project: The project data model.
        :param content_model: The content model's data model.
        """
        # Retrieval of search items.
        root: Element = self._get_root(project.bootstrap_filepath)

        # Recovery of the node to delete. If it does not exist: stop.
        value: Element = self.__get_content_model(root, project, content_model, "models")
        if value is None:
            return

        # Retrieving the node that should contain the node to delete. If it does not exist: stop.
        list_node: Element = self.__get_content_model_list_node(root, project, "models")
        if list_node is None:
            return

        # Remove value node.
        list_node.remove(value)
        # File rewritten.
        self._write(root, project.bootstrap_filepath)

    def add_message_content_model(self, project: ProjectModel, content_model: ContentModel):
        # Retrieval of search items.
        root: Element = self._get_root(project.bootstrap_filepath)
        namespace: str = self.get_namespace("xmlns")

        # Verification that the 'value' node exists.
        value: Element = self.__get_content_model(root, project, content_model, "labels")
        if value is not None:
            return

        filename: str = self.__get_value_filename(content_model, "labels")
        value = Element("value")
        value.text = "alfresco/module/${project.artifactId}/messages/" + filename[:filename.rfind(".properties")]

        # Checking that the parent node of 'value' exists.
        (is_created, list_node) = self.__get_create_list_node(root, project, "labels")
        list_node.append(value)

        if is_created:
            (is_created, property_node) = self.__get_create_property_node(root, project, "labels")
            property_node.append(list_node)

            if is_created:
                (is_created, bean) = self.__get_create_bean_node(root, project)
                bean.append(property_node)

                if is_created:
                    bean.append(property_node)
                    root.append(bean)

        # File rewritten.
        self._write(root, project.bootstrap_filepath)

    def remove_message_content_model(self, project: ProjectModel, content_model: ContentModel):
        """
        Remove a content model from the bootstrap file.
        :param project: The project data model.
        :param content_model: The content model's data model.
        """
        # Retrieval of search items.
        root: Element = self._get_root(project.bootstrap_filepath)

        # Recovery of the node to delete. If it does not exist: stop.
        value: Element = self.__get_content_model(root, project, content_model, "labels")
        if value is None:
            return

        # Retrieving the node that should contain the node to delete. If it does not exist: stop.
        list_node: Element = self.__get_content_model_list_node(root, project, "labels")
        if list_node is None:
            return

        # Remove value node.
        list_node.remove(value)
        # File rewritten.
        self._write(root, project.bootstrap_filepath)

    def __get_create_list_node(self, root: Element, project: ProjectModel, property_type: str) -> tuple[bool, Element]:
        """
        Finds or creates the desired node.
        :param root: The root of the XML file.
        :param project: The project data model.
        :return: A tuple composed of a boolean true if the node has been created otherwise false, and the node.
        """
        namespace: str = self.get_namespace("xmlns")
        node: Optional[Element] = root.find(".//{0}bean[@id='{1}-platform.dictionaryBootstrap']/{0}property[@name="
                                            "'{2}']/{0}list".format(namespace, project.artifact_id, property_type))
        return (True, Element("list")) if node is None else (False, node)

    def __get_create_property_node(self, root: Element, project: ProjectModel, property_type: str) \
            -> tuple[bool, Element]:
        """
        Finds or creates the desired node.
        :param root: The root of the XML file.
        :param project: The project data model.
        :return: A tuple composed of a boolean true if the node has been created otherwise false, and the node.
        """
        namespace: str = self.get_namespace("xmlns")
        node: Optional[Element] = root.find(".//{0}bean[@id='{1}-platform.dictionaryBootstrap']/{0}property"
                                            "[@name='{2}']".format(namespace, project.artifact_id, property_type))
        if node is None:
            node = Element("property")
            node.set("name", property_type)
            return True, node

        return False, node

    def __get_create_bean_node(self, root: Element, project: ProjectModel) -> tuple[bool, Element]:
        """
        Finds or creates the desired node.
        :param root: The root of the XML file.
        :param project: The project data model.
        :return: A tuple composed of a boolean true if the node has been created otherwise false, and the node.
        """
        namespace: str = self.get_namespace("xmlns")
        node: Optional[Element] = root.find(".//{0}bean[@id='{1}-platform.dictionaryBootstrap']"
                                            .format(namespace, project.artifact_id))
        if node is None:
            node = Element("bean")
            node.set("id", "{0}-platform.dictionaryBootstrap".format(project.artifact_id))
            node.set("parent", "dictionaryModelBootstrap")
            node.set("depends-on", "dictionaryBootstrap")
            return True, node

        return False, node

    def __get_content_model_list_node(self, root, project: ProjectModel, property_type: str) -> Optional[Element]:
        """
        Returns the content-models list file node.
        :param root: The root of the XML file.
        :param project: The project data model.
        :return: The content-models list file node.
        """
        # Retrieval of search items.
        namespace: str = self.get_namespace("xmlns")
        # Retrieving the list of node
        return root.find(".//{0}bean[@id='{1}-platform.dictionaryBootstrap']/{0}property[@name='{2}']/{0}list"
                         .format(namespace, project.artifact_id, property_type))

    def __get_content_model(self, root: Element, project: ProjectModel, content_model: ContentModel,
                            property_type: str) -> Optional[Element]:
        """
        Returns the content model file node.
        :param root: The root of the XML file.
        :param project: The project data model.
        :param content_model: The content model's data model.
        :return: The content model file node.
        """
        # File name retrieval.
        filename: str = self.__get_value_filename(content_model, property_type)
        # Retrieval of search items.
        namespace: str = self.get_namespace("xmlns")

        # Retrieving the list of nodes
        values: list[Element] = root.findall(".//{0}bean[@id='{1}-platform.dictionaryBootstrap']/{0}property"
                                             "[@name='{2}']/{0}list/{0}value"
                                             .format(namespace, project.artifact_id, property_type))
        # Node search.
        index: int = 0
        maximum: int = len(values)
        search: str = "alfresco/module/${project.artifactId}/" + "{0}/{1}"\
            .format("model" if property_type.__eq__("models") else "messages", filename)

        while index.__lt__(maximum) and values[index].text.__ne__(search):
            index += 1

        # Return of the node.
        return None if index.__eq__(maximum) else values[index]

    @staticmethod
    def __get_value_filename(content_model: ContentModel, property_type: str) -> str:
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.path)
        if property_type.__eq__("labels"):
            filename = filename[:filename.rfind(".properties")-2]
        return filename
