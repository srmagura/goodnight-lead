from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

#Additional user info which extends the django User class using a one-to-one relationship.
#Saved in the app_leaduserinfo table
#Access through user.leaduserinfo
class LeadUserInfo(models.Model):
    #Linked User
    user = models.OneToOneField(User)

    #Additional fields
    gender_choices = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Prefer not to respond'),
    )
    gender = models.CharField(max_length=1, choices=gender_choices)

    major = models.CharField(max_length=100)

    year_choices = (
        (1, 'Freshman'),
        (2, 'Sophmore'),
        (3, 'Junior'),
        (4, 'Senior'),
    )
    year = models.IntegerField(choices=year_choices, validators=[MinValueValidator(1), MaxValueValidator(4)])

    #shortname -> fullname
    organization_choices = (
        ('gsp', 'Goodnight Scholars Program'),
    )
    organization = models.CharField(max_length=100, choices=organization_choices)

class Submission(models.Model):
    user = models.ForeignKey(User)
    inventory_id = models.IntegerField()
    current_page = models.IntegerField(default=None, null=True)

    def is_complete(self):
        return self.current_page is None

class Answer(models.Model):
    submission = models.ForeignKey(Submission)
    question_id = models.IntegerField()
    content = models.CharField(max_length=1000)

class Metric(models.Model):
    submission = models.ForeignKey(Submission)
    key = models.CharField(max_length=50)
    value = models.FloatField()