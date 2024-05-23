import json
import subprocess
import os
from hobo.environment.models import Variable

# Chemin des fichiers JSON
error_message = ""
recipe_json_path = "/etc/hobo/recipe.json"
hobo_json_path = "/opt/publik/scripts/scripts_teleservices/python-scripts/hobo_variable.json"


# Lire le fichier JSON hobo_variable.json
def load_json_config():
    global error_message
    try:
        with open(hobo_json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        error_message += f"Le fichier {hobo_json_path} n'a pas été trouvé."
    except json.JSONDecodeError:
        print(f"Erreur de décodage du fichier JSON {hobo_json_path}.")


# Lire le fichier JSON recipe.json
try:
    with open(recipe_json_path, "r", encoding="utf-8") as file:
        recipe_data = json.load(file)
except FileNotFoundError:
    error_message += f"Le fichier {recipe_json_path} n'a pas été trouvé."
except json.JSONDecodeError:
    error_message += f"Erreur de décodage du fichier JSON {recipe_json_path}."
# Extraire la valeur de "combo"
try:
    combo_value = recipe_data["variables"]["combo"]
except KeyError:
    error_message += "La clé 'combo' n'a pas été trouvée dans le fichier JSON."
hobo_variables = load_json_config()

# Remplacer {{ commune_slug }} par combo_value dans les variables hobo
for name, value in hobo_variables.items():
    if "{{ commune_slug }}" in value["value"]:
        value["value"] = value["value"].replace("{{ commune_slug }}", combo_value)


# Fonction pour créer ou mettre à jour une variable
def create_or_update_variable(name, label, value):
    """
    Create or update a variable.

    Usage :

        create_or_update_variable("plausible_domain", "Activer Plausible sur cette instance ?", "url_stat")
    """
    variable, created = Variable.objects.update_or_create(name=name, defaults={"label": label, "value": value})
    if created:
        print(f"Variable '{variable}' has been created on {combo_value}, {error_message}")
    else:
        print(f"Variable '{variable}' has been updated on {combo_value}, {error_message}")


# Créer ou mettre à jour les variables avec les nouvelles valeurs
for name, value in hobo_variables.items():
    create_or_update_variable(name, value["label"], value["value"])
