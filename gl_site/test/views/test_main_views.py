# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

# Import use info for testing account creation
from gl_site.models import LeadUserInfo, Organization

# Object factory
from gl_site.test.Factory import Factory

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
        self.assertTemplateUsed(response, template_name = 'user/login.html')

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
        self.assertTemplateUsed(response, template_name = 'user/login.html')

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
        self.assertTemplateUsed(response, template_name = 'user/login.html')

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
        """ Create user account for testing """
        self.user = Factory.createUser()

        self.organization = Factory.createOrganization(self.user)

        self.session = Factory.createSession(self.organization, self.user)

        self.info = Factory.createDemographics(self.user, self.organization, self.session)

    def testLogoutRequired(self):
        """ A logged in user cannot access this page """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the response
        response = self.client.get('/register/{}'.format(self.info.session.uuid), follow = True)

        # Sanity check
        self.assertTrue(response.context['user'].is_authenticated())

        # Verify redirect to index
        self.assertRedirects(response, '/')

    def testRequestMethodGET(self):
        """ GET request for registration
            Verify that making a request via GET
            renders the register page with blank
            forms
        """
        # Make the request
        response = self.client.get('/register/{}'.format(self.info.session.uuid), follow = True)

        # Verify the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify no messages were sent
        self.assertEqual(len(response.context['messages']), 0)

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify both forms are blank and have no errors
        for field in response.context['user_form']:
            self.assertEqual(field.errors, [])
            self.assertEqual(field.value(), None)

        for field in response.context['info_form']:
            self.assertEqual(field.errors, [])
            self.assertEqual(field.value(), None)

    def testUserInfoNotValid_UsernameNotUnique(self):
        """ Attempt to register with a taken username.
            Verify that submission via POST with a
            username that is already in use rerenders
            the template and shows an error without
            creating the user account
        """

        # Get the POST dict
        registrationform = Factory.createUserRegistrationPostDict(self.organization)
        registrationform['username'] = self.user.username

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registrationform, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.assertEqual(user_form['username'].value(), registrationform['username'])
        self.assertEqual(user_form['email'].value(), registrationform['email'])
        self.assertEqual(user_form['first_name'].value(), registrationform['first_name'])
        self.assertEqual(user_form['last_name'].value(), registrationform['last_name'])
        self.assertEqual(user_form['password1'].value(), registrationform['password1'])
        self.assertEqual(user_form['password2'].value(), registrationform['password2'])

        # lead stuff
        info_form = response.context['info_form']
        self.assertEqual(info_form['gender'].value(), registrationform['gender'])
        self.assertEqual(info_form['major'].value(), registrationform['major'])
        self.assertEqual(info_form['year'].value(), str(registrationform['year']))
        self.assertEqual(info_form['organization_code'].value(), registrationform['organization_code'])

        # Correct error messages gets set
        self.assertEqual(re.sub(r'\* ', '', user_form['username'].errors.as_text()),
            'A user with that username already exists.')
        self.assertEqual(user_form['email'].errors.as_text(), '')
        self.assertEqual(user_form['first_name'].errors.as_text(), '')
        self.assertEqual(user_form['last_name'].errors.as_text(), '')
        self.assertEqual(user_form['password1'].errors.as_text(), '')
        self.assertEqual(user_form['password2'].errors.as_text(), '')
        self.assertEqual(info_form['gender'].errors.as_text(), '')
        self.assertEqual(info_form['major'].errors.as_text(), '')
        self.assertEqual(info_form['year'].errors.as_text(), '')
        self.assertEqual(info_form['organization_code'].errors.as_text(), '')

    def testUserInfoNotValid_EmailNotUnique(self):
        """
        Verify that submission via POST with an
        email that is already in use rerenders
        the template and shows an error without
        creating the user account
        """

        # Get the POST dict
        registrationform = Factory.createUserRegistrationPostDict(self.organization)
        registrationform['email'] = self.user.email

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registrationform, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.assertEqual(user_form['username'].value(), registrationform['username'])
        self.assertEqual(user_form['email'].value(), registrationform['email'])
        self.assertEqual(user_form['first_name'].value(), registrationform['first_name'])
        self.assertEqual(user_form['last_name'].value(), registrationform['last_name'])
        self.assertEqual(user_form['password1'].value(), registrationform['password1'])
        self.assertEqual(user_form['password2'].value(), registrationform['password2'])

        # lead stuff
        info_form = response.context['info_form']
        self.assertEqual(info_form['gender'].value(), registrationform['gender'])
        self.assertEqual(info_form['major'].value(), registrationform['major'])
        self.assertEqual(info_form['year'].value(), str(registrationform['year']))
        self.assertEqual(info_form['organization_code'].value(), registrationform['organization_code'])


        # Correct error messages gets set
        self.assertEqual(user_form['username'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', user_form['email'].errors.as_text()),
            'Email already in use')
        self.assertEqual(user_form['first_name'].errors.as_text(), '')
        self.assertEqual(user_form['last_name'].errors.as_text(), '')
        self.assertEqual(user_form['password1'].errors.as_text(), '')
        self.assertEqual(user_form['password2'].errors.as_text(), '')
        self.assertEqual(info_form['gender'].errors.as_text(), '')
        self.assertEqual(info_form['major'].errors.as_text(), '')
        self.assertEqual(info_form['year'].errors.as_text(), '')
        self.assertEqual(info_form['organization_code'].errors.as_text(), '')

    def testUserInfoNotValid_PasswordConfirmationFailed(self):
        """
        Verify that submission via POST with a
        failed password confirmation rerenders
        the template and shows an error without
        creating the user account
        """

        # Get the POST dict
        registrationform = Factory.createUserRegistrationPostDict(self.organization)
        registrationform['password2'] = 'incorrect'

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registrationform, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.assertEqual(user_form['username'].value(), registrationform['username'])
        self.assertEqual(user_form['email'].value(), registrationform['email'])
        self.assertEqual(user_form['first_name'].value(), registrationform['first_name'])
        self.assertEqual(user_form['last_name'].value(), registrationform['last_name'])
        self.assertEqual(user_form['password1'].value(), registrationform['password1'])
        self.assertEqual(user_form['password2'].value(), registrationform['password2'])

        # lead stuff
        info_form = response.context['info_form']
        self.assertEqual(info_form['gender'].value(), registrationform['gender'])
        self.assertEqual(info_form['major'].value(), registrationform['major'])
        self.assertEqual(info_form['year'].value(), str(registrationform['year']))
        self.assertEqual(info_form['organization_code'].value(), registrationform['organization_code'])

        # Correct error messages gets set
        self.assertEqual(user_form['username'].errors.as_text(), '')
        self.assertEqual(user_form['email'].errors.as_text(), '')
        self.assertEqual(user_form['first_name'].errors.as_text(), '')
        self.assertEqual(user_form['last_name'].errors.as_text(), '')
        self.assertEqual(user_form['password1'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', user_form['password2'].errors.as_text()),
            'The two password fields didn\'t match.')
        self.assertEqual(info_form['gender'].errors.as_text(), '')
        self.assertEqual(info_form['major'].errors.as_text(), '')
        self.assertEqual(info_form['year'].errors.as_text(), '')
        self.assertEqual(info_form['organization_code'].errors.as_text(), '')

    def testUserInfoNotValid_FieldsLeftBlank(self):
        """
        Verify that all fields fail to validate if
        left blank and that the page rerenders
        without creating the user account
        """
        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            {
                # Lead info
                'gender': 'M',
                'major': 'tester',
                'year': '1',
                'organization_code': self.organization.code
            },
            follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.assertEqual(user_form['username'].value(), None)
        self.assertEqual(user_form['email'].value(), None)
        self.assertEqual(user_form['first_name'].value(), None)
        self.assertEqual(user_form['last_name'].value(), None)
        self.assertEqual(user_form['password1'].value(), None)
        self.assertEqual(user_form['password2'].value(), None)

        # lead stuff
        info_form = response.context['info_form']
        self.assertEqual(info_form['gender'].value(), 'M')
        self.assertEqual(info_form['major'].value(), 'tester')
        self.assertEqual(info_form['year'].value(), '1')
        self.assertEqual(info_form['organization_code'].value(), self.organization.code)

        # Correct error messages gets set
        self.assertEqual(re.sub(r'\* ', '', user_form['username'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', user_form['email'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', user_form['first_name'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', user_form['last_name'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', user_form['password1'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', user_form['password2'].errors.as_text()),
            'This field is required.')
        self.assertEqual(info_form['gender'].errors.as_text(), '')
        self.assertEqual(info_form['major'].errors.as_text(), '')
        self.assertEqual(info_form['year'].errors.as_text(), '')
        self.assertEqual(info_form['organization_code'].errors.as_text(), '')

    def testLEADInfoNotValid_FieldsLeftBlank(self):
        """
        Verify that all fields fail to validate if
        left blank and that the page rerenders
        without creating the user account
        """
        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
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
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.assertEqual(user_form['username'].value(), 'testuser')
        self.assertEqual(user_form['email'].value(), 'testuser@gmail.com')
        self.assertEqual(user_form['first_name'].value(), 'test')
        self.assertEqual(user_form['last_name'].value(), 'user')
        self.assertEqual(user_form['password1'].value(), 'testpass')
        self.assertEqual(user_form['password2'].value(), 'testpass')

        # lead stuff
        info_form = response.context['info_form']
        self.assertEqual(info_form['gender'].value(), None)
        self.assertEqual(info_form['major'].value(), None)
        self.assertEqual(info_form['year'].value(), None)
        self.assertEqual(info_form['organization_code'].value(), None)

        # Correct error messages gets set
        self.assertEqual(user_form['username'].errors.as_text(), '')
        self.assertEqual(user_form['email'].errors.as_text(), '')
        self.assertEqual(user_form['first_name'].errors.as_text(), '')
        self.assertEqual(user_form['last_name'].errors.as_text(), '')
        self.assertEqual(user_form['password1'].errors.as_text(), '')
        self.assertEqual(user_form['password2'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', info_form['gender'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', info_form['major'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', info_form['year'].errors.as_text()),
            'This field is required.')
        self.assertEqual(re.sub(r'\* ', '', info_form['organization_code'].errors.as_text()),
            'This field is required.')

    def testOrganizationCodeInvalid(self):
        """ Verify an invalid organization sends an error """

        # Get the POST dict
        registrationform = Factory.createUserRegistrationPostDict(self.organization)
        registrationform['organization_code'] = 'invalid'

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registrationform, follow = True)

        # Get the forms
        user_form = response.context['user_form']
        info_form = response.context['info_form']

        self.assertEqual(user_form['username'].value(), registrationform['username'])
        self.assertEqual(user_form['email'].value(), registrationform['email'])
        self.assertEqual(user_form['password1'].value(), registrationform['password1']) # Password should be hashed
        self.assertEqual(user_form['first_name'].value(), registrationform['first_name'])
        self.assertEqual(user_form['last_name'].value(), registrationform['last_name'])

        self.assertEqual(info_form['gender'].value(), registrationform['gender'])
        self.assertEqual(info_form['major'].value(), registrationform['major'])
        self.assertEqual(info_form['organization_code'].value(), 'invalid')

        # Correct error messages gets set

        self.assertEqual(user_form['username'].errors.as_text(), '')
        self.assertEqual(user_form['email'].errors.as_text(), '')
        self.assertEqual(user_form['first_name'].errors.as_text(), '')
        self.assertEqual(user_form['last_name'].errors.as_text(), '')
        self.assertEqual(user_form['password1'].errors.as_text(), '')
        self.assertEqual(user_form['password2'].errors.as_text(), '')

        self.assertEqual(info_form['gender'].errors.as_text(), '')
        self.assertEqual(info_form['major'].errors.as_text(), '')
        self.assertEqual(info_form['year'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', info_form['organization_code'].errors.as_text()),
            'Invalid organization code.')

    def testValidInfo(self):
        """
        Verify that submission of valid information
        creates the user account, the lead info,
        logs the user in, sets a success message,
        and redirects to the index view
        """

        # Get the POST dict
        registrationform = Factory.createUserRegistrationPostDict(self.organization)

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registrationform, follow = True)

        # Verify the user account is created with correct attributes
        user = User.objects.get(username = registrationform['username'])
        info = LeadUserInfo.objects.get(user = user)

        self.assertTrue(user is not None)
        self.assertEqual(user.username, registrationform['username'])
        self.assertEqual(user.email, registrationform['email'])
        self.assertNotEqual(user.password, registrationform['password1']) # Password should be hashed
        self.assertEqual(user.first_name, registrationform['first_name'])
        self.assertEqual(user.last_name, registrationform['last_name'])

        self.assertTrue(info is not None)
        self.assertEqual(info.user, user)
        self.assertEqual(info.gender, registrationform['gender'])
        self.assertEqual(info.major, registrationform['major'])
        self.assertEqual(info.organization, self.organization)

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

    def setUp(self):
        """
        Set up user account for testing
        """

        # Create the user
        User.objects.create_user(username = 'test', password='pass', email = 'test@gmail.com')

    def testLogoutRequired(self):
        """
        Verify a user must be logged out
        before navigating to the page
        """

        # Login
        self.client.login(username = 'test', password = 'pass')

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
        response = self.client.post('/reset_password', {'email': 'test@gmail.com'}, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/reset_password_page.html')

        # Verify the form and success are passed to the response
        self.assertTrue('form' in response.context)
        self.assertTrue('success' in response.context)

        self.assertTrue(response.context['success'])

class testMainViews_Logout(TestCase):
    """
    Test case for the logout view
    """

    def testLoginRequired(self):
        """
        Verify the view does not load if logged out
        """

        # Make the get reqeust
        response = self.client.get('/logout', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/login')

    def testLogout(self):
        # Create an account and log in
        User.objects.create_user(username = 'test', password='pass', email = 'test@gmail.com')
        self.client.login(username = 'test', password = 'pass')

        # Make the get reqeust
        response = self.client.get('/logout', follow = True)

        # Verify redirect
        self.assertRedirects(response, '/login')

class testMainViews_PageNotFound(TestCase):
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
        User.objects.create_user(username = 'test', password='pass', email = 'test@gmail.com')
        self.client.login(username = 'test', password = 'pass')

        # Make the GET request
        response = self.client.get('/unsupportedpage', follow = True)

        # Verify template
        self.assertTemplateUsed(response, 'page_not_found.html')
