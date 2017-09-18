# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0016_sessionNameUniqueWithinOrg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaduserinfo',
            name='graduation_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
