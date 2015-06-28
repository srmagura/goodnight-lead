# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings

def setOrganizationCreatedBy(apps, schema_editor):
    """ Set the creating user for the default organization """

    Organization = apps.get_model("gl_site", "Organization")
    User = apps.get_model("auth", "User")

    org = Organization.objects.get(name='Default')
    org.created_by = User.objects.get(username='DefaultAdmin')
    org.save()

class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gl_site', '0005_addOrganizationSessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.RunPython(
            setOrganizationCreatedBy
        ),
    ]
