# SAMPLE : sh copy_categories.sh lalouviere lescommunes.be
if ! [ -d /var/lib/wcs/$1-formulaires.$2/datasources ]
then
    (mkdir /var/lib/wcs/$1-formulaires.$2/datasources)
fi

sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/98 > /var/lib/wcs/$1-formulaires.$2/datasources/98
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/99 > /var/lib/wcs/$1-formulaires.$2/datasources/99
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/100 > /var/lib/wcs/$1-formulaires.$2/datasources/100
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/101 > /var/lib/wcs/$1-formulaires.$2/datasources/101
sed "s~http://local-passerelle.example.net~https://$1-passerelle.$2~g" datasources/102 > /var/lib/wcs/$1-formulaires.$2/datasources/102
