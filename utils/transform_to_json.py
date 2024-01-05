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
    with fs.open(f'{bucket}/{path}', 'wb') as f:
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


if __name__ == "__main__":
    input_file_path = 'ETL-s3/data_gu_check_API.csv'  # Replace with your input file path

    data_list = transform_to_json(input_file_path)
    save_to_s3(data_list, os.getenv("S3_BUCKET"), os.path.basename(input_file_path) + '.json')
