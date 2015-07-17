# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

# Object factory
from gl_site.test.factory import Factory

# Import use info for testing account creation
from gl_site.models import LeadUserInfo

# Regex parser
import re

# Date utilities
from datetime import date

# Common validation
from gl_site.test.form_validation import AccountFormValidator

class TestRegister(TestCase, AccountFormValidator):
    """ Test method for register view """

    def setUp(self):
        """ Create user account for testing """
        self.user, self.info = Factory.create_user()
        self.organization = self.info.organization
        self.session = self.info.session

    def testLogoutRequired(self):
        """ A logged in user cannot access this page """

        # Log in
        self.client.login(username = self.user.username, password = Factory.default_password)

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
        registration_form = Factory.create_user_registration_post_dict(self.organization)
        registration_form['username'] = self.user.username

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        info_form = response.context['info_form']

        # Validate
        self.validate_form(user_form, registration_form, ('username'))
        self.validate_form(info_form, registration_form, ())

    def testUserInfoNotValid_EmailNotUnique(self):
        """
        Verify that submission via POST with an
        email that is already in use rerenders
        the template and shows an error without
        creating the user account
        """

        # Get the POST dict
        registration_form = Factory.create_user_registration_post_dict(self.organization)
        registration_form['email'] = self.user.email

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.validate_form(user_form, registration_form, ('email'))

        # lead stuff
        info_form = response.context['info_form']
        self.validate_form(info_form, registration_form, ())

    def testUserInfoNotValid_PasswordConfirmationFailed(self):
        """
        Verify that submission via POST with a
        failed password confirmation rerenders
        the template and shows an error without
        creating the user account
        """

        # Get the POST dict
        registration_form = Factory.create_user_registration_post_dict(self.organization)
        registration_form['password2'] = 'incorrect'

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.validate_form(user_form, registration_form, ('password2'))

        # lead stuff
        info_form = response.context['info_form']
        self.validate_form(info_form, registration_form, ())

    def testUserInfoNotValid_FieldsLeftBlank(self):
        """
        Verify that all fields fail to validate if
        left blank and that the page rerenders
        without creating the user account
        """

        registration_form = {
            # Lead info
            'gender': 'M',
            'major': LeadUserInfo.OTHER,
            'education': 'FR',
            'graduation_date': str(date.today()),
            'organization_code': self.organization.code
        }

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        for field in user_form:
            self.assertEqual(field.value(), None)
            self.assertEqual(re.sub(r'\* ', '', field.errors.as_text()),
                'This field is required.')

        # lead stuff
        info_form = response.context['info_form']
        self.validate_form(info_form, registration_form, ())

    def testLEADInfoNotValid_FieldsLeftBlank(self):
        """
        Verify that all fields fail to validate if
        left blank and that the page rerenders
        without creating the user account
        """

        registration_form = {
            # User info
            'username': 'testuser',
            'email': 'testuser@gmail.com',
            'password1': 'testpass',
            'password2': 'testpass',
            'first_name': 'test',
            'last_name': 'user'
        }

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Verify that the register page was rendered
        self.assertTemplateUsed(response, 'user/register.html')

        # Verify both forms are included in the response
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Verify form fields retain their set values
        user_form = response.context['user_form']
        self.validate_form(user_form, registration_form, ())

        # lead stuff
        info_form = response.context['info_form']
        for field in info_form:
            self.assertEqual(field.value(), None)
            self.assertEqual(re.sub(r'\* ', '', field.errors.as_text()),
                'This field is required.')

    def testOrganizationCodeInvalid(self):
        """ Verify an invalid organization sends an error """

        # Get the POST dict
        registration_form = Factory.create_user_registration_post_dict(self.organization)
        registration_form['organization_code'] = 'invalid'

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Get the forms
        user_form = response.context['user_form']
        self.validate_form(user_form, registration_form, ())

        info_form = response.context['info_form']
        self.validate_form(info_form, registration_form, ('organization_code'))

    def testValidInfo(self):
        """
        Verify that submission of valid information
        creates the user account, the lead info,
        logs the user in, sets a success message,
        and redirects to the dashboard view
        """

        # Get the POST dict
        registration_form = Factory.create_user_registration_post_dict(self.organization)

        # Make the post request
        response = self.client.post('/register/{}'.format(self.info.session.uuid),
            registration_form, follow = True)

        # Verify the user account is created with correct attributes
        user = User.objects.get(username = registration_form['username'])
        info = LeadUserInfo.objects.get(user = user)

        self.assertTrue(user is not None)
        self.assertEqual(user.username, registration_form['username'])
        self.assertEqual(user.email, registration_form['email'])
        self.assertNotEqual(user.password, registration_form['password1']) # Password should be hashed
        self.assertEqual(user.first_name, registration_form['first_name'])
        self.assertEqual(user.last_name, registration_form['last_name'])

        self.assertTrue(info is not None)
        self.assertEqual(info.user, user)
        self.assertEqual(info.gender, registration_form['gender'])
        self.assertEqual(info.major, registration_form['major'])
        self.assertEqual(info.organization, self.organization)

        # Verify success message set
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        for message in messages:
            self.assertEqual(message.message, "User account created successfully.")

        # Verify the user is redirected to the dashboard
        self.assertTemplateUsed(response, 'dashboard.html')
