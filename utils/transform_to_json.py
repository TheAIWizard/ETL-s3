import sys
import os
import csv
import json
import pyarrow as pa
import s3fs
from datetime import datetime


def save_to_s3(data, bucket: str, path: str, file_path: str):
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.getenv("S3_ENDPOINT_URL")},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    with fs.open(f'{bucket}/{path}{file_path}', 'w') as f:
        # Save the data as JSON
        json.dump(data, f, indent=2)

# next: create functions to split json and save it in annotation source in dated folders.


def split_and_save_to_s3(list_of_dicts, bucket: str, base_path: str, file_path: str):
    current_date = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Split tasks and save each to S3
    for i, dictionary in enumerate(list_of_dicts):
        output_file_name = f'task_{i}.json'
        object_key = f'{base_path}{current_date}-{file_path}/'

        print(f"S3 Object Key: {object_key}{output_file_name}")
        save_to_s3(dictionary, bucket, object_key, output_file_name)


def transform_to_json(input_file_path):
    _, input_extension = os.path.splitext(input_file_path)

    if input_extension.lower() == '.csv':
        # Convert CSV data to a list of dictionaries
        with open(input_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data_list = [row for row in csv_reader]
    elif input_extension.lower() == '.parquet':
        # Read Parquet file and convert to list of dictionaries
        table = pa.parquet.read_table(input_file_path)
        data_list = table.to_pandas().to_dict(orient='records')
    else:
        print(f"Unsupported input format: {input_extension}")

    return data_list


def main(bucket: str, path_json: str, path_source: str, input_file_path: str):
    data = transform_to_json(input_file_path)
    # save converted json to bucket
    save_to_s3(data, bucket, path_json, os.path.splitext(input_file_path)[0] + '.json')
    # split and save json to data source bucket for label studio annotation
    split_and_save_to_s3(data, bucket, path_source, os.path.splitext(input_file_path)[0])


if __name__ == "__main__":
    input_file_path = str(sys.argv[1])
    main(os.getenv("S3_BUCKET"), os.getenv("S3_BUCKET_PREFIX_TRANSFORM_JSON"), os.getenv("S3_BUCKET_PREFIX_ANNOTATION_SOURCE"), input_file_path)
