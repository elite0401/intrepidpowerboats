#! coding: utf-8
import os

from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Admin name', 'admin_name@devartis.com'),
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
    'dsn': env('RAVEN_DSN'),
}

INSTALLED_APPS += (
    'cachalot',
    'raven.contrib.django.raven_compat',
)

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
        "intrepid-registration@intrepidpowerboats.com",
    ],
    "OPTIONAL_EQUIPMENT_TAB_FORM": [
        'kclinton@intrepidpowerboats.com',
        'pstoker@IntrepidPowerBoats.com',
        'cgonzalez@intrepidpowerboats.com',
    ],
    "EMPLOYMENT_PAGE_FORM": [
        "hr@intrepidpowerboats.com",
        "kclinton@intrepidpowerboats.com",
        "mbeaver@IntrepidPowerboats.com",
    ],
    "CONTACT_US_FORM": [
        'kclinton@intrepidpowerboats.com',
        'pstoker@IntrepidPowerBoats.com',
        'cgonzalez@intrepidpowerboats.com',
    ],
    "OWNERS_PORTAL_FEEDBACK_FORM": [
        'kclinton@intrepidpowerboats.com',
        'pstoker@IntrepidPowerBoats.com',
        'cgonzalez@intrepidpowerboats.com',
        'customercare@intrepidpowerboats.com',
        'jbrenna@IntrepidPowerboats.com',
    ],
    "TESTIMONIAL_SHARE": [
        'customercare@intrepidpowerboats.com',
        'jbrenna@IntrepidPowerboats.com',
        'kclinton@intrepidpowerboats.com',
    ],
    "BUILD_A_BOAT_SHARE": [
        'kclinton@intrepidpowerboats.com',
        'pstoker@IntrepidPowerBoats.com',
        'cgonzalez@intrepidpowerboats.com',
    ],
    "NEWSLETTER_FORM": [
        "intrepid-newsletter@intrepidpowerboats.com",
    ],
    "POST_SUBMISSION_NOTIFICATION": [
        "customercare@intrepidpowerboats.com",
        "jbrenna@IntrepidPowerboats.com",
        "kclinton@intrepidpowerboats.com",
    ],
}
# Contact email addresses
INQUIRY_EMAIL_ADDRESS = TO_EMAIL['CONTACT_US_FORM']
BOAT_INFORMATION_EMAIL_ADDRESS = TO_EMAIL['CONTACT_US_FORM']
SALES_EMAIL_ADDRESS = TO_EMAIL['CONTACT_US_FORM']

VIMEO_CONFIG = {
    'VIMEO_API_URL': env("VIMEO_API_URL", default="https://api.vimeo.com/"),
    'PRO_UPLOAD_TOKEN': env("VIMEO_PRO_UPLOAD_TOKEN")
}

COMPRESS_ENABLED = True

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    }
}
