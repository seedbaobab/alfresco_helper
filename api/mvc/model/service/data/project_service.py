import subprocess
from abc import ABC

from api.mvc.model.data.project_model import ProjectModel
from api.mvc.model.service.file.bootstrap_service import BootstrapFileService
from api.mvc.model.service.file.service_context_service import ServiceContextFileService
from api.mvc.model.service.file.share_config_service import ShareConfigFileService
from api.mvc.model.service.file.share_slingshot_app_context import ShareSlingshotApplicationContext
from api.mvc.model.service.file.webscript_service import WebScriptFileService
from api_core.helper.file_folder_helper import FileFolderHelper
from api_core.mvc.service.model.service import Service


class ProjectService(Service, ABC):
    """
    Class providing services for managing project data models.
    """

    def __init__(self):
        super().__init__("project")
        self.__bfs: BootstrapFileService = BootstrapFileService()
        self.__wsfs: WebScriptFileService = WebScriptFileService()
        self.__scfs: ShareConfigFileService = ShareConfigFileService()
        self.__sctxtfs: ServiceContextFileService = ServiceContextFileService()
        self.__ssac: ShareSlingshotApplicationContext = ShareSlingshotApplicationContext()

    @staticmethod
    def new(sdk: str, group_id: str, artifact_id: str) -> tuple[int, str, str]:
        """
        Creates a new Alfresco All-In-One project.
        :param sdk: The value of the Alfresco All-in-One project SDK to create.
        :param group_id: The value of the Alfresco All-in-One project group id to create.
        :param artifact_id: The value of the Alfresco All-in-One project artifact id to create.
        :return: The execution status of the creation command.
        """
        # Create the maven project
        child_process: subprocess.Popen = subprocess.Popen(
            "mvn archetype:generate -D\"archetypeGroupId=org.alfresco.maven.archetype\" "
            "-D\"archetypeArtifactId=alfresco-allinone-archetype\" "
            "-D\"archetypeVersion={0}\" -D\"groupId={1}\" -D\"artifactId={2}\" "
            "-D\"interactiveMode=false\"".format(sdk, group_id, artifact_id), stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, shell=True)
        # Get the command result.
        (out, err) = child_process.communicate()
        return child_process.returncode, out, err

    def reset(self, project: ProjectModel):
        self.__bfs.reset(project)
        self.__scfs.reset(project)
        self.__wsfs.reset(project)
        self.__ssac.reset(project)
        self.__sctxtfs.reset(project)

        FileFolderHelper.remove_content(project.share_message_folder)

    def raz(self, project: ProjectModel):
        self.reset(project)

        FileFolderHelper.remove_folder(project.integration_tests_filepath)
        FileFolderHelper.remove_folder(project.platform_extension_folder)

        FileFolderHelper.remove_content(project.platform_unit_test_folder)

        FileFolderHelper.remove_content(project.share_site_data_extension)
        FileFolderHelper.remove_content(project.platform_java_folder)
        FileFolderHelper.remove_content(project.content_model_folder)
        FileFolderHelper.remove_content(project.workflow_process_folder)
        FileFolderHelper.remove_content(project.content_model_message_absolute_folder_path)

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()
        self.__load_manual()
        self.__raz_manual()
        self.__reset_manual()

    def __new_manual(self):
        """
        Add the new project command in manual.
        """
        self._ms.new_manual("new", "Creates a new Alfresco All-In-One project.")
        self._ms.add_call()
        self._ms.save()

    def __load_manual(self):
        """
        Add the load project command in manual.
        """
        self._ms.new_manual("load", "Load an Alfresco All-In-One project.")
        self._ms.add_call()
        self._ms.save()

    def __reset_manual(self):
        """
        Add the reset project command in manual.
        """
        self._ms.new_manual("reset", "Reset a Alfresco All-In-One project.")
        self._ms.add_call()
        self._ms.save()

    def __raz_manual(self):
        """
        Add the raz project command in manual.
        """
        self._ms.new_manual("raz", "Reset to zero a Alfresco All-In-One project.")
        self._ms.add_call()
        self._ms.save()
