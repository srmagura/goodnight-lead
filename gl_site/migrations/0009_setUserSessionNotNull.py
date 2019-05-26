# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0008_addSessionIDToUserInfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaduserinfo',
            name='session',
            field=models.ForeignKey(default=1, to='gl_site.Session', on_delete=models.PROTECT),
        ),
    ]
