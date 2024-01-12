import os
import json
import requests

# Replace with your actual AWS credentials stored in environment variables
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
aws_session_token = os.environ.get("AWS_SESSION_TOKEN")
s3_endpoint = os.environ.get("S3_ENDPOINT")
authorization_token = "your token"

service_endpoint = "http://user-nrandriamanana-933743.user.lab.sspcloud.fr"
bucket = "nrandriamanana"
prefix = "Label Studio/Annotation APE 2024/Annotation source/Test/"


# headers
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Token {authorization_token}"
}


# Create new s3 storage for annotation source
url_create_s3 = f"{service_endpoint}/api/storages/s3"
payload_create_s3 = {
    "presign": True,
    "title": "Your Title test source",
    "description": "Your Description test source",
    "last_sync_count": 0,
    "bucket": bucket,
    "prefix": prefix,
    "use_blob_urls": False,
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key,
    # "aws_session_token": aws_session_token,
    "region_name": "us-east-1",
    "s3_endpoint": s3_endpoint,
    # "presign_ttl": 0,
    "recursive_scan": True,
    "project": 1
}


# Replace with the actual values for {id} and other parameters
url_sync_s3 = service_endpoint + "/api/storages/s3/{id}/sync"
print(url_sync_s3)

payload_sync_s3 = {
    "presign": True,
    "title": "Your Title test",
    "description": "Your Description test",
    "last_sync_count": 0,
    "can_delete_objects": True,
    "bucket": bucket,
    "prefix": prefix,
    "use_blob_urls": False,
    "aws_access_key_id": aws_access_key_id,
    "aws_secret_access_key": aws_secret_access_key,
    # "aws_session_token": aws_session_token,
    "region_name": "us-east-1",
    "s3_endpoint": s3_endpoint,
    "recursive_scan": True,
    "project": 1
}

# Perform the POST request to create S3 storage connection
response_create_s3 = requests.post(url_create_s3, data=json.dumps(payload_create_s3), headers=headers)
print(response_create_s3.json()["id"])
print(str(response_create_s3.json()["id"]))
id_s3 = str(response_create_s3.json()["id"])  # s3 storage connection id
# Perform the POST request to sync S3 storage connection
response_sync_s3 = requests.post(url_sync_s3.format(id=id_s3), data=json.dumps(payload_sync_s3), headers=headers)

# Check the responses
if response_create_s3.status_code == 200:
    print("Create export storage successful!")
    print(response_create_s3.json())
else:
    print(f"Error: {response_create_s3.status_code} - {response_create_s3.text}")

if response_sync_s3.status_code == 200:
    print("Sync export storage successful!")
    print(response_sync_s3.json())
else:
    print(f"Error: {response_sync_s3.status_code} - {response_sync_s3.text}")
