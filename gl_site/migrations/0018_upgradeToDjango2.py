# Generated by Django 2.2.1 on 2019-05-26 19:47
# Note: This was auto generated as a result of upgrading to Django >= 2.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0017_makeGradDateOptional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaduserinfo',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Self-Identify'), ('N', 'Prefer not to respond')], max_length=1),
        ),
    ]
