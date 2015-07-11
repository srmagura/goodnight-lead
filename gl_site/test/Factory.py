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

    @staticmethod
    def incrementIndex():
        """ Increment the factory index. Guarantees uniqueness. """
        Factory.index = Factory.index + 1

    @staticmethod
    def createOrganization(created_by):
        """ Create an organization and set the creating user """

        org = Organization.objects.create(
            name = "Test Organization {}".format(Factory.index),
            code = "Secret {}".format(Factory.index),
            created_by = created_by
        )
        Factory.incrementIndex()
        return org

    @staticmethod
    def createSession(organization, created_by):
        """ Create a session and set the organization and creating user """

        session = Session.objects.create(
            name = "Test Session {}".format(Factory.index),
            organization = organization,
            created_by = created_by
        )
        Factory.incrementIndex()
        return session

    @staticmethod
    def createDemographics(user, organization, session):
        """ Create user demographics and link to user, org, and session """

        info = LeadUserInfo.objects.create(
            user = user,
            gender = 'M',
            major = LeadUserInfo.OTHER,
            education = 'FR',
            graduation_date = date.today(),
            organization = organization,
            session = session
        )
        Factory.incrementIndex()
        return info

    @staticmethod
    def createUser():
        """ Create a default user """

        user = User.objects.create_user(
            username = "testuser{}".format(Factory.index),
            email = "testuser{}@gmail.com".format(Factory.index),
            password = Factory.defaultPassword,
            first_name = "test{}".format(Factory.index),
            last_name = "user{}".format(Factory.index)
        )
        Factory.incrementIndex()
        return user

    @staticmethod
    def createUserSettingsPostDict(user, leaduserinfo):
        """ Create the dictionary sent through post for account settings """

        return {
            # User fields
            'username': user.username,
            'email': user.email,
            'password': Factory.defaultPassword,
            'first_name': user.first_name,
            'last_name': user.last_name,

            # Info fields
            'gender': leaduserinfo.gender,
            'major': leaduserinfo.major,
            'education': leaduserinfo.education,
            'graduation_date': leaduserinfo.graduation_date,
        }

    @staticmethod
    def createUserRegistrationPostDict(organization):
        """ Create a registration dict
            Returns a registration dictionary with unique
            user information where applicable.
        """

        form =  {
            # User fields
            'username' : "testuser{}".format(Factory.index),
            'email' : "testuser{}@gmail.com".format(Factory.index),
            'password1' : Factory.defaultPassword,
            'password2' : Factory.defaultPassword,
            'first_name' : "test{}".format(Factory.index),
            'last_name' : "user{}".format(Factory.index),

            # Info fields
            'gender': 'M',
            'major': LeadUserInfo.OTHER,
            'education': 'FR',
            'graduation_date' : str(date.today()),
            'organization_code' : organization.code
        }
        Factory.incrementIndex()
        return form
