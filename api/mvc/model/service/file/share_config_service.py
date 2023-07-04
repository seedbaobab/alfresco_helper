from typing import Optional
from xml.etree.ElementTree import Element, Comment

from api.mvc.model.data.aspect_model import AspectModel
from api.mvc.model.data.content_model import ContentModel
from api.mvc.model.data.data_model import DataModel
from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.data.property_model import PropertyModel
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.service.file.xml_file_service import XmlFileService


class ShareConfigFileService(XmlFileService):
    """

    """

    def __init__(self):
        """

        """
        super().__init__(False, None)

    def reset(self, project: ProjectModel):
        """
        Reset the 'share-config-custom.xml' file of the share project of the alfresco project.
        :param project: The project data model.
        """
        # Delete file.
        FileFolderHelper.remove_file(project.share_config_filepath)
        # File rewritten.
        # Creating the 'alfresco-config' node.
        root: Element = Element("alfresco-config")

        config_document_library: Element = Element("config")
        config_document_library.set("evaluator", "string-compare")
        config_document_library.set("condition", "DocumentLibrary")

        aspects: Element = Element("aspects")

        aspects_visible: Element = Element("visible")
        aspects_addable: Element = Element("addable")
        aspects_removeable: Element = Element("removeable")

        aspects.append(aspects_visible)
        aspects.append(aspects_addable)
        aspects.append(aspects_removeable)

        types: Element = Element("types")

        content_type: Element = Element("type")
        content_type.set("name", "cm:content")

        folder_type: Element = Element("type")
        folder_type.set("name", "cm:folder")

        types.append(content_type)
        types.append(folder_type)

        config_document_library.append(aspects)
        config_document_library.append(types)

        config_advanced_search: Element = Element("config")
        config_advanced_search.set("evaluator", "string-compare")
        config_advanced_search.set("condition", "AdvancedSearch")
        config_advanced_search.set("replace", "true")

        advanced_search: Element = Element("advanced-search")
        forms: Element = Element("forms")

        content_form: Element = Element("form")
        content_form.set("labelId", "search.form.label.cm_content")
        content_form.set("descriptionId", "search.form.desc.cm_content")
        content_form.text = "cm:content"

        folder_form: Element = Element("form")
        folder_form.set("labelId", "search.form.label.cm_folder")
        folder_form.set("descriptionId", "search.form.desc.cm_folder")
        folder_form.text = "cm:folder"

        forms.append(content_form)
        forms.append(folder_form)
        advanced_search.append(forms)
        config_advanced_search.append(advanced_search)

        root.append(config_document_library)
        root.append(config_advanced_search)

        self._write(root, project.share_config_filepath)

    def add_aspect_evaluator(self, project: ProjectModel, aspect: AspectModel):
        self.__add_data_evaluator(project, aspect)

    def add_parent_mandatory_data(self, project: ProjectModel, data: DataModel, data_linked: DataModel):
        root: Element = self._get_root(project.share_config_filepath)

        (in_creation, set_node) = self.__get_create_parent_mandatory_set(data, data_linked, root)
        if not in_creation:
            return

        (in_creation, appearance) = self.__get_create_appearance(data, root)
        appearance.append(set_node)

        if in_creation:
            (in_creation, form) = self.__get_create_form(data, root)
            form.append(appearance)

            if in_creation:
                (in_creation, forms) = self.__get_create_forms(data, root)
                forms.append(form)

                if in_creation:
                    (in_creation, config) = self.__get_create_data_evaluator(data, root)
                    config.append(forms)

                    if in_creation:
                        root.append(config)

        self._write(root, project.share_config_filepath)

    def add_aspect_set(self, project: ProjectModel, aspect: AspectModel):
        root: Element = self._get_root(project.share_config_filepath)

        (in_creation, set_node) = self.__get_create_set(aspect, root)
        if not in_creation:
            return

        (in_creation, appearance) = self.__get_create_appearance(aspect, root)
        appearance.append(set_node)

        if in_creation:
            (in_creation, form) = self.__get_create_form(aspect, root)
            form.append(appearance)

            if in_creation:
                (in_creation, forms) = self.__get_create_forms(aspect, root)
                forms.append(form)

                if in_creation:
                    (in_creation, config) = self.__get_create_data_evaluator(aspect, root)
                    config.append(forms)

                    if in_creation:
                        root.append(config)

        self._write(root, project.share_config_filepath)

    def add_aspect_document_library(self, project: ProjectModel, content_model: ContentModel, aspect: AspectModel):
        root: Element = self._get_root(project.share_config_filepath)
        (value_in_creation, value_node) = self.__get_create_aspect_document_library(aspect, root)

        if value_in_creation:
            (in_creation, visible) = self.__get_create_visible_document_library(root)
            visible.append(value_node)
            if in_creation:
                (in_creation, aspects) = self.__get_create_aspects_document_library(root)
                aspects.append(value_node)

                if in_creation:
                    (in_creation, config) = self.__get_create_config_document_library(root)
                    config.append(aspects)

                    if in_creation:
                        root.append(config)

        self._write(root, project.share_config_filepath)

    def add_property(self, project, data: DataModel, property_model: PropertyModel):
        root: Element = self._get_root(project.share_config_filepath)
        (show_in_creation, show) = self.__get_create_show_field(data, property_model, root)
        if show_in_creation:
            (in_creation, field_visibility) = self.__get_create_field_visibility(data, root)
            field_visibility.append(show)

            if in_creation:
                (in_creation, form) = self.__get_create_form(data, root)
                form.append(field_visibility)

                if in_creation:
                    (in_creation, forms) = self.__get_create_forms(data, root)
                    forms.append(form)

                    if in_creation:
                        (in_creation, config) = self.__get_create_data_evaluator(data, root)
                        config.append(forms)

                        if in_creation:
                            root.append(config)

        (field_in_creation, field) = self.__get_create_field(data, property_model, root)
        if field_in_creation:
            (in_creation, appearance) = self.__get_create_appearance(data, root)
            appearance.append(field)

            if in_creation:
                (in_creation, form) = self.__get_create_form(data, root)
                form.append(appearance)

                if in_creation:
                    (in_creation, forms) = self.__get_create_forms(data, root)
                    forms.append(form)

                    if in_creation:
                        (in_creation, config) = self.__get_create_data_evaluator(data, root)
                        config.append(forms)

                        if in_creation:
                            root.append(config)

        if show_in_creation or field_in_creation:
            self._write(root, project.share_config_filepath)

    @staticmethod
    def __get_create_field(data: DataModel, property_model: PropertyModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form/appearance/field[@id='{1}']"
                                  .format(data.complete_name, property_model.complete_name))
        if node is None:
            node = Element("field")
            node.set("id", property_model.complete_name)
            node.set("label-id", property_model.label_id)
            node.set("set", data.share_set_id)
            return True, node

        return False, node

    @staticmethod
    def __get_create_parent_mandatory_set(data: DataModel, data_set: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form/appearance/set[@id='{1}']"
                                  .format(data.complete_name, data_set.share_set_id))
        if node is None:
            node = Element("set")
            node.set("id", data_set.share_set_id)
            node.set("appearance", "bordered-panel")
            node.set("label-id", data_set.share_label_id)
            return True, node

        return False, node

    @staticmethod
    def __get_create_appearance(data: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form/appearance".format(data.complete_name))
        return (True, Element("appearance")) if node is None else (False, node)

    @staticmethod
    def __get_create_set(data: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form/appearance/set[@id='{1}']"
                                  .format(data.complete_name, data.share_set_id))
        if node is None:
            node = Element("set")
            node.set("id", data.share_set_id)
            node.set("appearance", "bordered-panel")
            node.set("label-id", data.share_label_id)
            return True, node

        return False, node

    @staticmethod
    def __get_create_forms(data: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms".format(data.complete_name))
        return (True, Element("forms")) if node is None else (False, node)

    @staticmethod
    def __get_create_form(data: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form".format(data.complete_name))
        return (True, Element("form")) if node is None else (False, node)

    @staticmethod
    def __get_create_field_visibility(data: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form/field-visibility"
                                  .format(data.complete_name))
        if node is None:
            node = Element("field-visibility")

            show_name: Element = Element("show")
            show_name.set("id", "cm:name")
            show_name.set("form-mode", "view")

            show_description: Element = Element("show")
            show_description.set("id", "cm:description")
            show_description.set("form-mode", "view")
            show_description.set("force", "true")

            show_created: Element = Element("show")
            show_created.set("id", "cm:created")
            show_created.set("form-mode", "view")

            show_creator: Element = Element("show")
            show_creator.set("id", "cm:creator")
            show_creator.set("form-mode", "view")

            show_modified: Element = Element("show")
            show_modified.set("id", "cm:modified")
            show_modified.set("form-mode", "view")

            show_modifier: Element = Element("show")
            show_modifier.set("id", "cm:modifier")
            show_modifier.set("form-mode", "view")

            node.append(show_name)
            node.append(show_description)
            node.append(show_created)
            node.append(show_creator)
            node.append(show_modified)
            node.append(show_modifier)
            return True, node

        return False, node

    @staticmethod
    def __get_create_show_field(data: DataModel, property_model: PropertyModel,
                                root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']/forms/form/field-visibility/"
                                  "show[@id='{1}']".format(data.complete_name, property_model.complete_name))
        if node is None:
            node = Element("show")
            node.set("id", "{0}".format(property_model.complete_name))
            return True, node

        return False, node

    def __add_data_evaluator(self, project: ProjectModel, data: DataModel):
        root: Element = self._get_root(project.share_config_filepath)
        (in_creation, field_visibility) = self.__get_create_field_visibility(data, root)

        if not in_creation:
            return

        (in_creation, form) = self.__get_create_form(data, root)
        form.append(field_visibility)
        if in_creation:
            (in_creation, forms) = self.__get_create_forms(data, root)
            forms.append(form)

            if in_creation:
                (in_creation, config) = self.__get_create_data_evaluator(data, root)
                config.append(forms)

                if in_creation:
                    root.append(config)

        self._write(root, project.share_config_filepath)

    @staticmethod
    def __get_create_data_evaluator(data: DataModel, root: Element) -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='{0}']".format(data.complete_name))
        if node is None:
            node = Element("config")

            if data.typology.__eq__("aspect"):
                node.set("evaluator", data.typology)
            elif data.typology.__eq__("type"):
                node.set("evaluator", "node-type")

            node.set("condition", "{0}".format(data.complete_name))
            return True, node

        return False, node

    @staticmethod
    def __get_create_config_document_library(root):
        node: Element = root.find(".//config[@condition='DocumentLibrary']")
        if node is None:
            node = Element("config")
            node.set("evaluator", "string-compare")
            node.set("condition", "DocumentLibrary")
            return True, node
        return False, node

    @staticmethod
    def __get_create_aspects_document_library(root):
        node: Element = root.find(".//config[@condition='DocumentLibrary']/aspects")
        return (True, Element("visible")) if node is None else (False, node)

    @staticmethod
    def __get_create_visible_document_library(root):
        node: Element = root.find(".//config[@condition='DocumentLibrary']/aspects/visible")
        return (True, Element("visible")) if node is None else (False, node)

    @staticmethod
    def __get_create_aspect_document_library(aspect: AspectModel, root: Element) \
            -> tuple[bool, Element]:
        node: Element = root.find(".//config[@condition='DocumentLibrary']/aspects/visible/aspect[@name='{0}']"
                                  .format(aspect.complete_name))
        if node is None:
            node = Element("aspect")
            node.set("name", "{0}".format(aspect.complete_name))
            return True, node

        return False, node




