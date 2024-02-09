"""
Needed to then manually update compromised secrets manually.
List all Passerelle connectors activated and their types.

sudo -u passerelle passerelle \
    tenant_command runscript -d demo-passerelle.guichet-citoyen.be \
    /opt/publik/scripts/scripts_teleservices/python-scripts/test.py
"""

import os
import subprocess

from django.apps import apps
from passerelle.base.models import BaseResource

trace_email_to_define = f""  # empty string to disable trace emails
log_level_to_define = "ERROR"  # possible values : INFO, DEBUG, WARNING, ERROR, CRITICAL


def get_all_apps():
    """Return all apps that have a model that inherits from BaseResource."""
    # Loop through all model classes registered in the Django project
    return [
        x
        for x in apps.get_models()  # Get all model classes
        if issubclass(x, BaseResource)  # Check if the model is a subclass of BaseResource
        and x.is_enabled()  # Check if the model is enabled (based on its is_enabled() method)
    ]


https = "https://"
base_passerelle_url = https + os.environ.get("HOSTNAME").replace("teleservices", "-passerelle.guichet-citoyen.be")


# Call the get_all_apps function and store the list of relevant model classes in all_apps
all_apps = get_all_apps()

# Initialize an empty list to store instances of models
all_instances = []

# Iterate over each model class in all_apps
for app in all_apps:
    # Extend the all_instances list with all instances (database records) of the current model class
    all_instances.extend(app.objects.all())  # app.objects.all() queries the database for all records of app model


all_instances.sort(key=lambda x: x.title.lower())

urls_debug = []

urls_debug.append(base_passerelle_url)

for instance in all_instances:
    if instance.title:
        if "Annuaire" in instance.title or "":
            url = base_passerelle_url + instance.get_absolute_url()
            urls_debug.append(url)


print(urls_debug)
