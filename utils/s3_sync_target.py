import sys
import os
import json
import requests
from count_project_id import get_last_pk
from get_last_target_folder_id import get_highest_integer_from_folders


def sync_api_s3(id_s3, prefix):
    # Replace with your actual AWS credentials stored in environment variables
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    # aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
    bucket = os.getenv("S3_BUCKET")
    # change to S3_ENDPOINT_URL if different python image
    s3_endpoint = os.environ.get("S3_ENDPOINT")
    service_endpoint = os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    project = str(get_last_pk()) # os.getenv("LABEL_STUDIO_PROJECT_ID")
    authorization_token = os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    # Sync s3 storage for annotation source
    payload_sync_s3 = {
        "title": f"Stockage sur S3 du {get_highest_integer_from_folders()}ème lot annoté",
        "description": "Synchronisation de la connexion de Label Studio au bucket S3 pour persister les données annotées",
        "can_delete_objects": True,
        "bucket": bucket,
        "prefix": prefix,
        "use_blob_urls": False,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        # "aws_session_token": aws_session_token,
        "region_name": "us-east-1",
        "s3_endpoint": s3_endpoint,
        "project": project
    }
    print(s3_endpoint)
    print("id: " + id_s3)
    # Replace with the actual values for {id} and other parameters
    url_sync_s3 = service_endpoint + "/api/storages/export/s3/" + id_s3 + "/sync"
    print(url_sync_s3)
    # Perform the POST request to sync S3 storage connection
    response_sync_s3 = requests.post(url_sync_s3, data=json.dumps(payload_sync_s3), headers=headers)

    # Check the responses
    if response_sync_s3.status_code == 201:
        print("Sync export storage successful!")
        print(response_sync_s3.json())
    else:
        print(f"Error: {response_sync_s3.status_code} - {response_sync_s3.text}")


id_s3 = str(sys.argv[1])
s3_target_path = str(sys.argv[2])
numero_lot = get_highest_integer_from_folders()
sync_api_s3(id_s3, s3_target_path)
