# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.factory import Factory

class TestErrorPage(TestCase):
    """
    Verify the page not found error page
    displays correctly
    """

    def testPageNotFound(self):
        """
        Verify the correct templage is rendered
        when logged in
        """

        # Create an account and log in
        user, user_info = Factory.create_user()
        self.client.login(username = user.username, password = Factory.default_password)

        # Make the GET request
        response = self.client.get('/unsupportedpage', follow = True)

        # Verify template
        self.assertTemplateUsed(response, 'page_not_found.html')
