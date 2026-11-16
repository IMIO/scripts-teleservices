#!/bin/bash

# lister les tenants
tenants_output=$(sudo -u authentic-multitenant authentic2-multitenant-manage list_tenants)

# extraire la 1ere partie de la réponse
tenant=$(echo "$tenants_output" | grep -oP '^\S+\s+\K\S+')

sudo -u authentic-multitenant authentic2-multitenant-manage tenant_command runscript -d $tenant /opt/publik/scripts/scripts_teleservices/python-scripts/delete_user.py
