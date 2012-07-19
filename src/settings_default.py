import os

import django.conf.global_settings as DEFAULT_SETTINGS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Michael van de Waeter', 'mvandewaeter@leukeleu.nl'),
)

MANAGERS = ADMINS

DATABASES = {}

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media', '')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static', '')
STATIC_URL = '/static/'

STATICFILES_DIRS = ()
STATICFILES_FINDERS = DEFAULT_SETTINGS.STATICFILES_FINDERS + (
    'compressor.finders.CompressorFinder',
)

SECRET_KEY = '!#1$1eyh5tvs74542b%$x*ht16n+ho6xc1v*5b$z-s)8h4xnrd'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = DEFAULT_SETTINGS.MIDDLEWARE_CLASSES + (
    'fiber.middleware.ObfuscateEmailAddressMiddleware',
    'fiber.middleware.AdminPageMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = ()

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

WSGI_APPLICATION = 'wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    # Project apps
    'project',
    'project.pages',

    # Generic apps
    'compressor',
    'fiber',
    'mptt',
    'djangorestframework',
    'south',
)

# Site
DOMAIN_NAME = 'www.example.com'
SITE_NAME = 'www.example.com'

# Fiber
IMAGES_DIR = 'uploads/images'
FILES_DIR = 'uploads/files'

FIBER_DEFAULT_TEMPLATE = 'base.html'

FIBER_TEMPLATE_CHOICES = [
    ('', 'Default'),
]

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
