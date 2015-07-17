# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.factory import Factory

class TestDashboard(TestCase):
    """ Test class for the dashboard view """

    def setUp(self):
        """ Set Up """
        self.user, user_info = Factory.create_user()

    def testLoginRequiredNoRedirectField(self):
        """
        Verify that the view redirects to the login page
        if the user is not logged in.
        """
        response = self.client.get('/', follow = True)
        self.assertRedirects(response, '/login')

        response = self.client.post('/', follow = True)
        self.assertRedirects(response, '/login')

    def testViewLoadsWithLogin(self):
        """ Test that a user who is logged in is sent to the dashboard """

        # login
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the request
        response = self.client.get('/', follow = True)

        # Verify the user was sent to the dashboard
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'dashboard.html')

        # Verify the expected amount of data is passed
        self.assertTrue('inventories' in response.context)
        self.assertEquals(len(response.context['inventories']), 6)
        self.assertTrue('quotes' in response.context)
