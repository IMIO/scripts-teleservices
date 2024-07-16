#!/bin/bash

# lister les tenants
tenants_output=$(sudo -u hobo hobo-manage list_tenants)

# Extraire la 1ere partie de la réponse
fargo_tenant=$(echo "$tenants_output" | grep -oP '^\S+')

echo "fargo tenant : $fargo_tenant"

#tuer fargo
echo "delete from ${fargo_tenant}.environment_fargo;"
