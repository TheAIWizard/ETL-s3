import sys
import os
import json
import requests


def create_connection_api_s3(prefix):
    # Replace with your actual AWS credentials stored in environment variables
    aws_access_key_id = ""
    aws_secret_access_key = ""
    # aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
    bucket = "projet-ape"
    s3_endpoint = os.environ.get("S3_ENDPOINT")
    service_endpoint = "https://projet-ape-102830.user.lab.sspcloud.fr"
    project = "1"
    authorization_token = ""
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    # Sync s3 storage for annotation source
    payload_sync_s3 = {
        "synchronizable": True,
        "title": "Your Title test",
        "description": "Your Description test",
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

    id_s3 = "84"
    print("id: " + id_s3)
    # Replace with the actual values for {id} and other parameters
    url_sync_s3 = service_endpoint + "/api/storages/export/s3/" + id_s3 + "/sync"
    # Perform the POST request to sync S3 storage connection
    response_sync_s3 = requests.post(url_sync_s3, data=json.dumps(payload_sync_s3), headers=headers)

    # Check the responses
    if response_sync_s3.status_code == 201:
        print("Sync export storage successful!")
        print(response_sync_s3.json())
    else:
        print(f"Error: {response_sync_s3.status_code} - {response_sync_s3.text}")


s3_target_path = "Label Studio/Annotation APE 2024/NAF 2008/Annotation target/Lot 2"
create_connection_api_s3(s3_target_path)
