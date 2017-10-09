#! coding: utf-8
import os
# noinspection PyUnresolvedReferences
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin name', 'fernando@devartis.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.environ['DATABASE_HOST'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
    }
}

MEDIA_ROOT = os.environ['MEDIA_ROOT']
STATIC_ROOT = os.environ['STATIC_ROOT']
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

RAVEN_CONFIG = {
    'dsn': os.environ['RAVEN_DSN'],
}

INSTALLED_APPS = INSTALLED_APPS + ('raven.contrib.django.raven_compat',)

if env("ENABLE_EMAIL", default=False):
    INSTALLED_APPS += ('anymail',)
    ANYMAIL = {
        # (exact settings here depend on your ESP...)
        "MAILGUN_API_KEY": env("MAILGUN_API_KEY"),
        "MAILGUN_SENDER_DOMAIN": env("MAILGUN_SENDER_DOMAIN")
    }
    EMAIL_BACKEND = "anymail.backends.mailgun.EmailBackend"  # or sendgrid.EmailBackend, or...
    DEFAULT_FROM_EMAIL = NO_REPLY_EMAIL

TO_EMAIL = {
    "REGISTRATION_FORM": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "OPTIONAL_EQUIPMENT_TAB_FORM": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "EMPLOYMENT_PAGE_FORM": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "CONTACT_US_FORM": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "OWNERS_PORTAL_FEEDBACK_FORM": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "TESTIMONIAL_SHARE": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "BUILD_A_BOAT_SHARE": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "NEWSLETTER_FORM": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
    "POST_SUBMISSION_NOTIFICATION": [
        'dalvarez@devartis.com',
        'fernando@devartis.com',
    ],
}
