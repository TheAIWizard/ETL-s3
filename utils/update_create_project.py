import os
import json
import requests
from datetime import datetime
from count_project_id import count_projects, get_last_pk
from get_last_target_folder_id import get_highest_integer_from_folders


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
    # formatted_date = date.strftime("%A %d/%B %Y")

    iso_year, iso_week_number, iso_weekday = date.isocalendar()
    # Utiliser le dictionnaire pour traduire le nom du mois
    month_name = MONTH_TRANSLATION[date.strftime("%B")]

    suffix = 'ème' if 10 <= iso_week_number % 100 <= 20 else {1: 'er'}.get(iso_week_number % 10, 'ème')

    week_info = f"{iso_week_number//4}{suffix} semaine de {month_name} {iso_year}"

    return f"{week_info}"


# store previous count
previous_count = count_projects()

with open("instructions.txt", 'r', encoding='utf-8') as file:
    instructions = file.read()

with open("taxonomy_NAF2025.xml", 'r', encoding='utf-8') as file:
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
    # get the id of the last s3 folder created as export storage for annotated data
    # bucket, prefix = os.getenv("S3_BUCKET"), os.getenv("S3_BUCKET_PREFIX_ANNOTATION_TARGET")
    delta = get_highest_integer_from_folders()
    payload_create_project = {
        "title": f"Lot {delta+1}",
        "description": "Série en cours d'annotation - Opération entraînement modèle (révision NAF 2025) - Campagne d'annotation des libellés d'activités: "+ date_actuelle,
        "label_config": xml_template,
        "expert_instruction": instructions,
        "show_instruction": True,
        "show_skip_button": True,
        "enable_empty_annotation": False, # désactiver annotation vide
        "show_annotation_history": False,
        "organization": 1,
        "color": "green",
        "maximum_annotations": 3,
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
    project_id = response_create_project.json()["id"]  # s3 storage connection id
    # update LABEL_STUDIO_PROJECT_ID value
    os.environ['LABEL_STUDIO_PROJECT_ID'] = str(project_id)
    # Check the responses
    if response_create_project.status_code == 201:
        pass
        # print(str(project_id))
    else:
        pass
        # print(f"Error: {response_create_project.status_code}-{response_create_project.text}")
    return project_id


def update_project():
    service_endpoint = os.getenv("LABEL_STUDIO_SERVICE_ENDPOINT")
    authorization_token = os.getenv("LABEL_STUDIO_TOKEN")
    # headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {authorization_token}"
    }
    # get the id of the last s3 folder created as export storage for annotated data
    # bucket, prefix = os.getenv("S3_BUCKET"), os.getenv("S3_BUCKET_PREFIX_ANNOTATION_TARGET")
    delta = get_highest_integer_from_folders()
    payload_update_project = {
        # "title": "Lot "+date_actuelle,
        "title": f"Lot {delta}",
        "description": "Série terminée - Opération qualité FastText (NAF 2008) - Campagne d'annotation des libellés d'activités: ",
        "label_config": xml_template,
        "expert_instruction": instructions,
        "show_instruction": True,
        "show_skip_button": True,
        "enable_empty_annotation": False, # désactiver annotation vide
        "show_annotation_history": False,
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
    url_get_project = f"{service_endpoint}/api/projects/{str(get_last_pk())}/"

    # Perform the POST request to create S3 storage connection
    response_update_project = requests.patch(url_get_project, data=json.dumps(payload_update_project), headers=headers)
    # project_id = str(response_update_project.json()["id"])  # s3 storage connection id
    # Check the responses
    if response_update_project.status_code == 201:
        pass
        # print("Project done. Next now !")
    else:
        pass
        # print(f"Error: {response_update_project.status_code}-{response_update_project.text}")


if previous_count <= 0:
    # create first project
    create_project()
else:
    # archive current project and create new project
    update_project()
    # store current id of newly created project
    create_project()
