# Test Case
from django.test import TestCase

# Factory
from gl_site.test.Factory import Factory

# Import Submission
from gl_site.models import Submission, Metric

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
