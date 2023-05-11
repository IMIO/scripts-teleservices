#!/bin/sh

set -e # Exit immediately if a command exits with a non-zero status.

CURRENT_DIR=/opt/publik/scripts/scripts_teleservices/bash-scripts

# setup passerelle connector
BAEC=/etc/passerelle/settings.d/baec.py
BAEC_FILE=baec.py
echo "--- Install passerelle settings"
if test -f "$BAEC"; then
    echo "$BAEC already exists. This is what we want so that's fine !"
else
    echo "$BAEC does not exist yet so I'm gonna create it and reboot passerelle..."
    cp CURRENT_DIR/$BAEC_FILE /etc/passerelle/settings.d/ && service passerelle restart
fi

CASIER=/etc/passerelle/settings.d/casier_judiciaire.py
CASIER_FILE=casier_judiciaire.py
if test -f "$CASIER"; then
    echo "$CASIER already exists. This is what we want so that's fine !"
else
    echo "$CASIER does not exist yet so I'm gonna create it and reboot passerelle..."
    echo $CURRENT_DIR/$CASIER_FILE
    cp $CURRENT_DIR/$CASIER_FILE /etc/passerelle/settings.d/ && service passerelle restart
fi
