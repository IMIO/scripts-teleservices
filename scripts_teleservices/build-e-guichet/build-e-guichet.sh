#!/bin/bash
# USAGE :
# $1 : commune_id (test, demo, local, huy, liege,...)
# $2 : domain (guichet-citoyen.be, example.net, ...)
# $3 : Type Instance light or full (case sensitive)
# $4 : All town's postcodes with a comma as separator (4000,4020,...)
# $5 : Latitude of the map pointer
# $6 : Longitude of the map pointer
# $7 : Organisation label : if many words use " "

# echoing example if no args
if [ -z "$1" ]; then
    echo "Exemple pour instance locale : ./build-e-guichet.sh local example.net full 5000 50.466575 4.865341 Local"
    exit 1
fi

# add custom settings in wcs site-options.cfg
## set var for following sed commands
match="\[options\]"
file="/var/lib/wcs/tenants/$1-formulaires.$2/site-options.cfg"

echo "-- Writing 'postgresql = true' in the site-options.cfg"
insert='postgresql = true'
grep -qxF "$insert" $file || sed -i "s/$match/$match\n$insert/" $file
sleep 0.1

echo "-- Setting 'workflow-resubmit-action = true' in the site-options.cfg "
insert='workflow-resubmit-action = true'
grep -qxF "$insert" $file || sed -i "s/$match/$match\n$insert/" $file
sleep 0.1

echo "-- Set default map pointer (ex: default_position = 48.8336428;2.3233045) in $file"
insert="default_position = $5;$6"
grep -qxF "$insert" $file || sed -i "s/$match/$match\n$insert/" $file
sleep 0.1

# Create categories
if [ $3 == "full" ]; then
  echo "-- Creating categories ..."
  sudo -u wcs sh copy_categories.sh $1 $2
  sleep 0.1
fi

# Create datasources
echo "-- Creating datasources ..."
sudo -u wcs sh copy_datasources.sh $1 $2 $3
sleep 0.1

# Create passerelle api user.
echo "-- Creating passerelle API user ..."
sudo -u passerelle /usr/bin/passerelle-manage tenant_command runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/passerelle/build-api-user.py -d $1-passerelle.$2
sleep 0.1

# Create passerelle "ts1 datasources connector" with prefilled motivations and destinations terms.
if [ $3 == "full" ]; then
  echo "-- Creating passerelle 'ts1 datasources' connector with prefilled motivations and destinations terms ..."
  sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/datasources/datasources.json
  sleep 0.1
fi

# Create passerelle "pays" datasource. (To choice country in users' profile).
echo "-- Creating passerelle 'pays' datasource ..."
sudo -u passerelle /usr/bin/passerelle-manage tenant_command import_site -d $1-passerelle.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/passerelle/pays.json --import-users
sleep 0.1

# Add hobo extra params
echo "-- Applying hobo-manage cook to extra hobo params defined in /etc/hobo/recipe-$1-extra.json  ..."
sudo -u hobo hobo-manage cook /etc/hobo/recipe.json
sed -e "s~commune~$1~g" hobo/recipe-commune-extra.json >/etc/hobo/recipe-$1-extra.json
sed -e "s~ORAGNISATION_LABEL~$7~g" hobo/recipe-commune-extra.json >/etc/hobo/recipe-$1-extra.json
if [ $1 = "local" ]; then
    sed -i "s~guichet-citoyen.be~$2~g" /etc/hobo/recipe-$1-extra.json
    sed -i 's~https~http~g' /etc/hobo/recipe-$1-extra.json
fi
test -e /etc/hobo/recipe-$1-extra.json && sudo -u hobo hobo-manage cook /etc/hobo/recipe-$1-extra.json
sleep 0.1

# Adapt country field in DB to have a list field instead a text field
echo "-- Adapt country field in DB to have a list field instead a text field  ..."
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/auth_fedict_var.py -d $1-auth.$2
sleep 0.1

# Import defaults authentic users
echo "-- Importing authentic users and roles ..."
authentic2-multitenant-manage tenant_command runscript /opt/publik/scripts/scripts_teleservices/build-e-guichet/import-authentic-user.py -d $1-auth.$2
sleep 0.1

echo "-- Waiting 30 seconds to be certain authentic and wcs are synchronized ..."
sleep 30

# Set permissions
echo "-- Setting permissions ..."
sudo -u wcs wcs-manage runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/import-permissions.py $3
sleep 0.1

# Create regie
if [ $3 == "full" ]; then
  echo "-- Payment managament creation (régie) ..."
  sudo -u combo combo-manage tenant_command runscript -d $1.$2 lingo_create_regie.py
  # Puppet deploy search for : create_regie.py.erb
  if [ -f /var/lib/combo/create_regie.py ]; then
      sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /var/lib/combo/create_regie.py
  fi
  sleep 0.1
fi

# Import combo site structure
echo "-- Importing $3 combo site structure ..."
if [ $3 = "full" ]; then
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-full.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-full.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/combo-site/combo-site-structure-full.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-full.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-full.json
fi
if [ $3 = "light" ]; then
    sed -i "s/COMMUNE/$1/g" combo-site/combo-site-structure-light.json
    sed -i "s/DOMAINE/$2/g" combo-site/combo-site-structure-light.json
    sudo -u combo combo-manage tenant_command import_site -d $1.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/combo-site/combo-site-structure-light.json
    sed -i "s/$1/COMMUNE/g" combo-site/combo-site-structure-light.json
    sed -i "s/$2/DOMAINE/g" combo-site/combo-site-structure-light.json
fi
sleep 0.1

# Import combo portail agent structure
echo "-- Importing combo agent portail structure ..."
sed -i "s/COMMUNE/$1/g" combo-site/combo-portail-agent-structure.json
sed -i "s/DOMAINE/$2/g" combo-site/combo-portail-agent-structure.json
sudo -u combo combo-manage tenant_command import_site -d $1-portail-agent.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/combo-site/combo-portail-agent-structure.json
sed -i "s/$1/COMMUNE/g" combo-site/combo-portail-agent-structure.json
sed -i "s/$2/DOMAINE/g" combo-site/combo-portail-agent-structure.json
sleep 0.1

# Create global hobo variables
echo "-- Creating hobo variables ..."
if [ $3 = "full" ]; then
  sudo -u hobo hobo-manage tenant_command runscript -d $1-hobo.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/hobo_create_variables.py
fi
if [ $3 = "light" ]; then
  sudo -u hobo hobo-manage tenant_command runscript -d $1-hobo.$2 /opt/publik/scripts/scripts_teleservices/build-e-guichet/hobo_create_variables_light.py
fi
sleep 0.1

echo "-- cat /etc/combo/settings.py : "
cat /etc/combo/settings.py
sleep 0.1

# Create fedict.py in /etc/authentic2-multitenant/settings.d/
if [ $3 = "full" ]; then
  echo "-- initalizing fedict.py : "
  sed "s/nomcommune/$1/g" fedict.py >/etc/authentic2-multitenant/settings.d/fedict.py
fi

# Setting mail to reveice trace errors
echo "-- Setting admints@imio.be as 'mail for trace errors' ..."
sudo -u wcs wcs-manage runscript --all-tenants /opt/publik/scripts/scripts_teleservices/build-e-guichet/set-error-mail-to-admints.py
sleep 0.1