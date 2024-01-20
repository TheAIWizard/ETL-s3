import os
import json
import requests
from datetime import datetime


# Dictionnaire de correspondance des mois anglais vers français
MONTH_TRANSLATION = {
    "January": "janvier",
    "February": "février",
    "March": "mars",
    "April": "avril",
    "May": "mai",
    "June": "juin",
    "July": "juillet",
    "August": "août",
    "September": "septembre",
    "October": "octobre",
    "November": "novembre",
    "December": "décembre"
}


def get_week_info_french(date=None):
    if date is None:
        date = datetime.now()

    # Format the date without the hour
    formatted_date = date.strftime("%A %d/%B %Y")

    iso_year, iso_week_number, iso_weekday = date.isocalendar()
    
    # Utiliser le dictionnaire pour traduire le nom du mois
    month_name = MONTH_TRANSLATION[date.strftime("%B")]

    suffix = 'ème' if 10 <= iso_week_number % 100 <= 20 else {1: 'er'}.get(iso_week_number % 10, 'ème')

    week_info = f"{iso_week_number}{suffix} semaine de {month_name} {iso_year}"

    return f"{week_info}: {formatted_date}"


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
    count = response_get.json()["count"] # s3 storage connection id
    # Check the responses
    if response_get.status_code == 200:
        print(count)
    else:
        print(f"Error: {response_get.status_code}")
    return count

# store previous count
previous_count = count_projects()

with open("instructions.txt", 'r', encoding='utf-8') as file:
    instructions = file.read()

with open("taxonomy.xml", 'r', encoding='utf-8') as file:
    xml_template = file.read()


def create_project():
    service_endpoint = os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    authorization_token = os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    current_date = datetime.now()
    date_actuelle = get_week_info_french(current_date)
    payload_create_project = {
        "title": f"Lot {count_projects()+2}",
        "description": "Opération qualité FastText (NAF 2008) - Campagne d'annotation des libellés d'activités: "+ date_actuelle,
        "label_config": xml_template,
        "expert_instruction": instructions,
        "show_instruction": True,
        "show_skip_button": True,
        "enable_empty_annotation": False, # désactiver annotation vide
        "show_annotation_history": True,
        "organization": 1,
        "color": "green",
        "maximum_annotations": 1,
        "is_published": 1,
        # "model_version": "string",
        # "is_draft": true,
        "sampling": "Sequential sampling", # choix de l'échantillonage
        # "show_overlap_first": true,
        # "overlap_cohort_percentage": 0,
        # "control_weights": {},
        "skip_queue": "REQUEUE_FOR_OTHERS",
        }

    # Create new s3 storage for annotation source
    url_get_project = f"{service_endpoint}/api/projects/"

    # Perform the POST request to create S3 storage connection
    response_create_project = requests.post(url_get_project, data=json.dumps(payload_create_project), headers=headers)
    project_id = str(response_create_project.json()["id"])  # s3 storage connection id
    # update LABEL_STUDIO_PROJECT_ID value
    os.environ['LABEL_STUDIO_PROJECT_ID'] = project_id
    # Check the responses
    if response_create_project.status_code == 201:
        print(project_id)
    else:
        print(f"Error: {response_create_project.status_code}-{response_create_project.text}")


def update_project():
    service_endpoint = os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    authorization_token = os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }

    # project_id = os.environ.get('PROJECT_ID')
    # print(project_id)
    print(count_projects())
    payload_update_project = {
        # "title": "Lot "+date_actuelle,
        "title": f"Lot {count_projects()+1}",
        "label_config": xml_template,
        "expert_instruction": instructions,
        "show_instruction": True,
        "show_skip_button": True,
        "enable_empty_annotation": False, # désactiver annotation vide
        "show_annotation_history": False,
        "organization": 1,
        "color": "red",
        "maximum_annotations": 1,
        "is_published": 1,
        # "model_version": "string",
        # "is_draft": true,
        "sampling": "Sequential sampling", # choix de l'échantillonage
        # "show_overlap_first": true,
        # "overlap_cohort_percentage": 0,
        # "control_weights": {},
        "skip_queue": "REQUEUE_FOR_OTHERS",
        }

    # Create new s3 storage for annotation source
    url_get_project = f"{service_endpoint}/api/projects/{str(count_projects())}/"

    # Perform the POST request to create S3 storage connection
    response_update_project = requests.patch(url_get_project, data=json.dumps(payload_update_project), headers=headers)
    # project_id = str(response_update_project.json()["id"])  # s3 storage connection id
    # Check the responses
    if response_update_project.status_code == 201:
        print("Project done. Next now !")
    else:
        print(f"Error: {response_update_project.status_code}-{response_update_project.text}")


if previous_count <= 0:
    # create first project
    create_project()
# archive current project and create new project 
update_project()
create_project()
