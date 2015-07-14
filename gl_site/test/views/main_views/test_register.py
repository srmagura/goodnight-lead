# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

# Object factory
from gl_site.test.Factory import Factory

# Import use info for testing account creation
from gl_site.models import LeadUserInfo

# Regex parser
import re

# Date utilities
from datetime import date

class TestRegister(TestCase):
    """ Test method for register view """

    def setUp(self):
        """ Create user account for testing """
        self.user, self.info = Factory.createUser()
        self.organization = self.info.organization
        self.session = self.info.session

    def testLogoutRequired(self):
        """ A logged in user cannot access this page """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the response
        response = self.client.get('/register/{}'.format(self.info.session.uuid), follow = True)

        # Sanity check
        self.assertTrue(response.context['user'].is_authenticated())

        # Verify redirect to dashboard
        self.assertTemplateUsed(response, 'dashboard.html')

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
        self.assertEqual(info_form['graduation_date'].value(), str(registrationform['graduation_date']))
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
        self.assertEqual(info_form['graduation_date'].errors.as_text(), '')
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
        self.assertEqual(info_form['graduation_date'].value(), str(registrationform['graduation_date']))
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
        self.assertEqual(info_form['graduation_date'].errors.as_text(), '')
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
        self.assertEqual(info_form['graduation_date'].value(), str(registrationform['graduation_date']))
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
        self.assertEqual(info_form['graduation_date'].errors.as_text(), '')
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
                'major': LeadUserInfo.OTHER,
                'graduation_date': date.today(),
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
        self.assertEqual(info_form['major'].value(), LeadUserInfo.OTHER)
        self.assertEqual(info_form['graduation_date'].value(), str(date.today()))
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
        self.assertEqual(info_form['graduation_date'].errors.as_text(), '')
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
        self.assertEqual(info_form['graduation_date'].value(), None)
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
        self.assertEqual(re.sub(r'\* ', '', info_form['graduation_date'].errors.as_text()),
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
        self.assertEqual(info_form['graduation_date'].errors.as_text(), '')
        self.assertEqual(re.sub(r'\* ', '', info_form['organization_code'].errors.as_text()),
            'Invalid organization code.')

    def testValidInfo(self):
        """
        Verify that submission of valid information
        creates the user account, the lead info,
        logs the user in, sets a success message,
        and redirects to the dashboard view
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

        # Verify the user is redirected to the dashboard
        self.assertTemplateUsed(response, 'dashboard.html')
