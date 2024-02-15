"""
Tool to debug Hobo variables.

Usage :

    sudo -u hobo hobo-manage tenant_command runscript \
        -d demo-hobo.guichet-citoyen.be \
        /opt/publik/scripts/scripts_teleservices/build-e-guichet/hobo_create_variables.py

"""


from hobo.environment.models import Variable


def create_variable(name, label, value):
    """
    Create a variable.

    Usage :

        create_variable("queuefair", "Queue-Fair activé", "True")
    """
    variable, created = Variable.objects.get_or_create(name=name, defaults={"label": label, "value": value})
    if created:
        print(f"Variable '{name}' has been created.")
    else:
        print(f"Variable '{name}' already exists. Fine.")


def create_or_update_variable(name, label, value):
    """
    Create or update a variable.

    Usage :

        create_or_update_variable("queuefair", "Queue-Fair activé", "True")
    """
    variable, created = Variable.objects.update_or_create(name=name, defaults={"label": label, "value": value})
    if created:
        print(f"Variable '{variable}' has been created.")
    else:
        print(f"Variable '{variable}' has been updated.")


def get_variable_info(name):
    """
    Get information about a variable.

    Usage:

        get_variable_info("queuefair")
    """
    try:
        variable = Variable.objects.get(name=name)
        print(f"Name: {variable.name}, Label: {variable.label}, Value: {variable.value}")
    except Variable.DoesNotExist:
        print(f"Variable '{name}' does not exist.")


# Example of usage:
# get_variable_info("var_name")
# create_or_update_variable("var_name", "Le libellé de la variable", "value")
# create_variable("var_name", "Le libellé de la variable", "value")
#
# Add you instructions below and run this script with (replace the tenant name):
#    sudo -u hobo hobo-manage tenant_command runscript -d REPLACE_WITH_TENANT /opt/publik/scripts/scripts_teleservices/python-scripts/hobo_var_tools.py
