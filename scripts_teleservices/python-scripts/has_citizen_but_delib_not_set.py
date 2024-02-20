"""
Return feedback if instance is a iA.Citizen and give feedback about its delib connector.
Made for project management / testing / quality assurance purposes.

sudo -u passerelle passerelle-manage \
    tenant_command runscript -d frasneslezanvaing-passerelle.guichet-citoyen.be \
    /opt/publik/scripts/scripts_teleservices/python-scripts/has_citizen_but_delib_not_set.py
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


passerelle_tenant = (
    subprocess.run(
        "ls /var/lib/passerelle/tenants/",
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


feedback = []
feedback.append(passerelle_tenant)

already_has_a_delib_connector = False
delib_connector_working = False
ia_citizen = False
delib_connector = False
delib_connector_url = False


for instance in all_instances:
    if instance.slug == "deliberations":
        already_has_a_delib_connector = True
        delib_connector = instance
        delib_connector_url = "https://" + passerelle_tenant + delib_connector.get_absolute_url()

    if instance.slug == "actualites":
        ia_citizen = True


if delib_connector and not ia_citizen:
    feedback.append("DELIB EXIST BUT NO iA.CITIZEN.")

if ia_citizen and not already_has_a_delib_connector:
    feedback.append("CITIZEN BUT DELIB MISSING.")

if ia_citizen and already_has_a_delib_connector:
    feedback.append("iA.Citizen AND DELIB EXIST")

if not ia_citizen and not already_has_a_delib_connector:
    feedback.append("NOTHING HERE.")

if delib_connector_url:
    feedback.append(delib_connector_url)


print(feedback)
