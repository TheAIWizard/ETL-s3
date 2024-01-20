import os
import requests


def count_projects():
    service_endpoint = os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    authorization_token = os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    # Create new s3 storage for annotation source
    url_get_project = f"{service_endpoint}/api/projects"

    # Perform the POST request to create S3 storage connection
    response_get = requests.get(url_get_project, headers=headers)
    # Check the responses
    if response_get.status_code == 200:
        count = response_get.json()["count"] # s3 storage connection id
    else:
        print(f"Error: {response_get.status_code}")
        count = 0
    return count