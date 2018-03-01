from __future__ import absolute_import, unicode_literals

from os.path import dirname

import environ
from django.utils.translation import ugettext_lazy as _
from machina import MACHINA_VANILLA_APPS, MACHINA_MAIN_STATIC_DIR

SETTINGS_DIR = environ.Path(__file__) - 1
ROOT_DIR = environ.Path(__file__) - 3  # (/a/b/myfile.py - 3 = /)
APPS_DIR = ROOT_DIR.path(dirname(dirname(__file__)))

env = environ.Env()
environ.Env.read_env(SETTINGS_DIR('.env'))

DEBUG = True

ADMINS = ()

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
]

LOCALE_PATHS = (
    ROOT_DIR('locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = str(ROOT_DIR('media'))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    str(ROOT_DIR.path('intrepidboats/static')),
    MACHINA_MAIN_STATIC_DIR,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9!n$10$pksr3j5dv*4bc21ke$%0$zs18+vse=al8dpfzi_9w4y'

MIDDLEWARE_CLASSES = (
    'cms.middleware.utils.ApphookReloadMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Machina
    'machina.apps.forum_permission.middleware.ForumPermissionMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'intrepidboats.apps.common.middleware.middleware.MobileTabletDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

FLAVOURS = (u'full', u'mobile', u'tablet',)

ANONYMOUS_USER_ID = -1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'intrepidboats.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'intrepidboats.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'django_settings_export.settings_export',
                # Machina
                'machina.core.context_processors.metadata',
                'django_mobile.context_processors.flavour',
                'intrepidboats.apps.common.context_processors.site_metadata_processor',
            ],
            'debug': True,
            'loaders': [
                'django_mobile.loader.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.filesystem.Loader'
            ]
        },
    },
]

TEMPLATE_LOADERS = TEMPLATES[0]['OPTIONS']['loaders']

DJANGO_BASE_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangocms_admin_style',
    'django.contrib.admin',
    'django.contrib.sitemaps',
]

VENDOR_APPS = [
    'bootstrap3',
    'django_extensions',
    'django_js_reverse',
    'ckeditor',
    'compressor',
    # Machina related apps:
    'mptt',
    'easy_thumbnails',
    'filer',
    'haystack',
    'whoosh',
    'widget_tweaks',
    'colorfield',
    'el_pagination',
    'django_mobile',
    'polymorphic',
    'nocaptcha_recaptcha',
]

CMS_APPS = [
    'cms',  # django CMS itself
    'treebeard',  # utilities for implementing a tree
    'menus',  # helper for model independent hierarchical website navigation
    'sekizai',  # for JavaScript and CSS management
    'djangocms_text_ckeditor',
    'djangocms_picture',
    'djangocms_vimeo',
]

APPS = [
    'intrepidboats.apps.common',
    'intrepidboats.apps.owners_portal.apps.OwnersPortalConfig',
    'intrepidboats.apps.boats',
    'intrepidboats.apps.contact',
    'intrepidboats.apps.difference',
    'intrepidboats.libs.forum_integration',
    'intrepidboats.libs.vimeo_rate_limiting',
]

INSTALLED_APPS = DJANGO_BASE_APPS + VENDOR_APPS + APPS + CMS_APPS + MACHINA_VANILLA_APPS

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.security.DisallowedHost': {
            'handlers': ['null'],
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

# EMAILS
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
VIMEO_CONFIG = {}

# DJANGO REVERSE JS
JS_REVERSE_INCLUDE_ONLY_NAMESPACES = ['owners_portal', "boats", "common", ]

# Boat conf
BOAT_CONFIG = {
    "BOAT_IMAGES": "boat_images/"
}

# CMS
CMS_TOOLBAR_HIDE = False
CMS_TEMPLATES = (
    ('contact/contact.html', 'Contact Page'),
    ('contact/careers.html', 'Careers Page'),
    ('difference/difference_index.html', 'Intrepid Difference page'),
)

CMS_PLACEHOLDER_CONF = {
    # Intrepid Difference
    'About Text': {'plugins': ['TextPlugin', 'PicturePlugin', ]},
    'Owner Privileges Image': {'plugins': ['PicturePlugin']},
    'Owner Privileges Text': {'plugins': ['TextPlugin']},
    'Testimonials': {'plugins': ['TestimonialCMSPlugin', 'TextPlugin']},

    'One of a kind (Left column)': {'plugins': ['TextPlugin', 'PicturePlugin', ]},
    'One of a kind (Right column)': {'plugins': ['TextPlugin', 'PicturePlugin', ]},
    'One of a kind (Slider image)': {'plugins': ['ImageWithTextPluginCMSPlugin']},

    'Versatility (Left column)': {'plugins': ['IntrepidDifferenceSectionCMSPlugin', 'TextPlugin']},
    'Versatility (Right column)': {'plugins': ['IntrepidDifferenceSectionCMSPlugin', 'TextPlugin']},

    'Craftmanship (Left column)': {'plugins': ['IntrepidDifferenceSectionCMSPlugin', 'TextPlugin']},
    'Craftmanship (Right column)': {'plugins': ['IntrepidDifferenceSectionCMSPlugin', 'TextPlugin']},

    # Contact
    'Headquarters information': {'plugins': ['TextPlugin']},
    'Employees (Left column)': {'plugins': ['CompanyAreaCMSPlugin', 'TextPlugin']},
    'Employees (Right column)': {'plugins': ['CompanyAreaCMSPlugin', 'TextPlugin']},

    # Careers
    'jobs': {'plugins': ['JobDescriptionCMSPlugin', 'TextPlugin']},
}

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    # 'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
    'intrepidboats.apps.boats.utils.rotate',
)

