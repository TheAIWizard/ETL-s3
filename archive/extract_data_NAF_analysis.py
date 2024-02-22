import pandas as pd
import json
import os


def transform_json_to_dataframe(json_dir):

    transformed_data = []

    for filename in os.listdir(json_dir):
        with open(os.path.join(json_dir, filename), 'r') as file:
            data = json.load(file)

        # Retrieve JSON keys as columns
        task_id = data['task']['inner_id']
        created_at = data['task']['created_at']
        updated_at = data['task']['updated_at']
        # Get data variables
        liasse_numero = data['task']['data']['liasse_numero']
        evenement_type = data['task']['data']['evenement_type']
        liasse_type = data['task']['data']['liasse_type']
        activ_surf_et = data['task']['data']['liasse_numero']
        activ_nat_et = data['task']['data']['activ_nat_et']
        cj = data['task']['data']['cj']
        # Extract text description amongst three columns according to the order of preference.
        activ_pr_lib_et = data['task']['data'].get('activ_pr_lib_et')
        activ_ex_lib_et = data['task']['data'].get('activ_ex_lib_et')
        activ_pr_lib = data['task']['data'].get('activ_pr_lib')

        if activ_pr_lib_et:
            libelle = activ_pr_lib_et
        elif activ_ex_lib_et:
            libelle = activ_ex_lib_et
        else:
            libelle = activ_pr_lib

        # Number of skips
        skips = int(data['was_cancelled'])
        # Get annotated data without skips and adjust from UI's bugs
        if len(data['result']) > 0:
            apet_manual = ""
            commentary = ""
            # Retrieve comment
            if 'text' in data['result'][0]['value']:        
                commentary = data['result'][0]['value']['text'][0]
            # Retrieve taxonomy result
            if 'taxonomy' in data['result'][0]['value']:
                taxonomy_values = data['result'][0]['value']['taxonomy'][0][-1]
                apet_manual = taxonomy_values.replace('.', '') # delete . in apet_manual
            #Check if apet is in comment and fill empty apet (due to LS bug)
            if commentary[:4].isdigit() and commentary[4].isalpha():
                print(commentary)
                apet_manual = commentary

        # Créer un dictionnaire pour les données transformées
        transformed_row = {
            'task_id' : task_id,
            'libelle': libelle,
            'apet_manual': apet_manual,
            'commentary' : commentary,
            'skips' : skips,
            'created_at' : created_at,
            'updated_at' : updated_at
        }
        
        # Ajouter le dictionnaire à la liste des données transformées
        transformed_data.append(transformed_row)

    # Créer un DataFrame à partir des données transformées
    results = pd.DataFrame(transformed_data)
    
    return results

# Spécifier le répertoire contenant les fichiers JSON
json_directory = 'batch-2'

# Appeler la fonction pour obtenir le DataFrame transformé
transformed_df = transform_json_to_dataframe(json_directory)

# Afficher le DataFrame
#print(transformed_df.sort_values(by=['task_id']))
print(transformed_df[transformed_df['task_id']==68][['task_id',"apet_manual","commentary"]])


# Define custom aggregation functions
def sum_skips(series):
    return series.sum()


def most_frequent_apet(series):
    return series.mode().iloc[0] if not series.empty else None


def list_apet(series):
    return list(series)

#DON'T FORGET TO ALSO CONSIDER MULTIPLE SKIP AND NOT TAKE AN APET WHEN XXXX inclassable
# Group by 'task_id', aggregate with custom functions
bilan_df = transformed_df.groupby('task_id').agg({'skips': sum_skips, 'apet_manual': [most_frequent_apet,list_apet]}).reset_index()

# Flatten multi-level column index
bilan_df.columns = ['task_id', 'sum_skips', 'most_frequent_apet', 'list_apet']

#print(bilan_df.iloc[1])
#print(len(os.listdir('Lot2.json')))

print(transformed_df[(transformed_df['skips']==0)&(transformed_df['apet_manual']=="")][['task_id',"commentary"]])
print(transformed_df[(transformed_df['skips']==0)&(transformed_df['apet_manual']=="")][['task_id',"apet_manual"]])

# When submit doesn't work replace apet by text
# reprendre ceux qui sont marqués pas d'activité et les remettre à annoter un peu plus tard
print(transformed_df[(transformed_df['skips']==0)&(transformed_df['commentary']=="pas d'activité")][['task_id',"commentary"]])