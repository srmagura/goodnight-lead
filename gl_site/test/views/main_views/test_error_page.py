# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.Factory import Factory

class TestErrorPage(TestCase):
    """
    Verify the page not found error page
    displays correctly
    """

    def testLoginRequired(self):
        """
        Navigation to an unknown page while not logged in
        redirects to the login page
        """

        # Make the response and verify redirect
        response = self.client.get('/unsupportedpage', follow = True)
        self.assertRedirects(response, '/login')

    def testPageNotFound(self):
        """
        Verify the correct templage is rendered
        when logged in
        """

        # Create an account and log in
        user, user_info = Factory.createUser()
        self.client.login(username = user.username, password = Factory.defaultPassword)

        # Make the GET request
        response = self.client.get('/unsupportedpage', follow = True)

        # Verify template
        self.assertTemplateUsed(response, 'page_not_found.html')
