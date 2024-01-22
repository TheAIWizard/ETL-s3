import os
import json
import requests


def get_last_target_s3_storage_id():
    current_label_studio_id = 4 # os.getenv("LABEL_STUDIO_PROJECT_ID")
    service_endpoint = "" #os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    authorization_token = ""  # os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    # Create new s3 storage for annotation source
    url_get_project = f"{service_endpoint}/api/storages/export/s3"

    # Payload
    payload_get_target_project = {
        "project": "7" # current_label_studio_id
    }

    # Perform the POST request to create S3 storage connection
    response_get = requests.get(url_get_project, data=json.dumps(payload_get_target_project), headers=headers)
    # Check the responses
    if response_get.status_code == 200:
        # response_json_data = response_get.json()
        # last label studio project id created
        #last_project_id = response_json_data['results'][0]['id'] if response_json_data['results'] else print("No existing project")
        #return last_project_id
        print(response_get.json())
    else:
        print(f"Error: {response_get.status_code}")
    print(response_get.json())

get_last_target_s3_storage_id()