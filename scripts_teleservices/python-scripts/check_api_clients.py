"""
20240122 - Script to check all the APIClients and verify if imio-maintenance is
set on the tenant.

Example of usage:

    sudo -u authentic-multitenant authentic2-multitenant-manage \
        tenant_command runscript -d staging2-auth.guichet-citoyen.be \
        /opt/publik/scripts/scripts_teleservices/python-scripts/test.py

"""
import subprocess

from authentic2.models import APIClient

tenant = subprocess.run(
    "ls /var/lib/authentic2-multitenant/tenants/",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    shell=True,
    check=True,
)

if tenant:
    tenant = tenant.stdout.decode("utf-8").split("\n")[0].strip()


# Fetch all the APIClient instances
api_clients = APIClient.objects.all()


imio_maintenance_set = bool()

if api_clients:
    # Debug listing of all the APIClient instances
    # print("API Clients Details:")
    # for api_client in api_clients:
    # print("ID:", api_client.id)
    # print("Name:", api_client.name)
    # print("Identifier:", api_client.identifier)
    # print("Is Active:", api_client.is_active)
    # print("Is Superuser:", api_client.is_superuser)
    # print("Description:", api_client.description)

    # check for imio-maintenance
    for api_client in api_clients:
        identifier = api_client.identifier
        if identifier == "imio-maintenance":
            imio_maintenance_set = True
            print("IMIO MAINTENANCE SET ON", tenant)
    if not imio_maintenance_set:
        print("IMIO MAINTENANCE NOT SET ON", tenant)
