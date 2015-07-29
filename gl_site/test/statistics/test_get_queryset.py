# Import the get_queryset function
from gl_site.statistics.data_generation import get_queryset

# Test imports
from django.test import TestCase
from gl_site.test.factory import Factory

# Models
from gl_site.models import Organization, Session

class TestGetQueryset(TestCase):
    """ Test class for get_queryset """

    def setUp(self):
        """ Set up variables used for testing """

        # Create a user to be used for testing
        self.user, self.info = Factory.create_user()

        # Create some organizations and sessions
        self.org1 = Factory.create_organization(self.user)
        Factory.create_session(self.org1, self.user)
        Factory.create_session(self.org1, self.user)

        self.org2 = Factory.create_organization(self.user)
        Factory.create_session(self.org2, self.user)
        Factory.create_session(self.org2, self.user)
        Factory.create_session(self.org2, self.user)
        Factory.create_session(self.org2, self.user)

    def test_user_is_staff(self):
        """ Validate the querysets returned from a user that is staff.
            Staff should have access to view all sessions in all
            organizations. Verify that that is what is returned.
        """

        # Set user as staff
        self.user.is_staff = True
        self.user.save()

        # Generate querysets
        querysets = get_queryset(self.user)

        # Organizatioins
        for organization in Organization.objects.all():
            self.assertIn(organization, querysets['organizations'])

        # Sessions
        for session in Session.objects.all():
            self.assertIn(session, querysets['sessions'])

    def test_user_is_not_staff(self):
        """ Validate the querysets returned for a user that is not staff.
            Regular users should only have access to view sessions in the
            organization that they belong to.
        """

        # Get the querysets
        querysets = get_queryset(self.user)

        # Organizations
        self.assertEqual(1, len(querysets['organizations']), "There is only one org")
        self.assertIn(self.info.organization, querysets['organizations'])

        # Sessions
        for session in Session.objects.filter(organization=self.info.organization):
            self.assertIn(session, querysets['sessions'])
