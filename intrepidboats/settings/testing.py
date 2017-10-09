#! coding: utf-8
import logging
# noinspection PyUnresolvedReferences
from .base import *

VENDOR_APPS = (
    'django_nose',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# we don't want logging while running tests.
logging.disable(logging.CRITICAL)
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)
DEBUG = False
TEMPLATE_DEBUG = False
TESTS_IN_PROGRESS = True

VIMEO_CONFIG = {
    'VIMEO_API_URL': env("VIMEO_API_URL", default="https://api.vimeo.com/"),
    'PRO_UPLOAD_TOKEN': "xxxxx"
}
