# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0010_migrateToUserGradDate'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaduserinfo',
            name='education',
            field=models.CharField(max_length=2, choices=[('HS', 'High School'), ('FR', 'Undergraduate - Freshman'), ('SO', 'Undergraduate - Sophmore'), ('JU', 'Undergraduate - Junior'), ('SE', 'Undergraduate - Senior'), ('GS', 'Graduate School'), ('GR', 'Graduated')], default='FR'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='leaduserinfo',
            name='session',
            field=models.ForeignKey(to='gl_site.Session'),
        ),
    ]
