# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0015_defaultDashboardText'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardtext',
            name='about_panel_contents',
            field=ckeditor.fields.RichTextField(help_text='Note: uploading images to the server is not currently supported. If you want to insert an image that is hosted elsewhere on the web, you can do so by copying its URL into image insert dialog.'),
        ),
        migrations.AlterField(
            model_name='dashboardtext',
            name='about_panel_title',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='session',
            name='name',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterUniqueTogether(
            name='session',
            unique_together=set([('name', 'organization')]),
        ),
    ]
