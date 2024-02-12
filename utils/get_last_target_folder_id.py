import s3fs
import os


def list_folders_in_prefix(bucket_name, prefix):
    # Create an S3 filesystem
    s3 = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.getenv("S3_ENDPOINT")},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # List objects in the specified prefix
    objects = s3.ls(f'{bucket_name}{prefix}/in-progress')

    return objects


def get_highest_integer_from_folders():
    # Replace 'your-bucket-name' with the actual name of your S3 bucket
    bucket_name = os.getenv("S3_BUCKET")
    # Specify the prefix of the folder of the export storage
    prefix = os.getenv("S3_BUCKET_PREFIX_ANNOTATION_TARGET")

# Get the list of folders in the specified prefix of the bucket
    folder_list = list_folders_in_prefix(bucket_name, prefix)
    # Extract integers from folder names and find the maximum
    integers = [int(digit) for folder in folder_list for digit in folder if digit.isdigit()]
    highest_integer = max(integers, default=None)
    # Depending on the folders already present, give the most convinient integer
    return highest_integer if highest_integer is not None else integers


def get_folders_number_in_prefix():
    # Replace 'your-bucket-name' with the actual name of your S3 bucket
    bucket_name = os.getenv("S3_BUCKET")
    # Specify the prefix of the folder of the export storage
    prefix = os.getenv("S3_BUCKET_PREFIX_ANNOTATION_TARGET")

# Get the list of folders in the specified prefix of the bucket
    folder_list = list_folders_in_prefix(bucket_name, prefix)
    # Extract integers from folder names and find the maximum
    integers = [int(folder.split()[-1]) for folder in folder_list if folder.split()[-1].isdigit()]
    # Depending on the folders already present, give its number
    return len(integers)
