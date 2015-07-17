# gl_site models
from gl_site.models import Organization, Session, LeadUserInfo

# Django User
from django.contrib.auth.models import User

# Date utilities
from datetime import date

class Factory:
    """ Factory class for creating commonly used objects in testing """

    index = 0
    defaultPassword = 'password'

    @classmethod
    def increment_index(cls):
        """ Increment the factory index. Guarantees uniqueness. """
        cls.index = cls.index + 1

    @classmethod
    def create_organization(cls, created_by):
        """ Create an organization and set the creating user """

        org = Organization.objects.create(
            name = "Test Organization {}".format(cls.index),
            code = "Secret {}".format(cls.index),
            created_by = created_by
        )
        cls.increment_index()
        return org

    @classmethod
    def create_session(cls, organization, created_by):
        """ Create a session and set the organization and creating user """

        session = Session.objects.create(
            name = "Test Session {}".format(cls.index),
            organization = organization,
            created_by = created_by
        )
        cls.increment_index()
        return session

    @classmethod
    def create_user(cls):
        """
        Create a default user, including its LeadUserInfo, Organization,
        and Session.
        """
        user = User.objects.create_user(
            username = "testuser{}".format(cls.index),
            email = "testuser{}@gmail.com".format(cls.index),
            password = cls.defaultPassword,
            first_name = "test{}".format(cls.index),
            last_name = "user{}".format(cls.index)
        )

        organization = cls.create_organization(user)
        session = cls.create_session(organization, user)

        info = LeadUserInfo.objects.create(
            user = user,
            gender = 'M',
            major = LeadUserInfo.OTHER,
            education = 'FR',
            graduation_date = date.today(),
            organization = organization,
            session = session
        )

        cls.increment_index()
        return (user, info)

    @classmethod
    def create_user_settings_post_dict(cls, user, leaduserinfo):
        """ Create the dictionary sent through post for account settings """

        return {
            # User fields
            'username': user.username,
            'email': user.email,
            'password': cls.defaultPassword,
            'first_name': user.first_name,
            'last_name': user.last_name,

            # Info fields
            'gender': leaduserinfo.gender,
            'major': leaduserinfo.major,
            'education': leaduserinfo.education,
            'graduation_date': leaduserinfo.graduation_date,
        }

    @classmethod
    def create_user_registration_post_dict(cls, organization):
        """ Create a registration dict
            Returns a registration dictionary with unique
            user information where applicable.
        """

        form =  {
            # User fields
            'username' : "testuser{}".format(cls.index),
            'email' : "testuser{}@gmail.com".format(cls.index),
            'password1' : cls.defaultPassword,
            'password2' : cls.defaultPassword,
            'first_name' : "test{}".format(cls.index),
            'last_name' : "user{}".format(cls.index),

            # Info fields
            'gender': 'M',
            'major': LeadUserInfo.OTHER,
            'education': 'FR',
            'graduation_date' : str(date.today()),
            'organization_code' : organization.code
        }
        cls.increment_index()
        return form
