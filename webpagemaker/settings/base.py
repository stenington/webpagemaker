# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *
from funfactory.manage import path

# Defines the views served for root URLs.
ROOT_URLCONF = 'webpagemaker.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django.contrib.messages',
    'django.contrib.admin',
    
    # Application base, containing global templates.
    'webpagemaker.base',
    'webpagemaker.api',
    'webpagemaker.website',
    'webpagemaker.learning_projects',
]

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

LOGGING = dict(loggers=dict(playdoh = {'level': logging.DEBUG}))

# Webpagemaker API settings

SUPPORTED_NONLOCALES = list(SUPPORTED_NONLOCALES) + [
    # The API endpoint
    'api',
    # Published pages
    'p',
    # Static resources for learning projects
    's',
    # static resources for in-development learning projects
    'sd',
    # Mission development API (debug only)
    'mission-slurp'
]

# Maximum size, in bytes, of published pages. Note that if you change this
# from its default, you may need to modify your database, since this
# setting's value is used in schema generation.
MAX_PUBLISHED_PAGE_SIZE = 10000

# Where to retrieve in-development learning projects from. Only
# consulted if settings.DEV is True.
LEARNING_PROJECTS_DROPBOX_URL = 'http://wpm-dropbox.toolness.org/'

# Where to serve static resources for learning projects from, relative to
# server root. Note that this also needs to be present in
# SUPPORTED_NONLOCALES.
LEARNING_PROJECTS_STATIC_URL = '/s/'

# Root directory to serve learning project static resources from when
# in debug mode.
LEARNING_PROJECTS_STATIC_ROOT = path('webpagemaker/learning_projects/static')

# Use our symlink for the admin media.
ADMIN_MEDIA_PREFIX = '/media/admin/'
