# Changelog
All notable changes to this project will be documented in this file.

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
