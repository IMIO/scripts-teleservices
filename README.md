# scripts-teleservices
contains the scripts we use to initialize a clean iA.Téléservices instance.
It consist of variables creation, structures described in json importation, rôles creations, ...

## How to install

1. Enter the docker image and do a :
`sudo -u hobo hobo-manage cook /etc/hobo/recipe.json`
2. Change directory 
`cd /opt/publik/scripts/scripts_teleservices/build-e-guichet`
3. Run the installation bash script (build-e-guichet.sh)
`./build-e-guichet.sh local example.net full 5000 50.466575 4.865341 Local`
example :
`./build-e-guichet.sh charleroi guichet-citoyen.be full 6000 50.466575 4.865341 Charleroi`

Check the log, it should not return any tracebacks errors.
