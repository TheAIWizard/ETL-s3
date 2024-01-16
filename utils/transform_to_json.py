import sys
import os
import csv
import json
import pyarrow.parquet as pq
import s3fs
import pytz
from datetime import datetime
from s3_sync_source import sync_api_s3


def sync_storage_s3(prefix: str):
    sync_api_s3(prefix)


def split_and_save_to_s3(list_of_dicts, bucket: str, base_path: str, file_path: str):
    # Définir le fuseau horaire local actuel
    local_timezone = pytz.timezone('Europe/Paris')
    # split json and save it in annotation source in dated folders.
    current_date = datetime.now(local_timezone).strftime('%Y-%m-%d_%H-%M-%S')

    # Split tasks and save each to S3
    for i, dictionary in enumerate(list_of_dicts):
        output_file_name = f'task_{i+1}.json'
        object_key = f'{base_path}{current_date}-{file_path}/'

        print(f"S3 Object Key: {object_key}{output_file_name}")
        save_to_s3(dictionary, bucket, object_key, output_file_name)
    # Once tasks loaded, sync s3 storage on label studio
    sync_storage_s3(object_key)


def save_to_s3(data, bucket: str, path: str, file_path: str):
    # Définir le fuseau horaire local actuel
    local_timezone = pytz.timezone('Europe/Paris')
    # save it in batch data json in dated folders.
    current_date = datetime.now(local_timezone).strftime('%Y-%m-%d_%H-%M-%S')

    fs = s3fs.S3FileSystem(
        client_kwargs={"endpoint_url": os.getenv("S3_ENDPOINT_URL")},
        key=os.getenv("AWS_ACCESS_KEY_ID"),
        secret=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    with fs.open(f'{bucket}/{path}{current_date}-{file_path}', 'w') as f:
        # Save the data as JSON
        json.dump(data, f, indent=2)


def format_data(data_df):
    with open('correspondance_intitule_nature_activite.json', 'r') as file:
        correspondance_tableau = json.load(file)
    # Convert Timestamp objects to strings
    data_df['date_modification'] = data_df['date_modification'].astype(str)
    # Map activ_nat_et with its heading
    data_df['activ_nat_et_intitule'] = data_df['activ_nat_et'].map(correspondance_tableau)
    # Replace NaN values with empty strings
    data_df = data_df.fillna("")
    print(data_df)
    return data_df


def transform_to_json(input_file_path):
    _, input_extension = os.path.splitext(input_file_path)

    if input_extension.lower() == '.csv':
        # Convert CSV data to a list of dictionaries
        with open(input_file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            data_list = [row for row in csv_reader]
    elif input_extension.lower() == '.parquet':
        # Read Parquet file and convert to list of dictionaries
        table = pq.read_table(input_file_path)
        data_df = table.to_pandas()
        # Format dataframe
        format_data(data_df)
        # Convert DataFrame to a list of dictionaries
        data_list = data_df.to_dict(orient='records')
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
