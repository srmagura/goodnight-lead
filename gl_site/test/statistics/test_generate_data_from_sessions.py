# Import the generate_data function
from gl_site.statistics.data_generation import generate_data_from_sessions

# Test imports
from django.test import TestCase
from gl_site.test.factory import Factory

# Models
from gl_site.models import Submission, Metric

class TestGenerateData(TestCase):
    """ Test case for generating statistics data from sessions """

    def setUp(self):
        """ Set up submission data in an organization for testing """

        # Admin account without leaduserinfo
        self.admin = Factory.create_admin()

        # Create an organization with three sessions
        self.org = Factory.create_organization(self.admin)
        self.session1 = Factory.create_session(self.org, self.admin)
        self.session2 = Factory.create_session(self.org, self.admin)
        self.session3 = Factory.create_session(self.org, self.admin)
        self.sessions = [self.session1, self.session2, self.session3]

        # Attach an explicit, no staff user, to the organization
        self.user, self.info = Factory.create_user_in_session(self.session1)

        # Generate data (3 sets of submissions) for each session
        for session in self.sessions:
            for i in range(0, 3):
                user, info = Factory.create_user_in_session(session)
                Factory.create_set_of_submissions(user)

    def test_not_enough_user_staff(self):
        """ Staff users should be able to view statistics any time.
            This is regardless of whether or not there are more than
            10 submissions for any inventory
        """

        self.assertEqual(9 * 6, Submission.objects.all().count())

    def test_not_enough_user_regular(self):
        """ Regular users should not be able to view statistics without data.
            There must be at least 10 submissions to view.
        """

        pass

    def test_enough_data(self):
        """ Metrics are returned correctly if enough data exists """

        pass
