import csv
import json

# mc cp --recursive "s3/nrandriamanana/Annotation source/data_gu_check_API.csv" .


def csv_to_json(csv_file_path, json_file_path):
    # Open the CSV file and read its contents
    with open(csv_file_path, 'r') as csv_file:
        # Assuming the first row of the CSV file contains headers
        csv_reader = csv.DictReader(csv_file)

        # Convert CSV data to a list of dictionaries
        data_list = [row for row in csv_reader]

    # Write JSON data to the specified JSON file
    with open(json_file_path, 'w') as json_file:
        # Use json.dump() to write the data to the JSON file
        json.dump(data_list, json_file, indent=2)

# Example usage:


csv_file_path = 'ETL-s3/data_gu_check_API.csv'  # Replace with your CSV file path
json_file_path = 'ETL-s3/data_gu_check_API.json'  # Replace with your desired JSON file path

# mc cp --recursive ETL-s3/data_gu_check_API.json "s3/nrandriamanana/Annotation source/"

csv_to_json(csv_file_path, json_file_path)
