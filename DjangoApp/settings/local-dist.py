# -*- mode: python; coding: utf-8; -*-
"""
This is an example settings/local.py file.
These settings overrides what's in settings/base.py
"""

import logging

# To extend any settings from settings/base.py here's an example:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'fiber_example',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Kiev'

# Debugging displays nice error messages, but leaks memory. Set this to False
# on all server instances and True only for development.
DEBUG = True
TEMPLATE_DEBUG = True

# Is this a development instance? Set this to True on development/master
# instances and False on stage/prod.
DEV = False

#from . import base
#INSTALLED_APPS = base.INSTALLED_APPS + ['debug_toolbar']
#INTERNAL_IPS = ('127.0.0.1',)
# DEBUG_TOOLBAR_PANELS = (
#     'debug_toolbar.panels.version.VersionDebugPanel',
#     'debug_toolbar.panels.timer.TimerDebugPanel',
#     'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#     'debug_toolbar.panels.headers.HeaderDebugPanel',
#     'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#     'debug_toolbar.panels.template.TemplateDebugPanel',
#     'debug_toolbar.panels.sql.SQLDebugPanel',
#     'debug_toolbar.panels.cache.CacheDebugPanel',
#     'debug_toolbar.panels.logger.LoggingPanel',
# )
#MIDDLEWARE_CLASSES = base.MIDDLEWARE_CLASSES + (
#  'debug_toolbar.middleware.DebugToolbarMiddleware',
#)


# Make this unique, and don't share it with anybody.  It cannot be blank.
SECRET_KEY = 'u-wgm$x77mabbfhs9b!1w_2d3@@6egjia4wpz$smjl#kv-vjl!'

##USE_X_FORWARDED_HOST = False
