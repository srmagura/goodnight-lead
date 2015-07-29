# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0013_siteconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='DashboardText',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('inventory_desc', models.TextField()),
                ('mental_health_warning', models.TextField()),
                ('about_panel_title', models.TextField()),
                ('about_panel_contents', ckeditor.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'Dashboard text',
                'verbose_name_plural': 'Dashboard text',
            },
        ),
    ]
