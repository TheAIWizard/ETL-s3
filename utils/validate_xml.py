import os
import requests
import json


with open("taxonomy.xml", 'r', encoding='utf-8') as file:
    xml_template = file.read()


def validate_xml(xml_template):
    service_endpoint = os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    authorization_token = os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    payload_validate_xml = {
        "label_config": xml_template,
        }

    # Create new s3 storage for annotation source
    url_validate_xml = f"{service_endpoint}/api/projects/validate"

    # Perform the POST request to create S3 storage connection
    response_validate_xml = requests.post(url_validate_xml, data=json.dumps(payload_validate_xml), headers=headers)
    # Check the responses
    if response_validate_xml.status_code == 204:
        print("Validation success")
    else:
        pass
        print(f"Error: {response_validate_xml.status_code}-{response_validate_xml.text}")


validate_xml(xml_template)
