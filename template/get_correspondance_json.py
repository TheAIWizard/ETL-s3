import pandas as pd
import json

# Load CSV file into a pandas DataFrame
df = pd.read_csv('./template/table_correspondance_cj_libelle.csv', encoding='ISO-8859-1')

# Convert DataFrame to a dictionary with 'code' as keys and 'libelle' as values
data = df.set_index('code')['libelle'].to_dict()

# Write data to JSON file
with open('./template/correspondance_intitule_cj.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, ensure_ascii=False, indent=4)
