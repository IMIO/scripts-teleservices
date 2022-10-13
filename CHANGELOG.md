# Changelog
All notable changes to this project will be documented in this file.

## [0.0.72] - 13/10/2022
### Fixed
[SUP-26104] Fix link not workint since the django var already generate protocol 'https://'

## [0.0.71] - 09/08/2022
### Updated
- build-e-guichet for ts-light [njphspv, dmshd]
- datasources for ts-light [njphspv, dmshd]
- hobo for ts-light [njphspv, dmshd]
- combo-site for ts-light [njphspv, dmshd]

## [0.0.70] - 29/06/2022
### Added
- list wcs tenants [nhi]

## [0.0.69] - 27/06/2022
### Added
- bijoe cron randomizer [nhi]

## [0.0.68] - 15/06/2022 
### Changed
- set package as python package [nhi, nse]

## [0.0.67] - 07/02/2022 -
### Added
- init python scripts to handle secret keys [dmshd]

## [0.0.66] - 02/02/2022 -
### Added
- init bash-scripts folder with scripts to echo or change secret keys [dmshd]

## [0.0.65] - 25/01/2022 -
### Fixed
- Update script that clean all forms in all baskets to make it work following #61027 [dmshd]

## [0.0.64] - 18/01/2022 -
### Added
- add script to make basket item deletion more easy [dmshd]


## [0.0.63] - 18/01/2022 -
### Fixed
- [TELE-1207] add an echoing of a default cmd example [dmshd]

## [0.0.62] - 04/01/2022 -
### Fixed
- [MTELEPEQA-1] fix link to backoffice not working [dmshd]

## [0.0.61] - 29/10/2021 -
### Fixed
- [SUP-20664] fix my mistake making sed duplicate the insertion at rerun of the script [dmshd]

## [0.0.60] - 29/10/2021 -
### Fixed
- [SUP-20664] restore postgresql = true insertion since it is definitively necessary! [dmshd]

## [0.0.59] - 18/10/2021 -
### Changed
-  Replace "portail citoyen" by "e-guichet" in our text cells, links [dmshd]

## [0.0.58] - 18/10/2021 -
### Fixed
-  fix errors in links [dmshd]

## [0.0.57] - 15/10/2021 -
### Fixed
-  fix JSON syntax error (additionnal comma) [dmshd]

## [0.0.56] - 14/10/2021 -
### changed
-  [MTELEVOIA-3] update combo site strucutre JSONs (portail agent, site-strucure) so it looks like what we showed at the mandatories saloon and the actual demo teleservices website [dmshd]

## [0.0.55] - 14/10/2021 -
### added
- add example build command in comment so we do not have to search for latitude longitude during local instance ici [dmshd]

## [0.0.54] - 14/10/2021 -
### changed
- [TELE-1051] use newer wcs runscript command [dmshd]

## [0.0.53] - 14/10/2021 -
### removed
- [TELE-1050] remove postgresql = true from site-options since entr'ouvert told us it's no longer needed [dmshd]

## [0.0.52] - 14/10/2021 -
### removed
- [MTELEVOIA-3] remove old generic forms and workflows since we now use teleservices-package [dmshd]

## [0.0.51] - 11/10/2021 -
### added
- [TELE-653] set admints@imio.be at build [dmshd]

## [0.0.50] - 11/10/2021 -
### changed
- [TELE-653] optimize detection for admints mail setting detection [dmshd]

## [0.0.49] - 05/10/2021 -
### changed
- [INFRA-4003] [TELE-1119] add -k to avoid SSL error following the Infra advice about that
-
## [0.0.47] - 24/08/2021 -
### removed
  - [TELE-1046] Removed unused code [dmshd]
### changed
  - [TELE-1046] fix wrong echo [dmshd]

## [0.0.46] - 20/07/2021 -
### changed
  - [TELE-972] use idp_url instead of harcoded authentic url to redirect to my profile [nhi]

## [0.0.45] - 30/06/2021 -
### added
  - [TELE-937] add 2 new parameters to set default map pointer [dmu]

## [0.0.44] - 30/06/2021 -
### changed
  - [TELE-936] avoir multiple sed insert when script is run multiple times [dmu]

## [0.0.43] - 30/06/2021 -
### changed
  - clean code (I committed merge syntax by mistake) [dmu]

## [0.0.42] - 30/06/2021 -
### fixed
  - [TOWS-45] : fix command not run as wcs user causing user:group perm issues [dmu]

## [0.0.41] - 16/06/2021 -
### Changed
  - [cdw] : Update script count_users.py (2nd)

## [0.0.40] - 16/06/2021 -
### Changed
  - [cdw] : Update script count_users.py

