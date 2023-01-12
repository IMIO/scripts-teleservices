#!/bin/sh

set -e # Exit immediately if a command exits with a non-zero status.

# setup passerelle connector
FILE=/etc/passerelle/settings.d/baec.py
if test -f "$FILE"; then
    echo "$FILE already exists. This is what we want so that's fine !"
else
    echo "$FILE does not exist yet so I'm gonna create it and reboot passerelle..."
    cp $(pwd)/baec.py /etc/passerelle/settings.d/ && service passerelle restart
fi
