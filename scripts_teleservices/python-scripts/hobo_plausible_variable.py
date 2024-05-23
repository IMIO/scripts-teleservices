import json

from hobo.environment.models import Variable  # type: ignore


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


def load_json_config():
    try:
        with open("./hobo_variable.json") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


hobo_variables = load_json_config()

for name, value in hobo_variables.items():
    create_or_update_variable(name, value["label"], value["value"])
    print(f"Variable '{name}' has been created or updated.")
    print(f"Label: '{value['label']}'")
    print(f"Value: '{value['value']}'")
    print("\n")
