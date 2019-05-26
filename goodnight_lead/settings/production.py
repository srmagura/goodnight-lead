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


# Security settings
SECURE_HSTS_SECONDS = 31536000  # 1 year (in seconds)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Parse database configuration from $DATABASE_URL
DATABASES = {'default': dj_database_url.config()}


