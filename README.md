# Wiki-JS service

Simple User and group management for [Wiki JS](https://wiki.js.org/) as a service of AllianceAuth 

## Setup
0. install and setup your Wiki.js instance [from the Wiki Docs](https://docs.requarks.io/)
1. activate venv
2. `pip install -U alliacneauth-wiki-js`
3. add `'wikijs',` to your `INSTALLED_APPS` in your projects `local.py`
4. generate a `Full Access` API key iun the wiki with maximum expiration be sure to copy it as the key wont be shown again.
5. add the settings ( outlined below ) to your `local.py`
6. run migrations and restart auth
7. setup permissions ( outlined below )

## Permissions
Perm | Codename | Admin | Frontend
--- | --- | --- | ---
Can access the WikiJS service | access_wikijs | - | Gives access to Wiki.js service
Can add wiki js | - | Admin add | -
Can change wiki js | - | Admin Edit | -
Can delete wiki js | - | Admin Delete | -
Can view wiki js | - | Admin View | -

## Settings
Setting | default | Description
--- | --- | ---
WIKIJS_API_KEY | "" | your global API key from the wiki admin section
WIKIJS_URL | "" | You Wiki's base URL
