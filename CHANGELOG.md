# Changelog
All notable changes to this project will be documented in this file.

## [0.0.21] - 12-05-2020 -
### Changed
  - build-e-guichet.sh 
    - add category model on a form who had no category and it causes crashed during our build-e-guichet.sh.
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
