# -*- coding: utf-8 -*-
# sudo -u  wcs wcsctl -f /etc/wcs/wcs-au-quotidien.cfg runscript --vhost=$1-formulaires.$2 /opt/publik/scripts/build-e-guichet/wcs_config.py $1

import sys
from quixote import get_publisher

pub = get_publisher()
if sys.argv[1].upper() == "LOCAL":
    pub.cfg['misc']['homepage-redirect-url'] = 'http://{0}.{1}/demarches/'.format(sys.argv[1], sys.args[2])
    pub.cfg['postgresql'] = {'database': 'wcs',
                             'user': 'postgres',
                             'host': 'database',
                             'port': '5432',
                             'password': 'password'}
else:
    pub.cfg['misc']['homepage-redirect-url'] = 'https://{0}.{1}/demarches/'.format(sys.argv[1], sys.args[2])

pub.write_cfg()
