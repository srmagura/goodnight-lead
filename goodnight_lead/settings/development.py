"""LEAD development settings."""


# Imports
import dj_database_url

from goodnight_lead.settings.common import *


# Enable debug mode
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True


# Define a secret key for development
SECRET_KEY = 'q(1n%=3@_7q-1fsqfvgbyjou_wsnm6t_@xahz3=i0fnnl&*hs='


# Allow all host headers
ALLOWED_HOSTS = ['*']


# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://gl_dev:pw@localhost/goodnight_lead'
    )
}

