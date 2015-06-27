# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gl_site', '0004_addOrganizationForeignKeyToUser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=120, unique=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('uuid', models.CharField(max_length=32, unique=True)),
                ('created_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(to='gl_site.Organization')),
            ],
        ),
        migrations.AlterField(
            model_name='leaduserinfo',
            name='gender',
            field=models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other'), ('N', 'Prefer not to respond')]),
        ),
        migrations.AlterField(
            model_name='leaduserinfo',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4)], choices=[(1, 'Freshman'), (2, 'Sophmore'), (3, 'Junior'), (4, 'Senior')]),
        ),
    ]
