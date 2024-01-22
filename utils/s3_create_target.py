import sys
import os
import json
import requests
from count_project_id import get_last_pk


def create_connection_api_s3(prefix):
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

    # Create new s3 storage for annotation source
    url_create_s3 = f"{service_endpoint}/api/storages/export/s3"
    payload_create_s3 = {
        "presign": True,
        "title": "Your Title test source",
        "description": "Your Description test source",
        "last_sync_count": 0,
        "bucket": bucket,
        "prefix": prefix,
        "can_delete_objects": True,
        "use_blob_urls": False,
        "aws_access_key_id": aws_access_key_id,
        "aws_secret_access_key": aws_secret_access_key,
        # "aws_session_token": aws_session_token,
        "region_name": "us-east-1",
        "s3_endpoint": s3_endpoint,
        # "presign_ttl": 0,
        "project": project
    }

    # Perform the POST request to create S3 storage connection
    response_create_s3 = requests.post(url_create_s3, data=json.dumps(payload_create_s3), headers=headers)
    id_s3 = str(response_create_s3.json()["id"])  # s3 storage connection id

    # Check the responses
    if response_create_s3.status_code == 201:
        print(id_s3)
    else:
        print(f"Error: {response_create_s3.status_code} - {response_create_s3.text}")


s3_target_path = str(sys.argv[1])
create_connection_api_s3(s3_target_path)
