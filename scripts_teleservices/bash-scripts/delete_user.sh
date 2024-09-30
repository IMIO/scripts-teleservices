#!/bin/bash

# lister les tenants
tenants_output=$(sudo -u authentic-multitenant authentic2-multitenant-manage list_tenants)

# extraire la 1ere partie de la réponse
tenant=$(echo "$tenants_output" | grep -oP '^\S+')

sudo -u authentic-multitenant authentic2-multitenant-manage runscript -d $tenant delete_user.py
