import sys
import os
import csv
import json
import pyarrow as pa
import s3fs


def save_to_s3(data, bucket: str, path: str):
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.getenv("S3_ENDPOINT_URL")},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    if isinstance(data, list):
        # Data is a list of files
        for idx, file_data in enumerate(data):
            file_path = f'{path}/file_{idx + 1}.json'  # You can adjust the file naming logic as needed
            with fs.open(f'{bucket}/{file_path}', 'wb') as f:
                json.dump(file_data, f, indent=2)
    else:
        # Data is a single file
        with fs.open(f'{bucket}/{path}', 'wb') as f:
            json.dump(data, f, indent=2)

# next: create functions to split json and save it in annotation source in dated nested folders.


def transform_to_json(input_file_path):
    # Check if the provided path is a directory
    if os.path.isdir(input_file_path):
        # Initialize an empty list to store the data from each CSV file
        data_list_per_file = []

        # Iterate over files in the directory
        for filename in os.listdir(input_file_path):
            file_path = os.path.join(input_file_path, filename)

            # Check if the file is a CSV file
            if os.path.isfile(file_path) and filename.lower().endswith('.csv'):
                # Convert CSV data to a list of dictionaries
                with open(file_path, 'r') as csv_file:
                    csv_reader = csv.DictReader(csv_file)
                    data_list_per_file.append([row for row in csv_reader])
    else:
        _, input_extension = os.path.splitext(input_file_path)

        if input_extension.lower() == '.csv':
            # Convert CSV data to a list of dictionaries
            with open(input_file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                data_list_per_file = [[row for row in csv_reader]]
        elif input_extension.lower() == '.parquet':
            # Read Parquet file and convert to a list of dictionaries
            table = pa.parquet.read_table(input_file_path)
            data_list_per_file = [table.to_pandas().to_dict(orient='records')]
        else:
            print(f"Unsupported input format: {input_extension}")
            return None

    return data_list_per_file


def main(bucket: str, path: str, input_file_path: str):
    data = transform_to_json(input_file_path)
    save_to_s3(data, bucket, path + '.json')


if __name__ == "__main__":
    input_file_path = str(sys.argv[1])

    main(os.getenv("S3_BUCKET"), os.getenv("S3_BUCKET_PREFIX"), input_file_path)
