# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def createDefaultOrganization(apps, schema_editor):
    """ Custom migration command to create a default organization """

    # Get the historical version of the Organization model
    # that existed at this migration.
    Organization = apps.get_model("gl_site", "Organization")

    # Create a default organization
    Organization.objects.create(
        name="Default",
        code="public",
    )

class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=120)),
                ('code', models.CharField(max_length=120)),
                ('creation_date', models.DateField(auto_now_add=True)),
            ],
        ),

        migrations.RunPython(
            createDefaultOrganization
        ),
    ]
