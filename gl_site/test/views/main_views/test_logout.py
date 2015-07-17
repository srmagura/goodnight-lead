# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.factory import Factory

class TestLogout(TestCase):
    """
    Test case for the logout view
    """

    def testLogout(self):
        # Create an account and log in
        user, user_info = Factory.create_user()
        self.client.login(username = user.username, password = Factory.defaultPassword)

        # Make the get reqeust
        response = self.client.get('/logout', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/login')
