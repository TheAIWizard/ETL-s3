import sys
import os
import csv
import json
import pyarrow as pa
import s3fs


def save_to_s3(data, bucket: str, prefix: str, path: str):
    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.getenv("S3_ENDPOINT_URL")},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    with fs.open(f'{bucket}/{prefix}/{path}', 'wb') as f:
        # Save the data as JSON
        json.dump(data, f, indent=2)


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
        raise ValueError(f"Unsupported input format: {input_extension}")

    return data_list


def main(bucket: str, prefix: str, input_file_path: str):
    data_list = transform_to_json(input_file_path)
    save_to_s3(data_list, bucket, prefix + input_file_path + '.json')


if __name__ == "__main__":
    input_file_path = str(sys.argv[1])

    data_list = transform_to_json(input_file_path)
    main(os.getenv("S3_BUCKET"), os.getenv("S3_BUCKET_PREFIX"), input_file_path)