from get_last_target_folder_id import get_highest_integer_from_folders, get_folders_number_in_prefix
from count_project_id import get_last_pk

if get_folders_number_in_prefix()-count_projects() > 1:
    print("Missing projects")
if get_folders_number_in_prefix()-count_projects() == 1:
    print(get_highest_integer_from_folders()+1)
if get_folders_number_in_prefix()-count_projects() == 0:
    print(get_highest_integer_from_folders())
if get_folders_number_in_prefix()-count_projects() < 0:
    print("Missing export storage files")
