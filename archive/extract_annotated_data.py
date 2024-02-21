import pandas as pd
import json
import os

def transform_json_to_dataframe(json_dir):
    # Créer une liste pour stocker les données transformées
    transformed_data = []

    # Parcourir les fichiers JSON dans le répertoire
    for filename in os.listdir(json_dir):
        # Lire le fichier JSON
        with open(os.path.join(json_dir, filename), 'r') as file:
            data = json.load(file)
        
        # Extraire la valeur de la colonne résultante selon l'ordre de préférence
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
        print(skips)

        # Check if there are results (no skip)
        if len(data['result']) > 0:
            # Retrieve comment
            if 'text' in data['result'][0]['value']:        
                commentary = data['result'][0]['value']['text'][0]
            else:
                commentary = ""
            # Retrieve taxonomy result
            if 'taxonomy' in data['result'][0]['value']:
                taxonomy_values = data['result'][0]['value']['taxonomy'][0][-1]
                apet_manual = taxonomy_values.replace('.', '') # delete . in apet_manual
            else:
                apet_manual = ""
            print(apet_manual)
        # Créer un dictionnaire pour les données transformées
        transformed_row = {
            'libelle': libelle,
            'apet_manual': apet_manual,
            'commentary' : commentary,
            'skips' : skips
        }
        
        # Ajouter le dictionnaire à la liste des données transformées
        transformed_data.append(transformed_row)

    # Créer un DataFrame à partir des données transformées
    df = pd.DataFrame(transformed_data)
    
    return df

# Spécifier le répertoire contenant les fichiers JSON
json_directory = 'batch-2'

# Appeler la fonction pour obtenir le DataFrame transformé
transformed_df = transform_json_to_dataframe(json_directory)

# Afficher le DataFrame
print(transformed_df[transformed_df["commentary"]!=""])
