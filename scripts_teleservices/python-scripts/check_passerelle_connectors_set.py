"""List all Passerelle connectors activated and their types.

sudo -u passerelle passerelle-manage \
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


wcs_tenant = (
    subprocess.run(
        "ls /var/lib/authentic2-multitenant/tenants/",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        check=True,
    )
    .stdout.decode("utf-8")
    .split("\n")[0]
    .strip()
)

# Call the get_all_apps function and store the list of relevant model classes in all_apps
all_apps = get_all_apps()

# Initialize an empty list to store instances of models
all_instances = []

# Iterate over each model class in all_apps
for app in all_apps:
    # Extend the all_instances list with all instances (database records) of the current model class
    all_instances.extend(app.objects.all())  # app.objects.all() queries the database for all records of app model


all_instances.sort(key=lambda x: x.title.lower())


errors = []

errors.append(wcs_tenant)

for instance in all_instances:
    import pprint

    if instance.slug == "actualites":
        if instance.client_id[-2:] != "16":
            errors.append("client_id actualites incorrect")
        if instance.client_secret[-2:] != "dc":
            errors.append("client_secret actualites incorrect")
    if instance.slug == "annuaire":
        if instance.client_id[-2:] != "ee":
            errors.append("client_id annuaire incorrect")
        if instance.client_secret[-2:] != "07":
            errors.append("client_secret annuaire incorrect")
    if instance.slug == "evenements":
        if instance.client_id[-2:] != "d5":
            errors.append("client_id evenements incorrect")
        if instance.client_secret[-2:] != "e2":
            errors.append("client_secret evenements incorrect")
    if instance.slug == "site-web":
        if instance.client_id[-2:] != "dd":
            errors.append("client_id site-web incorrect")
        if instance.client_secret[-2:] != "df":
            errors.append("client_secret site-web incorrect")

print(errors)
