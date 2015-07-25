from django.db import models, migrations
from django.core.management import call_command

def load_default_dashboard_text(apps, schema_editor):
    call_command('loaddata', 'default_dashboard_text.json')

class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0014_dashboardtext'),
    ]

    operations = [
        migrations.RunPython(load_default_dashboard_text)
    ]
