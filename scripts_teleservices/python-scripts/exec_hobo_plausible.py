import json
import subprocess
import os

recipe_json_path = "/etc/hobo/recipe.json"
hobo_json_path = "./hobo_variable.json"
# Lire le fichier JSON recipe.json
try:
    with open(recipe_json_path, "r", encoding="utf-8") as file:
        recipe_data = json.load(file)
except FileNotFoundError:
    print(f"Le fichier {recipe_json_path} n'a pas été trouvé.")
    exit(1)
except json.JSONDecodeError:
    print(f"Erreur de décodage du fichier JSON {recipe_json_path}.")
    exit(1)


# Construction de la commande shell avec la valeur de "hobo" et execution avec subprocess
# Extraire la valeur de "hobo"
try:
    hobo_tenant = recipe_data["variables"]["hobo"]
except KeyError:
    print("La clé 'hobo' n'a pas été trouvée dans le fichier JSON.")
    exit(1)
try:
    subprocess.run(
        [
            "sudo",
            "-u",
            "hobo",
            "hobo-manage",
            "tenant_command",
            "runscript",
            "-d",
            hobo_tenant,
            "/opt/publik/scripts/scripts_teleservices/python-scripts/hobo_plausible_variable.py",
        ]
    )
except subprocess.CalledProcessError as e:
    print(f"Erreur lors de l'exécution de la commande shell : {e}")
    exit(1)
