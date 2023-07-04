from typing import Optional
from xml.etree.ElementTree import Element, Comment

from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.project_model import ProjectModel
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.service.file.xml_file_service import XmlFileService


class ShareSlingshotApplicationContext(XmlFileService):
    """

    """

    def __init__(self):
        """

        """
        super().__init__(True, {"xmlns": "http://www.springframework.org/schema/beans"})

    def reset(self, project: ProjectModel):
        """
        Reset the 'webscript-context.xml' file of the platform project of the alfresco project.
        :param project: The project data model.
        """
        # Delete file.
        FileFolderHelper.remove_file(project.share_slingshot_application_context_filepath)

        # File rewritten.
        # Creating the 'alfresco-config' node.
        root: Element = Element("beans")
        root.set("xmlns", "http://www.springframework.org/schema/beans")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xsi:schemaLocation", "http://www.springframework.org/schema/beans "
                                       "http://www.springframework.org/schema/beans/spring-beans-3.0.xsd")

        self._write(root, project.share_slingshot_application_context_filepath)

    def add_message_file_labels(self, project: ProjectModel, content_model: ContentModel):
        root: Element = self._get_root(project.share_slingshot_application_context_filepath)
        (is_created, value) = self.__get_create_message_value(content_model, root)
        if is_created:
            (is_created, list_node) = self.__get_create_message_list(root)
            list_node.append(value)

            if is_created:
                (is_created, property_node) = self.__get_create_message_property(root)
                property_node.append(list_node)

                if is_created:
                    (is_created, bean) = self.__get_create_message_bean(project, root)
                    bean.append(property_node)
                    if is_created:
                        root.append(bean)

        self._write(root, project.share_slingshot_application_context_filepath)

    def remove_message_file(self, project: ProjectModel, content_model: ContentModel):
        root: Element = self._get_root(project.share_slingshot_application_context_filepath)
        value: Element = self.__get_message_value(content_model, root)
        if value is None:
            return
        list_node: Element = self.__get_message_list(root)
        if list_node is None:
            return
        list_node.remove(value)

    def __get_create_message_bean(self, project: ProjectModel, root: Element) -> tuple[bool, Element]:
        namespace: str = self.get_namespace("xmlns")
        node: Element = root.find(".//{0}bean[@class='org.springframework.extensions.surf.util."
                                  "ResourceBundleBootstrapComponent']".format(namespace))
        if node is None:
            node = Element("bean")
            node.set("id", "{0}.{1}-share.resources".format(project.group_id, project.artifact_id))
            node.set("class", "org.springframework.extensions.surf.util.ResourceBundleBootstrapComponent")
            return True, node

        return False, node

    def __get_create_message_property(self, root: Element) -> tuple[bool, Element]:
        namespace: str = self.get_namespace("xmlns")
        node: Element = root.find(".//{0}bean[@class='org.springframework.extensions.surf.util."
                                  "ResourceBundleBootstrapComponent']/{0}property[@name='resourceBundles']"
                                  .format(namespace))
        if node is None:
            node = Element("property")
            node.set("name", "resourceBundles")
            return True, node

        return False, node

    def __get_create_message_list(self, root: Element) -> tuple[bool, Element]:
        node: Element = self.__get_message_list(root)
        return (True, Element("list")) if node is None else (False, node)

    def __get_create_message_value(self, content_model: ContentModel, root: Element) \
            -> tuple[bool, Element]:
        node: Element = self.__get_message_value(content_model, root)
        if node is not None:
            return False, node
        node = Element("value")
        node.text = self.__get_value(content_model)

        return True, node

    def __get_message_list(self, root: Element) -> Optional[Element]:
        namespace: str = self.get_namespace("xmlns")
        return root.find(".//{0}bean[@class='org.springframework.extensions.surf.util."
                         "ResourceBundleBootstrapComponent']/{0}property[@name='resourceBundles']/{0}list"
                         .format(namespace))

    def __get_message_value(self, content_model: ContentModel, root: Element) \
            -> Optional[Element]:
        namespace: str = self.get_namespace("xmlns")
        nodes: list[Element] = root.findall(".//{0}bean[@class='org.springframework.extensions.surf.util."
                                            "ResourceBundleBootstrapComponent']/{0}property[@name='resourceBundles']/"
                                            "{0}list/{0}value".format(namespace))

        index: int = 0
        maximum: int = len(nodes)
        value: str = self.__get_value(content_model)
        while index.__lt__(maximum) and value.__ne__(nodes[index].text):
            index += 1

        return None if index.__eq__(maximum) else nodes[index]

    @staticmethod
    def __get_value(content_model: ContentModel) -> str:
        filename: str = FileFolderHelper.extract_filename_from_path(content_model.share_message_file_path)
        return "alfresco.web-extension.messages.{0}".format(filename[:filename.rfind(".properties")])
