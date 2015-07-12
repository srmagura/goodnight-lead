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

    BUSINESS = 'Business'
    EDUCATION = 'Education'
    ENGINEERING = 'Engineering'
    DESIGN = 'Design and Fine Arts'
    HUMANITIES = 'Humanities'
    LAW = 'Law'
    LIFE_SCIENCE = 'Life Sciences'
    MATH = 'Math and Physical Sciences'
    MEDICINE = 'Medicine'
    SOCIAL_SCIENCE = 'Social Sciences'
    HEALTH = 'Health'
    APPLIED_FIELDS = 'Applied Fields'
    OTHER = 'Other'

    # User major / career field
    major_choices = (
        (BUSINESS, BUSINESS),
        (EDUCATION, EDUCATION),
        (ENGINEERING, ENGINEERING),
        (DESIGN, DESIGN),
        (HUMANITIES, HUMANITIES),
        (LAW, LAW),
        (LIFE_SCIENCE, LIFE_SCIENCE),
        (MATH, MATH),
        (MEDICINE, MEDICINE),
        (SOCIAL_SCIENCE, SOCIAL_SCIENCE),
        (HEALTH, HEALTH),
        (APPLIED_FIELDS, APPLIED_FIELDS),
        (OTHER, OTHER)
    )
    major = models.CharField('Major / Career', max_length=100, choices = major_choices)

    # User education level
    HIGH_SCHOOL = ('HS', 'High School')
    FRESHMAN = ('FR', 'Undergraduate - Freshman')
    SOPHMORE = ('SO', 'Undergraduate - Sophmore')
    JUNIOR = ('JU', 'Undergraduate - Junior')
    SENIOR = ('SE', 'Undergraduate - Senior')
    GRADUATE_SCHOOL = ('GS', 'Graduate School')
    GRADUATED = ('GR', 'Graduated')
    education_choices = (
        HIGH_SCHOOL,
        FRESHMAN,
        SOPHMORE,
        JUNIOR,
        SENIOR,
        GRADUATE_SCHOOL,
        GRADUATED
    )
    education = models.CharField(max_length = 2, choices = education_choices)

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
