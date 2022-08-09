# SAMPLE : sh copy_categories.sh lalouviere lescommunes.be
if ! [ -d /var/lib/wcs/tenants/$1-formulaires.$2/datasources ]; then
    (mkdir /var/lib/wcs/tenants/$1-formulaires.$2/datasources && chown wcs:wcs /var/lib/wcs/tenants$1-formulaires.$2/datasources -Rf)
fi

if [ $3 == "full" ]; then
  cp datasources/98 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/98
  cp datasources/99 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/99
  cp datasources/100 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/100
  cp datasources/101 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/101
  cp datasources/102 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/102
  cp datasources/103 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/103
  cp datasources/104 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/104
  cp datasources/105 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/105
  cp datasources/106 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/106
  cp datasources/108 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/108
  cp datasources/109 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/109
  cp datasources/110 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/110
  cp datasources/111 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/111
  cp datasources/112 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/112
fi
if [ $3 == "light" ]; then
  cp datasources/104 /var/lib/wcs/tenants/$1-formulaires.$2/datasources/104
fi
