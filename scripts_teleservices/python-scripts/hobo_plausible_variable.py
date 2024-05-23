import json
from hobo.environment.models import Variable

# Chemin des fichiers JSON
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

# Extraire la valeur de "combo"
try:
    combo_value = recipe_data["variables"]["combo"]
except KeyError:
    print("La clé 'combo' n'a pas été trouvée dans le fichier JSON.")
    exit(1)


# Lire le fichier JSON hobo_variable.json
def load_json_config():
    try:
        with open(hobo_json_path, "r", encoding="utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        print(f"Le fichier {hobo_json_path} n'a pas été trouvé.")
        exit(1)
    except json.JSONDecodeError:
        print(f"Erreur de décodage du fichier JSON {hobo_json_path}.")
        exit(1)


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
        print(f"Variable '{variable}' has been created.")
    else:
        print(f"Variable '{variable}' has been updated.")


# Créer ou mettre à jour les variables avec les nouvelles valeurs
for name, value in hobo_variables.items():
    create_or_update_variable(name, value["label"], value["value"])
    print(f"Variable '{name}' has been created or updated.")
    print(f"Label: '{value['label']}'")
    print(f"Value: '{value['value']}'")
    print("\n")
