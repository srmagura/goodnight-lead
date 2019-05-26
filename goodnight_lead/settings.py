"""LEAD settings."""


# Imports
import os

import dj_database_url


# Project base directory
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q(1n%=3@_7q-1fsqfvgbyjou_wsnm6t_@xahz3=i0fnnl&*hs='


# SECURITY WARNING: don't run with debug turned on in production!
# Debug is set through environment variables for development.
# E.g. export GOODNIGHT_LEAD_DEBUG=1
# The default value is false if the env does not exist.
# Prod and test do not run in debug mode.
DEBUG = os.getenv('GOODNIGHT_LEAD_DEBUG', False)


# Allow all host headers
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'gl_site'
)

MIDDLEWARE = (

    # Security
    'django.middleware.security.SecurityMiddleware',

    # Whitenoise
    'whitenoise.middleware.WhiteNoiseMiddleware',

    # Other
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

)

ROOT_URLCONF = 'goodnight_lead.urls'

WSGI_APPLICATION = 'goodnight_lead.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(
        default='postgres://gl_dev:pw@localhost/goodnight_lead'
    )
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Always redirect to use https when not in DEBUG
SECURE_SSL_REDIRECT = not DEBUG

# Static asset configuration
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
PROJECT_DIR = os.path.dirname(__file__)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

# We don't currently support uploading images from ckeditor, but we still
# need to define this variable
CKEDITOR_UPLOAD_PATH = 'ckeditor_uploads/'

# Default url for login page (override django default)
LOGIN_URL = '/login'


# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': os.getenv('GOODNIGHT_LEAD_TEMPLATE_DEBUG', False),
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]