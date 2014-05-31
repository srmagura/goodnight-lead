from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

#Additional user info which extends the django User class using a one-to-one relationship.
#Saved in the app_leaduserinfo db
#Access through user.leaduserinfo
class LeadUserInfo(models.Model):
    #Linked User
    user = models.OneToOneField(User)
    
    #Additional fields
    gender = models.CharField(max_length=1)
    major = models.CharField(max_length=100)
    year = models.IntegerField(max_length=2, validators=[MinValueValidator(1), MaxValueValidator(4)])
    organization = models.CharField(max_length=100)
    #Goals?