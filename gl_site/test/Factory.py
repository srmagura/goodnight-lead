# gl_site models
from gl_site.models import Organization, Session, LeadUserInfo

# Django User
from django.contrib.auth.models import User

class Callable:
    """ Callable object, similar to static method """
    def __init__(self, anycallable):
        self.__call__ = anycallable

class Factory:
    """ Factory class for creating commonly used objects in testing """

    index = 0
    defaultPassword = 'password'

    def incrementIndex():
        """ Increment the factory index. Guarantees uniqueness. """
        Factory.index = Factory.index + 1
    incrementIndex = Callable(incrementIndex)

    def createOrganization(created_by):
        """ Create an organization and set the creating user """
        org = Organization.objects.create(
            name = "Test Organization {}".format(Factory.index),
            code = "Secret {}".format(Factory.index),
            created_by = created_by
        )
        Factory.incrementIndex()
        return org
    createOrganization = Callable(createOrganization)

    def createSession(organization, created_by):
        """ Create a session and set the organization and creating user """

        session = Session.objects.create(
            name = "Test Session {}".format(Factory.index),
            organization = organization,
            created_by = created_by
        )
        Factory.incrementIndex()
        return session
    createSession = Callable(createSession)

    def createDemographics(user, organization, session):
        """ Create user demographics and link to user, org, and session """

        info = LeadUserInfo.objects.create(
            user = user,
            gender = 'M',
            major = 'Tester',
            year = 1,
            organization = organization,
            session = session
        )
        Factory.incrementIndex()
        return info
    createDemographics = Callable(createDemographics)

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
    createUser = Callable(createUser)

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
            'year': leaduserinfo.year,
        }
    createUserSettingsPostDict = Callable(createUserSettingsPostDict)
