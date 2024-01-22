from get_last_target_folder_id import get_highest_integer_from_folders


def get_current_target_folder():
    return get_highest_integer_from_folders()+1
