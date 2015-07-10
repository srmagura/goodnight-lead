# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from datetime import date

def set_graduation_date(apps, schema_editor):
    """ Set the graduation date based on user creation and year """

    # Get all demographics objects
    LeadUserInfo = apps.get_model('gl_site', 'LeadUserInfo')
    demographics = LeadUserInfo.objects.all()

    # Iterate over all demographics to set grad date
    for demographic in demographics:
        join = demographic.user.date_joined
        demographic.graduation_date = date(join.year + 4, 5, 1)
        demographic.save()

class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0009_setUserSessionNotNull'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaduserinfo',
            name='graduation_date',
            field=models.DateField(null=True),
        ),
        migrations.RunPython(
            set_graduation_date
        ),
        migrations.AlterField(
            model_name='leaduserinfo',
            name='graduation_date',
            field=models.DateField(),
        ),
        migrations.RemoveField(
            model_name='leaduserinfo',
            name='year',
        )
    ]
