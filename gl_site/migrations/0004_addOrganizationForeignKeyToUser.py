# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0003_removeOrganizationFromUser'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaduserinfo',
            name='organization',
            field=models.ForeignKey(default=1, to='gl_site.Organization'),
            preserve_default=False,
        ),
    ]
