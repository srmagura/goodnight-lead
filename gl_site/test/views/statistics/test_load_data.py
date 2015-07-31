# Import test case
from django.test import TestCase

# Object factory
from gl_site.test.factory import Factory

# View
from gl_site.statistics import views as stats

class TestLoadData(TestCase):
    """ Test for the load data view """

    def setUp(self):
        """ Set up a user for testing """

        self.user, self.info = Factory.create_user()
        self.user.is_staff = True
        self.user.save()

        Factory.create_set_of_submissions(self.user)

        # Login
        self.client.login(username=self.user.username, password=Factory.default_password)

    def test_login_required(self):
        """ User must be logged in to view """

        # Logout
        self.client.logout()

        # Make the request
        response = self.client.get('/statistics/load_data', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/login')

    def test_view_loads_with_login(self):
        """ View should load with login """

        data = {
            'organization': self.info.organization.id,
            'session': self.info.session.id
        }

        # Make the request
        response = self.client.get('/statistics/load_data', data, follow = True)

        self.assertEqual(200, response.status_code)

    def test_method_not_allowed(self):
        """ Method must be GET """

        # Make a bad request
        response = self.client.post('/statistics/load_data', follow = True)

        # Verify
        self.assertEqual(stats.METHOD_NOT_ALLOWED, response.status_code)

    def test_forbidden(self):
        """ Bad organization or session choice responds as forbidden """

        # Data
        data = {
            'organization': 0,
            'session': 0
        }

        # Make the request
        response = self.client.get('/statistics/load_data', data, follow = True)

        # Verify
        self.assertEquals(stats.FORBIDDEN, response.status_code)

    def test_bad_request(self):
        """ Bad request represents an error while looking up data """

        # Unset staff privileges
        self.user.is_staff = False
        self.user.save()

        # Data
        data = {
            'organization': self.info.organization.id,
            'session': self.info.session.id
        }

        # Make the request
        response = self.client.get('/statistics/load_data', data, follow = True)

        # Verify
        self.assertEquals(stats.BAD_REQUEST, response.status_code)
