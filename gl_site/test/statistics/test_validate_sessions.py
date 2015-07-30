# Import the validate_sessions function
from gl_site.statistics.data_generation import validate_sessions

# Test imports
from django.test import TestCase
from gl_site.test.factory import Factory

# Models
from gl_site.models import Session

class TestValidateSession(TestCase):
    """ Test class for validate_sessions """

    def setUp(self):
        """ Create variables for testing """

        # Create a user to be used for testing
        self.user, self.info = Factory.create_user()
        Factory.create_session(self.info.organization, self.user)

        # Create some organizations and sessions
        self.org1 = Factory.create_organization(self.user)
        self.session1 = Factory.create_session(self.org1, self.user)

    def test_organization_is_invalid(self):
        """ A non staff user cannot request sessions they do not belong to """

        try:
            validate_sessions(self.org1, self.session1, self.user)
            self.fail('Validate sessions should throw an exception')
        except LookupError:
            pass

    def test_organization_is_none_session_is_none(self):
        """ Validate sessions returns all viewable sessions.
            For staff, this is all sessions. For non staff this
            is all sessions in the organization to which they belong.
        """

        # Non staff
        sessions = validate_sessions(None, None, self.user)

        for session in Session.objects.filter(organization=self.info.organization):
            self.assertIn(session, sessions)

        # Staff
        self.user.is_staff = True
        self.user.save()

        sessions = validate_sessions(None, None, self.user)

        for session in Session.objects.all():
            self.assertIn(session, sessions)

    def test_organization_is_defined_session_is_none(self):
        """ Validate sessions returns all sessions in the organization. """

        # Non staff
        sessions = validate_sessions(self.info.organization, None, self.user)

        for session in Session.objects.filter(organization=self.info.organization):
            self.assertIn(session, sessions)

        # Staff
        self.user.is_staff = True
        self.user.save()

        sessions = validate_sessions(self.org1, None, self.user)

        for session in Session.objects.filter(organization=self.org1):
            self.assertIn(session, sessions)

    def test_organization_is_defined_session_invalid(self):
        """ Selecting a session not in the organization raises an exception """

        try:
            validate_sessions(self.info.organization, self.session1, self.user)
            self.fail('Validate sessions should have raised an exception')
        except LookupError:
            pass

    def test_organization_is_defined_session_is_defined(self):
        """ Valid definitions returns a list containing the session """

        sessions = validate_sessions(self.info.organization, self.info.session, self.user)

        self.assertEqual(1, len(sessions), 'There is only one session')
        self.assertEqual(self.info.session, sessions[0])
