# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.factory import Factory
from .auth_test_util import AuthTestUtil

INVALID_LOGIN_MSG = 'Incorrect username or password.'

class TestLogin(TestCase, AuthTestUtil):
    """ Test Case for the home view """

    def setUp(self):
        """ Set Up """
        user, user_info = Factory.create_user()
        self.user = user

    def testLogoutRequired(self):
        """ Verify that a logged in user cannot make it to the login page """

        # login
        self.client.login(username = self.user.username, password = Factory.default_password)

        # Make the request
        response = self.client.post('/login', follow = True)
        self.assertRedirects(response, '/')

    def testInvalidLogin_Username(self):
        """
        Verify that an invalid username does not let a user in.
        Authentication failure should set a warning message
        and rerender the template.
        """
        self.assert_invalid_login('invalid', Factory.default_password,
            INVALID_LOGIN_MSG)

    def testInvalidLogin_Password(self):
        """
        Verify that an invalid password does not let a user in.
        Authentication failure should set a warning message
        and rerender the template.
        """
        self.assert_invalid_login(self.user.username, 'invalid',
            INVALID_LOGIN_MSG)

    def testInvalidLogin_Both(self):
        """
        Verify that an invalid username and password do not let a user in.
        Authentication failure should set a warning message
        and rerender the template.
        """
        self.assert_invalid_login('invalid', 'invalid',
            INVALID_LOGIN_MSG)

    def testValidLogin(self):
        """
        Verify that a valid username and password let a user in.
        Will redirect to the dashboard.
        """

        # Make the request with username and password set
        response = self.client.post('/login',
            {'username': self.user.username, 'password': Factory.default_password}, follow = True)

        # Get messages and verify
        messages = response.context['messages']
        self.assertEqual(len(messages), 0)

        # Redirect and correct template used
        self.assertRedirects(response, '/')
        self.assertTemplateUsed(response, template_name = 'dashboard.html')

        # User authenticated
        self.assertTrue(response.context['user'].is_authenticated)
