from django.test import TestCase

from gl_site.test.factory import Factory
from .auth_test_util import AuthTestUtil

INVALID_LOGIN_MSG = ('Your account has no associated demographic '
    'information, and thus you are not allowed to login. '
    'This can only occur if your account was not created '
    'through the user registration form. '
    'If you are an administrator, you can still login to '
    'the admin site. If you would like to access the public '
    'part of the site, please create a new account through '
    'the user registration form.')

class TestAdminAuth(TestCase, AuthTestUtil):
    """
    Test authentication for admins. Admins can log into the admin site,
    but they may or may not have LeadUserInfo.
    """

    def setUp(self):
        """
        Create a superuser that lacks LeadUserInfo.
        """
        admin = Factory.create_admin()
        self.admin = admin

    def test_public_login(self):
        """
        Verify that a user without LeadUserInfo cannot log in to the
        public site.
        """
        self.assert_invalid_login(self.admin.username,
            Factory.default_password, INVALID_LOGIN_MSG)

    def assert_login_page(self, response):
        """
        Assert that we are on the login page and unauthenticated.
        """
        self.assertTemplateUsed(response, template_name='user/login.html')
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logged_in_view_login(self):
        """
        Verify that if an admin is authenticated and tries
        to access the site index (i.e. /) they are logged out and
        redirected to the login page.
        """
        response = self.client.get('/', follow=True)
        self.assert_login_page(response)

    def test_logged_in_view_public(self):
        """
        Verify that if an admin is authenticated and tries
        to access part of the public site they are logged out and
        redirected to the login page.
        """
        response = self.client.get('/inventory/review/0', follow=True)
        self.assert_login_page(response)
