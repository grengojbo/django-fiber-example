# -*- mode: python; coding: utf-8; -*-
"""
This is your project's main settings file that can be committed to your
repo. If you need to override a setting locally, use local.py
"""

import django
import os
import sys
import logging
#import django.conf.global_settings as DEFAULT_SETTINGS
#import memcache_toolbar.panels.memcache

# Your project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + "../../../")

PYTHON_VERSION = '%s.%s' % sys.version_info[:2]
DJANGO_VERSION = django.get_version()
#path = lambda *a: os.path.join(ROOT, *a)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

SUPPORTED_NONLOCALES = ['media', 'admin', 'static']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru-ru'

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
# Example: "/home/media/media.example.com/media/"
MEDIA_ROOT = FILEBROWSER_MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.example.com/media/", "http://example.com/media/"
MEDIA_URL = FILEBROWSER_MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.example.com/static/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public/static')

# URL prefix for static files.
# Example: "http://media.example.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    'static',
    )

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
#)
TEMPLATE_LOADERS = (
   ('django.template.loaders.cached.Loader', (
       'django.template.loaders.filesystem.Loader',
       'django.template.loaders.app_directories.Loader',
       'django.template.loaders.eggs.Loader',
   )),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u-wgm$x77mabbfhs9b!1w_2d3@@6egjia4wpz$smjl#kv-vjl!'


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'south',
    'mptt',
    'compressor',
    'fiber',
    'rest_framework',
    'modeltranslation',
    'fiber_modeltranslation'
]

MIDDLEWARE_CLASSES = (
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'fiber.middleware.ObfuscateEmailAddressMiddleware',
    'fiber.middleware.AdminPageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'DjangoApp.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'DjangoApp.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.csrf',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or
    # "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates'),
    )

# List of callables that know how to import templates from various sources.

FIXTURE_DIRS = (
    os.path.join(PROJECT_ROOT, 'fixtures'),
    )

gettext = lambda s: s

LANGUAGES = (
    ('en', gettext('English')),
    #('fr', gettext('French')),
    #('es', gettext('Spanish')),
    #('pt', gettext('Portuguese')),
    #('de', gettext('German')),
    ('ru', gettext('Russian')),
    ('uk', gettext('Ukraine')),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'ru'
#MODELTRANSLATION_TRANSLATION_REGISTRY = 'DjangoApp.translation'
# Specify a model to use for user profiles, if desired.
#AUTH_PROFILE_MODULE = 'DjangoApp.accounts.UserProfile'

FILE_UPLOAD_PERMISSIONS = 0664

SOUTH_TESTS_MIGRATE = False

APPEND_SLASH = False

API_RENDER_HTML = False
FIBER_TEMPLATE_CHOICES = (
    ('', 'Default template'),
    ('tpl-home.html', 'Home template'),
    ('tpl-page.html', 'With other page template'),
)
FIBER_CONTENT_TEMPLATE_CHOICES = (
   ('', 'Default template'),
   ('special-content-template.html', 'Special template'),
)
FIBER_METADATA_CONTENT_SCHEMA = FIBER_METADATA_PAGE_SCHEMA = {
    'title': {
        'widget': 'select',
        'values': ['option1', 'option2', 'option3',],
    },
    'bgcolor': {
        'widget': 'combobox',
        'values': ['#ffffff', '#fff000', '#ff00cc'],
        'prefill_from_db': True,
    },
    'description': {
        'widget': 'textarea',
    },
}

#REST_FRAMEWORK = {
#    #'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAdminUser',),
#    'FILTER_BACKEND': 'rest_framework.filters.DjangoFilterBackend',
#    'PAGINATE_BY': 50
#}

# Django extensions
try:
    import django_extensions
except ImportError:
    pass
else:
    INSTALLED_APPS = INSTALLED_APPS + ['django_extensions']

try:
    import gunicorn
except ImportError:
    pass
else:
    INSTALLED_APPS = INSTALLED_APPS + ('gunicorn')

# Add the Guardian and userena authentication backends
AUTHENTICATION_BACKENDS = (
    #'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Needed for Django guardian
ANONYMOUS_USER_ID = -1

## Log settings

LOG_LEVEL = logging.INFO
LOG_COLORSQL_ENABLE = True
LOG_COLORSQL_VERBOSE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


