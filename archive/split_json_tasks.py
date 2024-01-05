import sys
import os
import json

input_json = sys.argv[1]
# Extract the directory path from the input JSON file
directory_path = os.path.dirname(input_json)

# Create a folder named "split_" in the same location
output_folder = os.path.join(directory_path, f'split_{os.path.splitext(os.path.basename(input_json))[0]}')
os.makedirs(output_folder, exist_ok=True)

with open(input_json) as inp:
    tasks = json.load(inp)

for i, v in enumerate(tasks):
    output_path = os.path.join(output_folder, f'task_{i}.json')
    with open(output_path, 'w') as f:
        json.dump(v, f)

# python3 split_json_tasks.py data_gu_check_API.json
# mc cp --recursive ETL-s3/split_data_gu_check_API/ "s3/nrandriamanana/Annotation source/split_data_gu_check_API/"
