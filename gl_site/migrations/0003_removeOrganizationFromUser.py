# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0002_createOrganizations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leaduserinfo',
            name='organization',
        ),
    ]
