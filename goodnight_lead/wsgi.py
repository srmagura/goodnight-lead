import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goodnight_lead.settings.production')

application = Cling(get_wsgi_application())
