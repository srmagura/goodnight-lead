# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.factory import Factory

class TestViewStatistics(TestCase):
    """ Test the view statistics view """

    def setUp(self):
        """ Create a user for testing """
        self.user, self.info = Factory.create_user()

    def test_login_required(self):
        """ User must be logged in to view """

        # Make the request
        response = self.client.get('/statistics/view', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/login')

    def test_view_loads_with_login(self):
        """ View should load with login """

        # Login
        self.client.login(username=self.user.username, password=Factory.default_password)

        # Make the request
        response = self.client.get('/statistics/view', follow = True)

        # Verify
        self.assertTemplateUsed(response, template_name = 'statistics/statistics.html')
        self.assertIn('form', response.context)
