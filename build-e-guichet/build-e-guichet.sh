#!/bin/bash
# USAGE : 
# $1 : commune_id (test, demo, local, huy, liege,...)
# $2 : domain (guichet-citoyen.be, example.net, ...)
# $3 : Type Instance light or full (case sensitive)
# $4 : All town's postcodes with a comma as separator (4000,4020,...)

# Use postgresql with wcs
echo "-- Writing 'postgresql = true' in /var/lib/wcs/$1-formulaires.$2/site-options.cfg "
sed -i '/\[options\]/a postgresql = true' /var/lib/wcs/$1-formulaires.$2/site-options.cfg
sleep 0.1

# Add resubmit action in workflows
echo "-- Writing 'workflow-resubmit-action = true' in /var/lib/wcs/$1-formulaires.$2/site-options.cfg "
sed -i '/\[options\]/a workflow-resubmit-action = true' /var/lib/wcs/$1-formulaires.$2/site-options.cfg
sleep 0.1

# Create categories
echo "-- Creating categories ..."
sh copy_categories.sh $1 $2
sleep 0.1

# Create datasources
echo "-- Creating datasources ..."
sh copy_datasources.sh $1 $2
sleep 0.1

# Create passerelle api user.
echo "-- Creating passerelle API user ..."
sudo -u passerelle /usr/bin/passerelle-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/passerelle/build-api-user.py -d $1-passerelle.$2
sleep 0.1

# Create passerelle "ts1 datasources connector" with prefilled motivations and destinations terms.
echo "-- Creating passerelle 'ts1 datasources' connector with prefilled motivations and destinations terms ..."
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/build-e-guichet/datasources/datasources.json
sleep 0.1

# Create passerelle "pays" datasource. (To choice country in users' profile).
echo "-- Creating passerelle 'pays' datasource ..."
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/build-e-guichet/passerelle/pays.json --import-users
sleep 0.1

# Add hobo extra params
echo "-- Applying hobo-manage cook to extra hobo params defined in /etc/hobo/recipe-$1-extra.json  ..."
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
sed -e "s~commune~$1~g" hobo/recipe-commune-extra.json > /etc/hobo/recipe-$1-extra.json
if [ $1 = "local" ];then
  sed -i "s~guichet-citoyen.be~$2~g" /etc/hobo/recipe-$1-extra.json
  sed -i 's~https~http~g' /etc/hobo/recipe-$1-extra.json
fi
test -e /etc/hobo/recipe-$1-extra.json && sudo -u hobo hobo-manage cook /etc/hobo/recipe-$1-extra.json
sleep 0.1

# Adapt country field in DB to have a list field instead a text field
echo "-- Applying hobo-manage cook to extra hobo params defined in /etc/hobo/recipe-$1-extra.json  ..."
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/auth_fedict_var.py -d $1-auth.$2
sleep 0.1

# Import defaults authentic users
echo "-- Importing authentic users and roles ..."
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/build-e-guichet/import-authentic-user.py -d $1-auth.$2
sleep 0.1

echo "-- Waiting 30 seconds to be certain authentic and wcs are synchronized ..."
sleep 30

# Set permissions
echo "-- Setting permissions ..."
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-permissions.py $3
sleep 0.1

# Import workflows
echo "-- Generic workflows installation ..."
sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-workflows.py /opt/publik/scripts/build-e-guichet/workflows/
if [ $3 = "full" ]
    then
    echo "INSTALL WORKFLOWS FOR FULL INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-workflows.py /opt/publik/scripts/build-e-guichet/workflows/only_full/
fi
sleep 0.1

# Import forms
echo "-- Generic forms installation ..."
if [ $3 = "full" ]
    then
    echo "INSTALL FORMS FOR FULL INSTANCE."
    sed -i "s/<option varname="cp_commune">\[cp_commune\]<\/option>/<option varname="cp_commune">$4<\/option>/g" /opt/publik/scripts/build-e-guichet/forms/only_full/*.wcs
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-forms.py /opt/publik/scripts/build-e-guichet/forms/only_full/
    sed -i "s/<option varname="cp_commune">$4<\/option>/<option varname="cp_commune">\[cp_commune\]<\/option>/g" /opt/publik/scripts/build-e-guichet/forms/only_full/*.wcs
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-forms.py /opt/publik/scripts/build-e-guichet/forms/models/
else
    echo "INSTALL FORMS FOR LIGHT INSTANCE."
    sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/import-forms.py /opt/publik/scripts/build-e-guichet/forms/only_light/
fi
sleep 0.1

# Create regie
echo "-- Payment managament creation (régie) ..."
sudo -u combo combo-manage tenant_command runscript -d $1.$2 lingo_create_regie.py
# Puppet deploy search for : create_regie.py.erb
if [ -f /var/lib/combo/create_regie.py ]
    then
sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /var/lib/combo/create_regie.py
fi
sleep 0.1

# Import combo site structure
echo "-- Importing combo site structure ..."
if [ $3 = "full" ]
    then
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-full.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-full.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/build-e-guichet/combo-site/combo-site-structure-full.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-full.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-full.json
else
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-light.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-light.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/build-e-guichet/combo-site/combo-site-structure-light.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-light.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-light.json
fi
sleep 0.1

# Import combo portail agent structure
echo "-- Importing combo agent portail structure ..."
sed -i "s/COMMUNE/$1/g" combo-site/combo-portail-agent-structure.json
sed -i "s/DOMAINE/$2/g" combo-site/combo-portail-agent-structure.json
sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /opt/publik/scripts/build-e-guichet/combo-site/combo-portail-agent-structure.json
sed -i "s/$1/COMMUNE/g" combo-site/combo-portail-agent-structure.json
sed -i "s/$2/DOMAINE/g" combo-site/combo-portail-agent-structure.json
sleep 0.1

# Create global hobo variables
echo "-- Creating hobo variables ..."
sudo -u hobo hobo-manage tenant_command runscript -d $1-hobo.$2 /opt/publik/scripts/build-e-guichet/hobo_create_variables.py
sleep 0.1

echo "-- cat /etc/combo/settings.py : "
cat /etc/combo/settings.py
sleep 0.1

# Deploy wcs properties : postgresql, smtp_server, homepage_redirect.
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/wcs_config.py $1 $2
# echo "sudo -u wcs wcs-manage convert-to-sql --dbname=teleservices_"$1"_wcs --user=teleservices_"$1"_teleservices --password=... --host=database.lan.imio.be" $1"-formulaires.guichet-citoyen.be"

echo " -- Config mail : mailrelay.imio.be"
