from django.db import models, migrations
from django.core.management import call_command
from io import StringIO

def load_default_dashboard_text(apps, schema_editor):
    # Specify stdout so that loaddata doesn't pollute the console
    buffer = StringIO()
    call_command('loaddata', 'default_dashboard_text.json', stdout=buffer)

class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0014_dashboardtext'),
    ]

    operations = [
        migrations.RunPython(load_default_dashboard_text)
    ]
