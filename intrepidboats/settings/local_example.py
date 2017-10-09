#! coding: utf-8
# noinspection PyUnresolvedReferences
from .base import *

ADMINS = (
    ('admin_name', 'admin_name@devartis.com'),
)
ALLOWED_HOSTS = ["*"]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_sample.dev.sqlite',
    }
}
VIMEO_CONFIG = {
    'VIMEO_API_URL': env("VIMEO_API_URL", default="https://api.vimeo.com/"),
    'PRO_UPLOAD_TOKEN': env("VIMEO_PRO_UPLOAD_TOKEN")
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': env('DATABASE_NAME'),
#         'USER': env('DATABASE_USER'),
#         'PASSWORD': env('DATABASE_PASSWORD'),
#         'HOST': env('DATABASE_HOST'),
#         'PORT': '5432',
# }
# }
