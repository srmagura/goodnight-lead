# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

# Import use info for testing account creation
from app.models import LeadUserInfo

# Regex parser
import re

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
        self.assertTrue('inventories' in response.context)
        self.assertTrue(len(response.context['inventories']) == 6)
        self.assertTrue('quotes' in response.context)

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
    """ Test method for register view """

    def setUp(self):
        User.objects.create_user(username = 'test', email='test@gmail.com', password = 'test')

    def testLogoutRequired(self):
        # Log in
        self.client.login(username = 'test', password = 'test')

        # Make the response
        response = self.client.get('/register', follow = True)

        # Sanity check
        self.assertTrue(response.context['user'].is_authenticated())

        # Verify redirect to index
        self.assertRedirects(response, '/')

    def testRequestMethodGET(self):
        """
        Verify that making a request via GET
        renders the register page with blank
        forms
        """
        # Make the request
        response = self.client.get('/register', follow = True)

        # Verify the register page was rendered
        self.assertTemplateUsed(response, 'user_templates/register.html')

        # Verify no messages were sent
        self.assertEqual(len(response.context['messages']), 0)

        # Verify both forms are included in the response
        self.assertTrue('userForm' in response.context)
        self.assertTrue('infoForm' in response.context)

        # Verify both forms are blank and have no errors
        for field in response.context['userForm']:
            self.assertEqual(field.errors, [])
            self.assertEqual(field.value(), None)

        for field in response.context['infoForm']:
            self.assertEqual(field.errors, [])
            self.assertEqual(field.value(), None)

    def testUserInfoNotValid_UsernameNotUnique(self):
        """
        Verify that submission via POST with a
        username that is already in use rerenders
        the template and shows an error without
        creating the user account
        """
        # Make the post request
        response = self.client.post('/register',
            {
                # User info
                'username': 'test', # Non unique user name
                'email': 'unique@gmail.com',
                'password1': 'testpass',
                'password2': 'testpass',
                'first_name': 'test',
                'last_name': 'user',

                # Lead info
                'gender': 'M',
                'major': 'tester',
                'year': '1',
                'organization': 'gsp'
            },
            follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user_templates/register.html')

        # Verify both forms are included in the response
        self.assertTrue('userForm' in response.context)
        self.assertTrue('infoForm' in response.context)

        # Verify form fields retain their set values
        userform = response.context['userForm']
        self.assertEqual(userform['username'].value(), 'test')
        self.assertEqual(userform['email'].value(), 'unique@gmail.com')
        self.assertEqual(userform['first_name'].value(), 'test')
        self.assertEqual(userform['last_name'].value(), 'user')
        self.assertEqual(userform['password1'].value(), 'testpass')
        self.assertEqual(userform['password2'].value(), 'testpass')

        # lead stuff
        infoform = response.context['infoForm']
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['major'].value(), 'tester')
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['organization'].value(), 'gsp')

        # Correct error messages gets set
        self.assertEqual(re.sub(r'\* ', '', userform['username'].errors.as_text()),
            'A user with that username already exists.')
        self.assertEqual(userform['email'].errors.as_text(), '')
        self.assertEqual(userform['first_name'].errors.as_text(), '')
        self.assertEqual(userform['last_name'].errors.as_text(), '')
        self.assertEqual(userform['password1'].errors.as_text(), '')
        self.assertEqual(userform['password2'].errors.as_text(), '')
        self.assertEqual(infoform['gender'].errors.as_text(), '')
        self.assertEqual(infoform['major'].errors.as_text(), '')
        self.assertEqual(infoform['year'].errors.as_text(), '')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testUserInfoNotValid_EmailNotUnique(self):
        """
        Verify that submission via POST with an
        email that is already in use rerenders
        the template and shows an error without
        creating the user account
        """
        # Make the post request
        response = self.client.post('/register',
            {
                # User info
                'username': 'testuser',
                'email': 'test@gmail.com', # Non uniuqe email
                'password1': 'testpass',
                'password2': 'testpass',
                'first_name': 'test',
                'last_name': 'user',

                # Lead info
                'gender': 'M',
                'major': 'tester',
                'year': '1',
                'organization': 'gsp'
            },
            follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user_templates/register.html')

        # Verify both forms are included in the response
        self.assertTrue('userForm' in response.context)
        self.assertTrue('infoForm' in response.context)

        # Verify form fields retain their set values
        userform = response.context['userForm']
        self.assertEqual(userform['username'].value(), 'testuser')
        self.assertEqual(userform['email'].value(), 'test@gmail.com')
        self.assertEqual(userform['first_name'].value(), 'test')
        self.assertEqual(userform['last_name'].value(), 'user')
        self.assertEqual(userform['password1'].value(), 'testpass')
        self.assertEqual(userform['password2'].value(), 'testpass')

        # lead stuff
        infoform = response.context['infoForm']
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['major'].value(), 'tester')
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['organization'].value(), 'gsp')

        # Correct error messages gets set
        self.assertEqual(userform['username'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', userform['email'].errors.as_text()),
            'Email already in use')
        self.assertEqual(userform['first_name'].errors.as_text(), '')
        self.assertEqual(userform['last_name'].errors.as_text(), '')
        self.assertEqual(userform['password1'].errors.as_text(), '')
        self.assertEqual(userform['password2'].errors.as_text(), '')
        self.assertEqual(infoform['gender'].errors.as_text(), '')
        self.assertEqual(infoform['major'].errors.as_text(), '')
        self.assertEqual(infoform['year'].errors.as_text(), '')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testUserInfoNotValid_PasswordConfirmationFailed(self):
        """
        Verify that submission via POST with a
        failed password confirmation rerenders
        the template and shows an error without
        creating the user account
        """
        # Make the post request
        response = self.client.post('/register',
            {
                # User info
                'username': 'testuser',
                'email': 'testuser@gmail.com',
                'password1': 'testpass',
                'password2': 'testpass2',
                'first_name': 'test',
                'last_name': 'user',

                # Lead info
                'gender': 'M',
                'major': 'tester',
                'year': '1',
                'organization': 'gsp'
            },
            follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user_templates/register.html')

        # Verify both forms are included in the response
        self.assertTrue('userForm' in response.context)
        self.assertTrue('infoForm' in response.context)

        # Verify form fields retain their set values
        userform = response.context['userForm']
        self.assertEqual(userform['username'].value(), 'testuser')
        self.assertEqual(userform['email'].value(), 'testuser@gmail.com')
        self.assertEqual(userform['first_name'].value(), 'test')
        self.assertEqual(userform['last_name'].value(), 'user')
        self.assertEqual(userform['password1'].value(), 'testpass')
        self.assertEqual(userform['password2'].value(), 'testpass2')

        # lead stuff
        infoform = response.context['infoForm']
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['major'].value(), 'tester')
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['organization'].value(), 'gsp')

        # Correct error messages gets set
        self.assertEqual(userform['username'].errors.as_text(), '')
        self.assertEqual(userform['email'].errors.as_text(), '')
        self.assertEqual(userform['first_name'].errors.as_text(), '')
        self.assertEqual(userform['last_name'].errors.as_text(), '')
        self.assertEqual(userform['password1'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', userform['password2'].errors.as_text()),
            'The two password fields didn\'t match.')
        self.assertEqual(infoform['gender'].errors.as_text(), '')
        self.assertEqual(infoform['major'].errors.as_text(), '')
        self.assertEqual(infoform['year'].errors.as_text(), '')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testUserInfoNotValid_FieldsLeftBlank(self):
        """
        Verify that all fields fail to validate if
        left blank and that the page rerenders
        without creating the user account
        """
        # Make the post request
        response = self.client.post('/register',
            {
                # Lead info
                'gender': 'M',
                'major': 'tester',
                'year': '1',
                'organization': 'gsp'
            },
            follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user_templates/register.html')

        # Verify both forms are included in the response
        self.assertTrue('userForm' in response.context)
        self.assertTrue('infoForm' in response.context)

        # Verify form fields retain their set values
        userform = response.context['userForm']
        self.assertEqual(userform['username'].value(), None)
        self.assertEqual(userform['email'].value(), None)
        self.assertEqual(userform['first_name'].value(), None)
        self.assertEqual(userform['last_name'].value(), None)
        self.assertEqual(userform['password1'].value(), None)
        self.assertEqual(userform['password2'].value(), None)

        # lead stuff
        infoform = response.context['infoForm']
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['major'].value(), 'tester')
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['organization'].value(), 'gsp')

        # Correct error messages gets set
        self.assertEqual(re.sub(r'\* ', '', userform['username'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', userform['email'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', userform['first_name'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', userform['last_name'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', userform['password1'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', userform['password2'].errors.as_text()),
            'This field is required.')
        self.assertEqual(infoform['gender'].errors.as_text(), '')
        self.assertEqual(infoform['major'].errors.as_text(), '')
        self.assertEqual(infoform['year'].errors.as_text(), '')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testLEADInfoNotValid_FieldsLeftBlank(self):
        """
        Verify that all fields fail to validate if
        left blank and that the page rerenders
        without creating the user account
        """
        # Make the post request
        response = self.client.post('/register',
            {
                # User info
                'username': 'testuser',
                'email': 'testuser@gmail.com',
                'password1': 'testpass',
                'password2': 'testpass',
                'first_name': 'test',
                'last_name': 'user'
            },
            follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user_templates/register.html')

        # Verify both forms are included in the response
        self.assertTrue('userForm' in response.context)
        self.assertTrue('infoForm' in response.context)

        # Verify form fields retain their set values
        userform = response.context['userForm']
        self.assertEqual(userform['username'].value(), 'testuser')
        self.assertEqual(userform['email'].value(), 'testuser@gmail.com')
        self.assertEqual(userform['first_name'].value(), 'test')
        self.assertEqual(userform['last_name'].value(), 'user')
        self.assertEqual(userform['password1'].value(), 'testpass')
        self.assertEqual(userform['password2'].value(), 'testpass')

        # lead stuff
        infoform = response.context['infoForm']
        self.assertEqual(infoform['gender'].value(), None)
        self.assertEqual(infoform['major'].value(), None)
        self.assertEqual(infoform['year'].value(), None)
        self.assertEqual(infoform['organization'].value(), None)

        # Correct error messages gets set
        self.assertEqual(userform['username'].errors.as_text(), '')
        self.assertEqual(userform['email'].errors.as_text(), '')
        self.assertEqual(userform['first_name'].errors.as_text(), '')
        self.assertEqual(userform['last_name'].errors.as_text(), '')
        self.assertEqual(userform['password1'].errors.as_text(), '')
        self.assertEqual(userform['password2'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', infoform['gender'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', infoform['major'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', infoform['year'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', infoform['organization'].errors.as_text()),
            'This field is required.')

    def testValidInfo(self):
        """
        Verify that submission of valid information
        creates the user account, the lead info,
        logs the user in, sets a success message,
        and redirects to the index view
        """
        # Make the post request
        response = self.client.post('/register',
            {
                # User info
                'username': 'testuser',
                'email': 'testuser@gmail.com',
                'password1': 'testpass',
                'password2': 'testpass',
                'first_name': 'test',
                'last_name': 'user',

                # Lead info
                'gender': 'M',
                'major': 'tester',
                'year': '1',
                'organization': 'gsp'
            },
            follow = True)

        # Verify the user account is created with correct attributes
        user = User.objects.get(username = 'testuser')
        info = LeadUserInfo.objects.get(user = user)

        self.assertTrue(user is not None)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@gmail.com')
        self.assertNotEqual(user.password, 'testuser') # Password should be hashed
        self.assertEqual(user.first_name, 'test')
        self.assertEqual(user.last_name, 'user')

        self.assertTrue(info is not None)
        self.assertEqual(info.user, user)
        self.assertEqual(info.gender, 'M')
        self.assertEqual(info.major, 'tester')
        self.assertEqual(info.organization, 'gsp')

        # Verify success message set
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        for message in messages:
            self.assertEqual(message.message, "User account created successfully.")

        # Verify the user is redirected to the index page
        self.assertRedirects(response, '/')

class testMainViews_ResetPasswordPage(TestCase):
    """
    Test Case to verify the reset password page
    works as expected. View is not currently used.
    """
    pass
