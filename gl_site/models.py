from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Import for providing sessions uuids
from uuid import uuid1

class Organization(models.Model):
    """ Organization affiliated with each user.
        Each user shares a many to one relationship
        with an organization for purposes of
        demographics and statistics.
    """

    # Organization name
    name = models.CharField(max_length=120, unique=True)

    # Entry code for selective approval
    code = models.CharField(max_length=120)

    # Date of organization creation for record keeping
    creation_date = models.DateField(auto_now_add=True)

    # Creating user
    created_by = models.ForeignKey(User)

    def __str__(self):
        return self.name

class Session(models.Model):
    """ Organization session affiliated with each user.
        Each organization may have multiple sessions,
        allowing them to hold separate Lead Labs and
        compare groups in a meaningful way.
    """

    # Session name
    name = models.CharField(max_length=120, unique=True)

    # The creating user of a session
    created_by = models.ForeignKey(User)

    # Date of creation for record keeping
    creation_date = models.DateField(auto_now_add=True)

    # Organization associated with this session
    organization = models.ForeignKey(Organization)

    # Universally unique identifier, stored as hex.
    # Used for generating session registration urls.
    uuid = models.CharField(max_length=32, unique = True)

    def save(self, *args, **kwargs):
        """
        Override the default save to set uuid. There's no chance of a uuid
        collision under the uuid1 standard.
        """
        # Set uuid in hex if the session has not yet been saved
        if self.id is None:
            self.uuid = uuid1().hex

        # Call super save method
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class LeadUserInfo(models.Model):
    """ Additional user info which extends the django User
        class using a one-to-one relationship.
        Saved in the app_leaduserinfo table
        Access through user.leaduserinfo
    """

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

    # User graduation date
    graduation_date = models.DateField()

    # Foreign key linking to an organization
    organization = models.ForeignKey(Organization)

    # Foreign key linking to a session
    session = models.ForeignKey(Session)

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
