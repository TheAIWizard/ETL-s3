import sys
import json

input_json = sys.argv[1]
with open(input_json) as inp:
    tasks = json.load(inp)

for i, v in enumerate(tasks):
    with open(f'split_{input_json}/task_{i}.json', 'w') as f:
        json.dump(v, f)

# python3 split_json_tasks.py data_gu_check_API.json
