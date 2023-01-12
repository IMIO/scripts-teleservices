#!/bin/bash
grep -nF --color 'auth-contexts' /var/lib/wcs/tenants/*/site-options.cfg || sed -i "s~\[options\]~\[options\]\nauth-contexts = fedict~" /var/lib/wcs/tenants/*/site-options2.cfg
