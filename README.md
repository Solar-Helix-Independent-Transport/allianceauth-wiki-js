# Wiki-JS service

Simple User and group management for [Wiki JS](https://wiki.js.org/) as a service of AllianceAuth 

## Setup
0. install and setup your Wiki.js instance [from the Wiki Docs](https://docs.requarks.io/)
1. activate venv
2. `pip install -U allianceauth-wiki-js`
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
WIKIJS_AADISCORDBOT_INTEGRATION | True | Enables an AADiscordbot cog with the ability to search the wiki

If you have issues with auth not being able to access the wiki due to SSL/redirection or similar. ( Cloudlfair can cause issues)

Setting | default | Description
--- | --- | ---
WIKIJS_API_URL | WIKIJS_URL | URL Overide for API access

add this setting to your local py with a direct link to the wiki
```python
# if auth is on the same box as wiki
WIKIJS_API_URL = "http://localhost:3000"

# if auth is on a different machine you could use the public ip adress of that machine.
WIKIJS_API_URL = "http://10.0.0.150:3000"
```

## FAQ
* I lost admin when i registered my admin user.
    * add a group called `Administrators` to your auth instance and give it to anyone who needs admin on the wiki.
* I cant lock down my wiki to registered members only.
    * i had to delete a row from the database manually to remove the guest roles permissions. Ask in the AA discord.