## [0.0.39] - 25/05/2021 -
### Changed
  - [dmu] : fix wcs tenant path in install scripts


## [0.0.38] - 27/04/2021 -
### added
  - [dmu] : add fedict.py in ./build-e-guichet
  - init fedict.py with build-e-guichet.sh

## [0.0.37] - 21/01/2021 -
### Changed
  - [dmu] : remove not necessary slash char in url that might
    cause future probblems.
    (I replaced `{{portal_url}}/api` by `{{portal_url}}api`)

## [0.0.36] - 21/01/2021 -
### Changed
  - [nhi] : fix datasource's xml

## [0.0.35] - 12/01/2021 -
### Changed
  - [dmu] : add missing datasource (2nd)
    copy_datasources.sh had to be modified too


## [0.0.34] - 12/01/2021 -
### Changed
  - [dmu] : add missing datasource (2nd)
    There was a problem with the id not following the logic of datasources already there
    The xml file was also different from those already there
    This version is trying to fix the build-e-guichet who was impacted by that



## [0.0.33] - 06/01/2021 -
### Changed
  - [nhi] : add missing datasource


## [0.0.32] - 27/11/2020 -
### Changed
  - [nse] : patch 0.0.29


## [0.0.31] - 03/11/2020 -
### Changed
  - [dmu] : add 2 models (Modèles - Liste pays, Modèles - Champ fichier)


## [0.0.30] - 20/10/2020 -
### Changed
  - [dmu] : WF - Gestion des rendez-vous : Reminder deletion
    Since Entr'Ouvert september 2020 update : Reminder send is
     now native and can be set in each agenda.

## [0.0.29] - 19/10/2020 -
### Changed
  - [dmu] : add "mondossier" to "cohabitation legale" form
  - [dmu] : add "mondossier" to "certificat de residence avec historique" form


## [0.0.28] - 28/08/2020 -
### Changed
  - [dmu] : add "mondossier" to "cohabitation legale" form
  - [dmu] : add "mondossier" to "certificat de residence avec historique" form


## [0.0.28] - 28/08/2020 -
### Changed
  - [nse] : add "regie payment" as a form option
  - [nse] : normalize form option name and label

## [0.0.27] - 19/08/2020 -
### Changed
  - [dmu, nse, nhi] : remove link in a action of the departement citoyen wf and add button (link to basket after submission)

## [0.0.26] - 16/06/2020 -
### Changed
  -  fix add hobo extra params section (build-e-guichet.sh)
      some sed didn't worked as expected in local

## [0.0.25] - 16/06/2020 -
### Changed
  -  fix bad syntax in a condition (build-e-guichet.sh)

## [0.0.24] - ? -
### Changed
  -  ?

## [0.0.23] - 09-06-2020 -
### Changed
  -  recipe-$1-extra.json wasn't properly set during a local instance build-e-guichet launch
The json has "guichet-citoyen.be" (default) instead of "$2" (most of time "local" for a local instance).
So sudo -u hobo hobo-manage cook /etc/hobo/recipe-$1-extra.json was cooking with wrong json data.
https://github.com/IMIO/scripts-teleservices/commit/5e63fd1b996761676006e488a2687695c4cdbfba

## [0.0.22] - 31-05-2020 -
### Changed
  -  build-e-guichet/hobo_create_variables.py
    - avoir no-reply usage (default mail sender)
    https://github.com/IMIO/scripts-teleservices/commit/f487b0c77543043ae117820e3a50c86a5d83e8e3

## [0.0.21] - 12-05-2020 -
### Changed
  -  build-e-guichet/forms/models/form-prise-de-rendez-vous.wcs
    - add category model on a form who had no category and it caused crashes during our build-e-guichet.sh.
    https://github.com/IMIO/scripts-teleservices/commit/88c165ee6c502d325a6fa718d8e6ab7c47bb0748

## [0.0.20] - 28-04-2020 -
### Changed
  - build-e-guichet.sh
    - add better feebacks about what is going on (echo)

## [0.0.19] - 28-04-2020 -
### Changed
  - build-e-guichet.sh
    - espace \[ \] chars to makes sed work again
    - add condition to sed extra params json and to make it work for local

## [0.0.18] - 27-04-2020 -
### Changed
  - removes \u00.. special chars from json to fix error in my local instance (I can't run build-e-guichet without encoding errors tracebacks)

## [0.0.17] - 24-04-2020 -
### Changed
  - delete branches from pull requests
### Fixed
  - PEP8 warnings (missing whitespaces, indentations,... )
  - Removed unused statements

## [0.0.16] - 23-04-2020 -
### Added
  - Readme changelog init
  - something (example)
### Changed
  - everything (example)
### Fixed
  - PEP8 warnings (missing whitespaces, indentations,... )
  - Removed unused statements
