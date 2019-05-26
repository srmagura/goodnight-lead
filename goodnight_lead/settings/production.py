"""LEAD production settings."""


# Imports
import os

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

from goodnight_lead.settings.common import *


# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False


# Get secret key
SECRET_KEY = os.getenv('GOODNIGHT_LEAD_SECRET_KEY')
if not SECRET_KEY:
    raise ImproperlyConfigured(
        'GOODNIGHT_LEAD_SECRET_KEY must be set when not in debug mode.'
    )


ALLOWED_HOSTS = ['.herokuapp.com']


# Always redirect to use https
SECURE_SSL_REDIRECT = True


# Parse database configuration from $DATABASE_URL
DATABASES = {'default': dj_database_url.config()}


