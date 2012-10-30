# Copy this file to settings.py.
from settings_default import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'STORAGE_ENGINE': 'InnoDB',
        'NAME': 'example1',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Site
DOMAIN_NAME = 'www.example.com'
SITE_NAME = 'www.example.com'
