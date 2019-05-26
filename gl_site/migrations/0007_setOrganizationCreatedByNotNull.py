# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0006_addCreatedByToOrganizations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT),
        ),
    ]
