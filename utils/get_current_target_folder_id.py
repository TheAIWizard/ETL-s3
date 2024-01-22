from get_last_target_folder_id import get_highest_integer_from_folders


def get_current_target_folder():
    print(get_highest_integer_from_folders())
    print(get_highest_integer_from_folders()+1)
    print(get_highest_integer_from_folders()+1)
    return get_highest_integer_from_folders()+1
