"""check_passerelle_connectors_set.py List all Passerelle connectors activated and their types."""

import argparse
import pprint

from django.apps import apps
from passerelle.base.models import BaseResource

debug_mode = False


def get_all_apps():
    """Return all apps that have a model that inherits from BaseResource."""
    return [x for x in apps.get_models() if issubclass(x, BaseResource) and x.is_enabled()]


# Fetch all app instances
all_apps = get_all_apps()
all_instances = []

for app in all_apps:
    all_instances.extend(app.objects.all())

# Sorting the instances by title
all_instances.sort(key=lambda x: x.title.lower())

# list for json output
json_output = {}

# Format and print details of each instance
for instance in all_instances:
    # print(dir(instance))
    json_output.setdefault(type(instance).__name__, []).append(instance.__dict__)
    print(instance.availability_parameters)

if debug_mode:
    pprint.pprint(json_output)
else:
    print(json_output)
