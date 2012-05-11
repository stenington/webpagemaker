# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

from funfactory.settings_base import *

# Defines the views served for root URLs.
ROOT_URLCONF = 'webpagemaker.urls'

INSTALLED_APPS = list(INSTALLED_APPS) + [
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    
    # Application base, containing global templates.
    'webpagemaker.base',
    'webpagemaker.api',
    'webpagemaker.website',
    'webpagemaker.learning_projects',
]

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'django.core.context_processors.static',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

STATIC_URL = "/s/"

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
    # Mission development API (debug only)
    'mission-slurp'
]

# Maximum size, in bytes, of published pages. Note that if you change this
# from its default, you may need to modify your database, since this
# setting's value is used in schema generation.
MAX_PUBLISHED_PAGE_SIZE = 10000

# Where to retrieve in-development learning projects from. Only
# consulted if settings.DEV is True.
LEARNING_PROJECTS_URL = 'http://wpm-dropbox.toolness.org/'

ADMIN_MEDIA_PREFIX = '/media/admin/'
