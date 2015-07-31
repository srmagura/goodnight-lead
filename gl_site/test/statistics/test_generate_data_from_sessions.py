# Import the generate_data function
from gl_site.statistics.data_generation import generate_data_from_sessions

# Test imports
from django.test import TestCase
from gl_site.test.factory import Factory

# Models
from gl_site.models import Metric

# Inventories
from gl_site.inventories import inventory_cls_list

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

        # Make staff
        self.user.is_staff = True
        self.user.save()

        # Request the data and verify it exists
        data = generate_data_from_sessions(self.sessions, self.user)

        # One entry for each of the 6 inventories
        self.assertEqual(6, len(data))

    def test_not_enough_user_regular(self):
        """ Regular users should not be able to view statistics without data.
            There must be at least 10 submissions to view.
        """

        try:
            # Request the data
            data = generate_data_from_sessions(self.sessions, self.user)
            self.fail('LookupError should have been raised. No data.')
        except LookupError:
            pass

    def test_enough_data(self):
        """ Metrics are returned correctly if enough data exists
            Independent of whether or not user is staff.
        """

        # Generate the 10th set of data
        Factory.create_set_of_submissions(self.user)

        # Load the data
        data = generate_data_from_sessions(self.sessions, self.user)

        # All 6 inventories should be listed
        self.assertEqual(6, len(data))

        inventories_by_name = {i.__name__: i for i in inventory_cls_list}

        # Validate each inventory
        for entry in data:
            # Data is present
            self.assertIn('inventory', entry)
            self.assertIn('data', entry)

            # Grab all the metrics
            metrics = Metric.objects.filter(
                submission__inventory_id=inventories_by_name[entry['inventory']].inventory_id,
                submission__user__leaduserinfo__session__in=self.sessions
            ).count()

            # If not via number of data points is equal to the nubmer of metrics
            if entry['inventory'] != 'Via':
                self.assertEqual(metrics, len(entry['data']))
            # Via datapoints is equal to the number of signature
            # strengths. 3 for this data set because all the data
            # is always the same.
            else:
                self.assertEqual(3, len(entry['data']))
