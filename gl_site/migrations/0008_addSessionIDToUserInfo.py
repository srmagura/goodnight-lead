# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0007_setOrganizationCreatedByNotNull'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaduserinfo',
            name='session',
            field=models.ForeignKey(null=True, to='gl_site.Session', on_delete=models.PROTECT),
        ),
    ]
