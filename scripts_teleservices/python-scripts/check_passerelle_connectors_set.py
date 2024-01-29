"""List all Passerelle connectors activated and their types.

sudo -u passerelle-multitenant passerelle-multitenant-manage \
    tenant_command runscript -d staging2-passerelle.guichet-citoyen.be \
    /opt/publik/scripts/scripts_teleservices/python-scripts/test.py
"""
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


# Call the get_all_apps function and store the list of relevant model classes in all_apps
all_apps = get_all_apps()

# Initialize an empty list to store instances of models
all_instances = []

# Iterate over each model class in all_apps
for app in all_apps:
    # Extend the all_instances list with all instances (database records) of the current model class
    all_instances.extend(app.objects.all())  # app.objects.all() queries the database for all records of app model


all_instances.sort(key=lambda x: x.title.lower())


for instance in all_instances:
    absolute_url = instance.get_absolute_url()
    if "aes" not in absolute_url:  # I don't want to change the log level of AES (another team is handling it)
        logging_params = instance.logging_parameters
        logging_params.trace_emails = trace_email_to_define
        logging_params.log_level = log_level_to_define
        try:
            instance.logging_parameters.full_clean()
        except Exception as e:
            print("Error while cleaning instance", e)

        try:
            logging_params.save()
        except Exception as e:
            print("Error while saving instance", e)

        # logging_params.refresh_from_db() # to get the new values from the database
