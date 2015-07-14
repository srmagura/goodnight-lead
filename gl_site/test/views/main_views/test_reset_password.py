# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.Factory import Factory

class TestResetPasswordPage(TestCase):
    """
    Test Case to verify the reset password page
    works as expected. View is not currently used.
    """

    def setUp(self):
        """
        Set up user account for testing
        """
        self.user, user_info = Factory.createUser()

    def testLogoutRequired(self):
        """
        Verify a user must be logged out
        before navigating to the page
        """

        # Login
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the GET request
        response = self.client.get('/reset_password', follow = True)

        # Verify redirected to index
        self.assertRedirects(response, '/')

    def testGET(self):
        """
        Verify the correct response is returned on a GET request
        """

        # Make the GET request
        response = self.client.get('/reset_password', follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/reset_password_page.html')

        # Verify the form and success are passed to the response
        self.assertTrue('form' in response.context)
        self.assertTrue('success' in response.context)

        self.assertFalse(response.context['success'])

    def testPOST(self):
        """
        Verify the correct response is returned on a POST request
        """

        # Make the GET request
        response = self.client.post('/reset_password', {'email': self.user.email}, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/reset_password_page.html')

        # Verify the form and success are passed to the response
        self.assertTrue('form' in response.context)
        self.assertTrue('success' in response.context)

        self.assertTrue(response.context['success'])
