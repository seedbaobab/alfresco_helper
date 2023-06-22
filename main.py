import sys

from api.alfresco_helper_api import AlfrescoHelperApi
from api_core.helper.file_folder_helper import FileFolderHelper

AlfrescoHelperApi(FileFolderHelper.extract_folder_from_filepath(__file__)).interpret(sys.argv[1:])
