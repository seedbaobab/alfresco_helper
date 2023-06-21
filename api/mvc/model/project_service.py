import subprocess
from abc import ABC

from api_core.mvc.service.model.service import Service


class ProjectService(Service, ABC):
    """
    Class providing services for managing project data models.
    """

    def __init__(self):
        super().__init__("project")

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

    def init_manual(self):
        """
        Initializes the service manual.
        """
        self.__new_manual()

    def __new_manual(self):
        """
        Add the new project command in manual.
        """
        self._ms.new_manual("new", "Creates a new Alfresco All-In-One project.")
        self._ms.add_call()
        self._ms.save()
