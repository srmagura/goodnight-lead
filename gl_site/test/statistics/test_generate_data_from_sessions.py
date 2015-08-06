# Import the generate_data function
from gl_site.statistics.data_generation import generate_data_from_sessions

# Test imports
from django.test import TestCase
from gl_site.test.factory import Factory

# Models
from gl_site.models import Metric, Submission
from django.db.models import Count, Min, Max, Avg, StdDev

# Inventories
from gl_site.inventories import inventory_cls_list
from gl_site.inventories.big_five import BigFive
from gl_site.inventories.ambiguity import Ambiguity
from gl_site.inventories.via import Via

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

        # Attach an explicit, non staff user, to the organization
        self.user, self.info = Factory.create_user(self.session1)

        # Generate data (3 sets of submissions) for each session
        for session in self.sessions:
            for i in range(0, 3):
                user, info = Factory.create_user(session)
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

        # All three sets of subdata should exist
        self.assertIn('submission_counts', data)
        self.assertIn('metrics_analysis', data)
        self.assertIn('users', data)

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

        # Generate the data for a non staff
        data = generate_data_from_sessions(self.sessions, self.user)

        # Verify non staff do not have access to analysis
        self.assertIn('submission_counts', data)
        self.assertNotIn('metrics_analysis', data)
        self.assertIn('users', data)

        # Set staff to check for analysis
        self.user.is_staff = True
        self.user.save()

        # Load the data
        data = generate_data_from_sessions(self.sessions, self.user)

        # Verify staff have all data
        self.assertIn('submission_counts', data)
        self.assertIn('metrics_analysis', data)
        self.assertIn('users', data)

        # Verify each submission has a submission count
        self.assertEqual(6, len(data['submission_counts']))

        # Verify the submission count is correct
        for submission in data['submission_counts']:
            correct_count = Submission.objects.filter(inventory_id=submission['inventory_id']).count()
            self.assertEqual(submission['count'], correct_count)

        # Verify that there is a metric analysis for each metric
        # That does not belong to Via.
        correct_count = Metric.objects.exclude(
            submission__inventory_id=Via.inventory_id
        ).distinct('key', 'submission__inventory_id').count()
        self.assertEqual(len(data['metrics_analysis']), correct_count)

        # Verify that the metric analysis for each inventory is correct
        for analysis in data['metrics_analysis']:
            correct_analysis = Metric.objects.filter(
                key=analysis['key'],
                submission__inventory_id=analysis['submission__inventory_id']
            ).values(
                'key', 'submission__inventory_id'
            ).annotate(
                min=Min('value'),
                max=Max('value'),
                mean=Avg('value'),
                standard_deviation=StdDev('value')
            )

            self.assertDictEqual(analysis, correct_analysis[0])

        # Verify that the user data is correct
        for user in data['users']:
            # The correct number of submissions has been attached
            num_submissions = Submission.objects.filter(user=user).count()
            self.assertEqual(len(user.submissions), num_submissions)

            # For each user submission
            for submission in user.submissions:
                # The submission belongs to the user
                self.assertEqual(user, submission.user)

                # The correct metrics exist in the submission
                num_metrics = Metric.objects.filter(submission=submission).count()
                self.assertEqual(len(submission.metrics), num_metrics)

                # For each submission metric
                for metric in submission.metrics:
                    # The metric belongs to the submission
                    self.assertEqual(submission, metric.submission)

    def test_partial_excludes(self):
        """ Data is only supposed to be generated for non staff users
            for inventories that have 10 submissions. Previous tests
            checked for all inventories at this boundary. Test that if
            some inventories have 10 submissions and some have less,
            only the ones which meet the requirement are returned
            within the data set.
        """

        # Create a submission for Big Five, Ambiguity, and Via
        Factory.create_submission(self.user, BigFive)
        Factory.create_submission(self.user, Ambiguity)
        Factory.create_submission(self.user, Via)

        # List of inventory id's a valid submission may have
        valid_submissions = [BigFive.inventory_id, Ambiguity.inventory_id, Via.inventory_id]

        # Grab the data
        data = generate_data_from_sessions(self.sessions, self.user)

        # A count of all submissions exists
        self.assertEqual(6, len(data['submission_counts']))

        # Verify the submission count is correct
        for submission in data['submission_counts']:
            correct_count = Submission.objects.filter(inventory_id=submission['inventory_id']).count()
            self.assertEqual(submission['count'], correct_count)

        # Non admin does not have analysis
        self.assertNotIn('metrics_analysis', data)

        # Verify that the user data is correct
        for user in data['users']:
            # The correct number of submissions has been attached
            self.assertEqual(len(user.submissions), len(valid_submissions))

            # For each user submission
            for submission in user.submissions:
                # The submission belongs to the user
                self.assertEqual(user, submission.user)

                # The submission is valid
                self.assertIn(submission.inventory_id, valid_submissions)

                # The correct metrics exist in the submission
                num_metrics = Metric.objects.filter(submission=submission).count()
                self.assertEqual(len(submission.metrics), num_metrics)

                # For each submission metric
                for metric in submission.metrics:
                    # The metric belongs to the submission
                    self.assertEqual(submission, metric.submission)
