# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

class TestMainViews_Index(TestCase):
    """ Test class for the index view """

    def setUp(self):
        """ Set Up """
        User.objects.create_user(username = 'test', password = 'pass')

    def testLoginRequiredNoRedirectField(self):
        """
        Verify that the view redirects to the index page
        if the user is not logged in.
        """
        response = self.client.get('/', follow = True)
        self.assertRedirects(response, '/login')

        response = self.client.post('/', follow = True)
        self.assertRedirects(response, '/login')

    def testViewLoadsWithLogin(self):
        """ Test that a user who is logged in is sent to the index page """

        # login
        self.client.login(username = 'test', password = 'pass')

        # Make the request
        response = self.client.get('/', follow = True)

        # Verify the user was sent to the index page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name = 'index.html')

        # Verify the expected amount of data is passed
        self.assertTrue(len(response.context) == 2)
        self.assertTrue(response.context['inventories'])
        self.assertTrue(len(response.context['inventories']) == 6)
        self.assertTrue(response.context['quotes'])

class TestMainViews_Login(TestCase):
    """ Test Case for the login_page view """

    def setUp(self):
        """ Set Up """
        User.objects.create_user(username = 'test', email='test@gmail', password='test')

    def testLogoutRequired(self):
        """ Verify that a logged in user cannot make it to the login page """

        # login
        self.client.login(username = 'test', password = 'test')

        # Make the request
        response = self.client.post('/login', follow = True)
        self.assertRedirects(response, '/')

    def testInvalidLogin_Username(self):
        """
        Verify that an invalid username does not let a user in.
        Authentication failure should set a warning message
        and rerender the template.
        """

        # Make the request with username and password set
        response = self.client.post('/login', {'username': 'testuser', 'password': 'test'}, follow = True)

        # Get messages and verify
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        for message in messages:
            self.assertEqual(message.message, "Incorrect username or password")

        # Correct template used
        self.assertTemplateUsed(response, template_name = 'user_templates/login.html')

        # Not authenticated
        self.assertFalse(response.context['user'].is_authenticated())

    def testInvalidLogin_Password(self):
        """
        Verify that an invalid password does not let a user in.
        Authentication failure should set a warning message
        and rerender the template.
        """

        # Make the request with username and password set
        response = self.client.post('/login', {'username': 'test', 'password': 'testpass'}, follow = True)

        # Get messages and verify
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        for message in messages:
            self.assertEqual(message.message, "Incorrect username or password")

        # Correct template used
        self.assertTemplateUsed(response, template_name = 'user_templates/login.html')

        # Not authenticated
        self.assertFalse(response.context['user'].is_authenticated())

    def testInvalidLogin_Both(self):
        """
        Verify that an invalid username and password do not let a user in.
        Authentication failure should set a warning message
        and rerender the template.
        """

        # Make the request with username and password set
        response = self.client.post('/login', {'username': 'testuser', 'password': 'testpass'}, follow = True)

        # Get messages and verify
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        for message in messages:
            self.assertEqual(message.message, "Incorrect username or password")

        # Correct template used
        self.assertTemplateUsed(response, template_name = 'user_templates/login.html')

        # Not authenticated
        self.assertFalse(response.context['user'].is_authenticated())

    def testValidLogin(self):
        """
        Verify that a valid username and password let a user in.
        Will redirect to the index page.
        """

        # Make the request with username and password set
        response = self.client.post('/login', {'username': 'test', 'password': 'test'}, follow = True)

        # Get messages and verify
        messages = response.context['messages']
        self.assertEqual(len(messages), 0)

        # Redirect and correct template used
        self.assertRedirects(response, '/')
        self.assertTemplateUsed(response, template_name = 'index.html')

        # User authenticated
        self.assertTrue(response.context['user'].is_authenticated())

class testMainViews_Register(TestCase):
    """  """

    def testRequestMethodNotPOST(self):
        pass

    def testUserInfoNotValid_UsernameNotUnique(self):
        pass

    def testUserInfoNotValid_EmailNotUnique(self):
        pass

    def testUserInfoNotValid_PasswordConfirmationFailed(self):
        pass

    def testUserInfoNotValid_FieldsLeftBlank(self):
        pass

    def testLEADInfoNotValid_FieldsLeftBlank(self):
        pass

    def testValidInfo(self):
        pass
