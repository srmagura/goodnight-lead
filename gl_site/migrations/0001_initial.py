# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_id', models.IntegerField()),
                ('content', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='LeadUserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female'), (b'O', b'Other'), (b'N', b'Prefer not to respond')])),
                ('major', models.CharField(max_length=100)),
                ('year', models.IntegerField(choices=[(1, b'Freshman'), (2, b'Sophmore'), (3, b'Junior'), (4, b'Senior')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)])),
                ('organization', models.CharField(max_length=100, choices=[(b'gsp', b'Goodnight Scholars Program')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Metric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=50)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('inventory_id', models.IntegerField()),
                ('current_page', models.IntegerField(default=None, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.AddField(
            model_name='metric',
            name='submission',
            field=models.ForeignKey(to='gl_site.Submission', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='answer',
            name='submission',
            field=models.ForeignKey(to='gl_site.Submission', on_delete=models.CASCADE),
        ),
    ]
