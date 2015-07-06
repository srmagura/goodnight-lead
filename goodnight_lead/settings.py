# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q(1n%=3@_7q-1fsqfvgbyjou_wsnm6t_@xahz3=i0fnnl&*hs='

# SECURITY WARNING: don't run with debug turned on in production!
# Debug is set through environment variables for development.
# The default value is false if the env does not exist.
# Prod and test do not run in debug mode.
DEBUG = os.getenv('GOODNIGHT_LEAD_DEBUG', False)

TEMPLATE_DEBUG = os.getenv('GOODNIGHT_LEAD_TEMPLATE_DEBUG', False)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gl_site'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'


# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES = {}
DATABASES['default'] = dj_database_url.config(default='postgres://gl_dev:pw@localhost/goodnight_lead')

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Always redirect to use https when not in DEBUG
SECURE_SSL_REDIRECT = not DEBUG

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
PROJECT_DIR = os.path.dirname(__file__)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

STATICFILES_DIRS = (os.path.join(BASE_DIR, '../static'),)

#Default url for login page (override django default)
LOGIN_URL = '/home'
