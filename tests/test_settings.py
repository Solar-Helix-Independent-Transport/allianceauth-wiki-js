"""
Alliance Auth Test Suite Django settings.
"""

from allianceauth.project_template.project_name.settings.base import *

# Celery configuration
CELERY_ALWAYS_EAGER = True  # Forces celery to run locally for testing

INSTALLED_APPS += [
    'wikijs',
]

ROOT_URLCONF = 'tests.urls'

NOSE_ARGS = [
    #'--with-coverage',
    #'--cover-package=',
    #'--exe',  # If your tests need this to be found/run, check they py files are not chmodded +x
]

CACHES['default'] = {'BACKEND': 'django.core.cache.backends.db.DatabaseCache'}


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

#LOGGING = None  # Comment out to enable logging for debugging

# Register an application at https://developers.eveonline.com for Authentication
# & API Access and fill out these settings. Be sure to set the callback URL
# to https://example.com/sso/callback substituting your domain for example.com
# Logging in to auth requires the publicData scope (can be overridden through the
# LOGIN_TOKEN_SCOPES setting). Other apps may require more (see their docs).
ESI_SSO_CLIENT_ID = '123'
ESI_SSO_CLIENT_SECRET = '123'
ESI_SSO_CALLBACK_URL = '123'


WIKIJS_API_KEY = "abc-123"
WIKIJS_URL = "http://localhost/"
