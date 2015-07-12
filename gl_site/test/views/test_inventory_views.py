# Test Case
from django.test import TestCase

# Import user.
from django.contrib.auth.models import User

# Import Submission
from gl_site.models import Submission
from gl_site.models import Metric

# Factory
from gl_site.test.Factory import Factory

class testInventoryViews_TakeInventory(TestCase):
    """
    Test Case for the Take Inventory view.
    """

    def setUp(self):
        """
        Set up for testing by creating a user account
        and loggin in.
        """

        # Create a user account and login
        self.user, user_info = Factory.createUser()
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

    def testLoginRequired(self):
        """
        Verify the view cannot be loaded
        by a user that is not logged in
        """

        # Log out
        self.client.logout()

        # Send the GET request
        response = self.client.get('/inventory/take/0', follow = True)

        # Verify redirect to login page
        self.assertRedirects(response, '/login')

    def testInvalidInventoryId(self):
        """
        Verify requesting an invalid inventory redirects
        to the error page
        """

        # Send the GET request
        response = self.client.get('/inventory/take/9999', follow = True)

        # Verify redirect to login page
        self.assertTemplateUsed(response, 'page_not_found.html')

    def testCompleteInventory(self):
        """
        Verify that trying to take a completed inventory
        redirects to the review page
        """

        # Create a Big5 submission with metrics
        submission = Submission.objects.create(
            user = self.user, inventory_id = 0)
        Metric.objects.create(submission = submission, key = 'openness', value = 4)
        Metric.objects.create(submission = submission, key = 'extraversion', value = 4)
        Metric.objects.create(submission = submission, key = 'emotional_stability', value = 4)
        Metric.objects.create(submission = submission, key = 'agreeableness', value = 4)
        Metric.objects.create(submission = submission, key = 'conscientiousness', value = 4)

        # Make the GET request
        response = self.client.get('/inventory/take/0', follow = True)

        # Verify redirect to the review page
        self.assertRedirects(response, '/inventory/review/0')

    def testGETRequest(self):
        """
        Verify that a logged in user requesting a valid inventory
        is given the correct data
        """

        # Make the GET reqeust
        response = self.client.get('/inventory/take/0', follow = True)

        # Verify the tmplate used
        self.assertTemplateUsed(response, 'take_inventory/big_five.html')

        # Verify the inventory, form, and final page are passed
        self.assertIn('inventory', response.context)
        self.assertIn('form', response.context)
        self.assertIn('is_final_page', response.context)

    def testPOSTRequest(self):
        """
        Verify inventory submission
        """

        # Make the POST request
        response = self.client.post('/inventory/take/0', {
                '1': '1',
                '2': '1',
                '3': '1',
                '4': '1',
                '5': '1',
                '6': '1',
                '7': '1',
                '8': '1',
                '9': '1',
                '10': '1',
            }, follow = True)

        # Verify redirects to view inventory
        self.assertRedirects(response, '/inventory/review/0')

class testInventoryViews_ReviewInventory(TestCase):
    """
    Test Case for the Review Inventory view
    """
    def setUp(self):
        # Create a user account and login
        self.user, user_info = Factory.createUser()
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Create an inventory
        self.client.post('/inventory/take/0', {
                '1': '1',
                '2': '1',
                '3': '1',
                '4': '1',
                '5': '1',
                '6': '1',
                '7': '1',
                '8': '1',
                '9': '1',
                '10': '1',
            }, follow = True)

    def testLoginRequired(self):
        """
        Verify must be logged in to
        access the review page
        """

        # Log out
        self.client.logout()

        # Make the GET request
        response = self.client.get('/inventory/review/0', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/login')

    def testInvalidInventoryId(self):
        """
        Verify navigating to an unknown inventory
        renders the error page
        """

        # Send the GET request
        response = self.client.get('/inventory/review/9999', follow = True)

        # Verify redirect to login page
        self.assertTemplateUsed(response, 'page_not_found.html')

    def testIncompleteInventory(self):
        """
        Verify that navegating to an incomplete inventory
        redirects to the take inventory page
        """

        # Send the GET request
        response = self.client.get('/inventory/review/1', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/inventory/take/1')

    def testGETRequest(self):
        """
        Make a valid GET request and verify
        the correct data is loaded
        """

        # Make the GET request
        response = self.client.get('/inventory/review/0', follow = True)

        # Verify the correct template is used
        self.assertTemplateUsed(response, 'review_inventory/big_five.html')

        # Verify the inventory is passed to the template
        self.assertIn('inventory', response.context)