HOME_PAGE_SETTINGS_NAME = "home"

PRE_OWNED_EXTERNAL_LINK = "http://www.yachtworld.com/core/listing/cache/pl_search_results.jsp?" \
                          "ywo=intrepidse&ps=50&type=&new=&" \
                          "luom=126&hosturl=intrepidse&page=broker&slim=broker&lineonly"

GEAR_EXTERNAL_LINK = "https://www.intrepidpowerboatsgear.com/"

SETTINGS_EXPORT = [
    'PRE_OWNED_EXTERNAL_LINK',
    'FACEBOOK_APP_ID',
    'GEAR_EXTERNAL_LINK',
]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    'machina_attachments': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp',
    }
}

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': ROOT_DIR('whoosh_index'),
    },
}

MACHINA_BASE_TEMPLATE_NAME = "machina/forum_base.html"
MACHINA_FORUM_NAME = "Intrepid Owners Portal"
MACHINA_MARKUP_LANGUAGE = ('markdown.markdown', {'safe_mode': 'remove'})
MACHINA_DEFAULT_AUTHENTICATED_USER_FORUM_PERMISSIONS = [
    'can_see_forum',
    'can_read_forum',
    'can_start_new_topics',
    'can_reply_to_topics',
    'can_edit_own_posts',
    'can_delete_own_posts',
    'can_post_without_approval',
    'can_create_polls',
    'can_vote_in_polls',
    'can_attach_file',
    'can_download_file',
]

NO_REPLY_EMAIL = "no-reply@intrepidpowerboats.com"

TO_EMAIL = {
    "REGISTRATION_FORM": [
        'admin@localhost',
    ],
    "OPTIONAL_EQUIPMENT_TAB_FORM": [
        'admin@localhost',
    ],
    "EMPLOYMENT_PAGE_FORM": [
        'admin@localhost',
    ],
    "CONTACT_US_FORM": [
        'admin@localhost',
    ],
    "OWNERS_PORTAL_FEEDBACK_FORM": [
        'admin@localhost',
    ],
    "TESTIMONIAL_SHARE": [
        'admin@localhost',
    ],
    "BUILD_A_BOAT_SHARE": [
        'admin@localhost',
    ],
    "NEWSLETTER_FORM": [
        'admin@localhost',
    ],
    "POST_SUBMISSION_NOTIFICATION": [
        'admin@localhost',
    ],
}

BUILD_A_BOAT = {
    "NO_REPLY_EMAIL": NO_REPLY_EMAIL,
    "NO_REPLY_EMAIL_REPORTS": NO_REPLY_EMAIL,
    "SALES_CONTACT": TO_EMAIL['BUILD_A_BOAT_SHARE']
}

# About tab in Model page
THUMBNAILS_PER_PAGE = 5

FACEBOOK_APP_ID = env("FACEBOOK_APP_ID", default="")
# Contact email addresses
INQUIRY_EMAIL_ADDRESS = TO_EMAIL['CONTACT_US_FORM']
BOAT_INFORMATION_EMAIL_ADDRESS = TO_EMAIL['CONTACT_US_FORM']
SALES_EMAIL_ADDRESS = TO_EMAIL['CONTACT_US_FORM']

# Authentication

LOGIN_URL = 'common:login'
LOGOUT_REDIRECT_URL = 'common:home'
LOGIN_REDIRECT_URL = 'owners_portal:owners_portal'

# Compression

COMPRESS_ENABLED = False

CKEDITOR_CONFIGS = {
    'boat_steps': {
        'toolbar': 'Basic',
    },
    'boat_steps_inline': {
        'toolbar': 'Basic',
        'height': 300,
        'width': 300,
    },
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Styles'],
            ['Format'],
            ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat'],
            ['TextColor', 'BGColor'],
            ['Undo', 'Redo'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule', 'SpecialChar'],
            ['Source']
        ],
        'width': 900,
        'toolbarCanCollapse': True,
    },
}

# Thumbnails
THUMBNAIL_ALIASES = {
    '': {
        'pager-item': {'size': (98, 98), 'crop': 'center', 'upscale': True, 'degrees': 0},
        'owners-gallery': {'size': (400, 400), 'crop': 'smart', 'upscale': True, 'degrees': 0},
        'testimonial': {'size': (420, 300), 'crop': 'smart', 'upscale': True, 'degrees': 0},
        'video': {'size': (365, 345), 'crop': 'smart', 'upscale': True, 'degrees': 0},
        'mobile': {'size': (767, 0), 'scale_and_crop': 'scale', 'degrees': 0},
        'mobile-rotate': {'size': (767, 0), 'scale_and_crop': 'scale', 'degrees': 90},
        'profile-picture': {'size': (206, 206), 'crop': 'smart', 'upscale': True, 'degrees': 0},
        'header': {'size': (1280, 256), 'crop': 'smart', 'upscale': True, 'degrees': 0},
    },
}

THUMBNAIL_BASEDIR = 'easy-thumbnails'

VIMEO_API_REQUEST_LIMIT = 10

NORECAPTCHA_SECRET_KEY = '6LcNNiUUAAAAAEQ3ejnIKFsh-LbYAb_P_akoe-IQ'
NORECAPTCHA_SITE_KEY = '6LcNNiUUAAAAAH8zve9-IzDfQ5UHLCoWqBv2_ln3'
