# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def move_major_to_current_choices(apps, schema_editor):
    """ Migrate all users from their current major to one of the default choices """

    # Get the demographics objects
    LeadUserInfo = apps.get_model('gl_site', 'LeadUserInfo')
    demographics = LeadUserInfo.objects.all()

    # List of majors to be migrated from prod.
    choices = {
        'Engineering': (
            'Computer Science',
            'Mechanical Engineering',
            'B.S. Nuclear Engineering',
            'Polymer and Color Chemistry',
            'Chemistry (BS)',
            'Biochemistry',
            'Chemical Engineering ',
            'Chemical Engineering',
            'Biological Engineering - Environmental Concentration',
            'Chemistry',
            'Civil Engineering',
            'Electrical and Computer Engineering',
            'Biomedical Engineering',
            'Industrial Engineering',
        ),
        'Life Sciences': (
            'Human Biology',
            'Biology',
            'Genetics',
            'Horticulture',
            'Poultry Science '
        ),
        'Math and Physical Sciences': (
            'Statistics ',
            'Physics',
        ),
        'Medicine': (
            'Psychology',
        ),
        'Health': (
            'Outdoor Leadership',
        ),
    }

    # Iterate ver all demographcis
    for demographic in demographics:
        # Iterate over all choices
        match = False
        for key, value in choices.items():
            # If the correct field is foud, update, save
            # and move on to the next user
            if demographic.major in choices[key]:
                demographic.major = key
                demographic.save()
                match = True
                break
        # No matching choice was found for the user, set default.
        if not match:
            demographic.major = 'Other'
            demographic.save()

class Migration(migrations.Migration):

    dependencies = [
        ('gl_site', '0011_addExpandedEducationChoices'),
    ]

    operations = [
        migrations.RunPython(
            move_major_to_current_choices
        ),
        migrations.AlterField(
            model_name='LeadUserInfo',
            name='major',
            field=models.CharField(choices=[('Business', 'Business'), ('Education', 'Education'), ('Engineering', 'Engineering'), ('Design and Fine Arts', 'Design and Fine Arts'), ('Humanities', 'Humanities'), ('Law', 'Law'), ('Life Sciences', 'Life Sciences'), ('Math and Physical Sciences', 'Math and Physical Sciences'), ('Medicine', 'Medicine'), ('Social Sciences', 'Social Sciences'), ('Health', 'Health'), ('Applied Fields', 'Applied Fields'), ('Other', 'Other')], max_length=100, verbose_name='Major / Career'),
        ),
    ]
