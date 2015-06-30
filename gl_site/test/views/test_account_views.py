# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

# Import user info
from gl_site.models import LeadUserInfo, Organization

# Regex parser
import re

class testAccountViews_AccountSettings(TestCase):
    """ Test class for verifying the account settings view """


    def setUp(self):
        """ Set Up
            Create a user account and user info
            to be used for testing
        """
        self.user = User.objects.create_user(username = 'test', email='test@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        self.organization = Organization.objects.create(name = "Testers", code = "secret")

        self.info = LeadUserInfo.objects.create(user = self.user, gender = 'M',
            major = 'Tester', year = 1, organization = self.organization)

    def testLoginRequired(self):
        """ Account Settings - Log in required.
            Verify that the user cannot navigate to this page
            if not logged in.
        """
        # Make a GET request of the view
        response = self.client.get('/account-settings', follow = True)

        # Verify view redirects to the login page
        self.assertRedirects(response, '/login')

    def testViewLoadsWithLogin(self):
        """ Account Settings - View loads with login.
            Verify that the view loads when logged in
            and that all the provided information is
            present and correct.
        """

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the GET request
        response = self.client.get('/account-settings', follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test@gmail.com')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), 'test')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), 'user')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), 'M')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), 'Tester')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), 1)

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), self.organization.name)
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), self.organization.code)
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

    def testUsernameNotUnique(self):
        """ Account Settings - Username not unique.
            Verify that attempting to change to a username
            already in use rerenders the page with a form
            error.
        """

        # Create a second user
        user = User.objects.create_user(username = 'test02', email='test02@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        LeadUserInfo.objects.create(user = user, gender = 'F',
            major = 'Tester', year = 2, organization = self.organization)

        # Log in as the first user
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test02', # Non unique username
                'email': 'test@gmail.com',
                'first_name': 'test',
                'last_name': 'user',

                # Info fields
                'gender': 'M',
                'major': 'Tester',
                'year': 1,
                'organization_name': 'Testers',
                'organization_code': 'secret'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test02')
        self.assertEqual(re.sub(r'\* ', '', userform['username'].errors.as_text()),
            'A user with that username already exists.')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test@gmail.com')
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), 'test')
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), 'user')
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['gender'].errors.as_text(), '')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), 'Tester')
        self.assertEqual(infoform['major'].errors.as_text(), '')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['year'].errors.as_text(), '')

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), self.organization.name)
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), self.organization.code)
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

    def testEmailNotUnique(self):
        """ Account Settings - Email already taken.
            Verify that attempting to change to an email
            already in use rerenders the page with a form
            error.
        """

        # Create a second user
        user = User.objects.create_user(username = 'test02', email='test02@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        LeadUserInfo.objects.create(user = user, gender = 'F', major = 'Tester', year = 2, organization = self.organization)

        # Log in as the first user
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test',
                'email': 'test02@gmail.com', # Non unique email
                'first_name': 'test',
                'last_name': 'user',

                # Info fields
                'gender': 'M',
                'major': 'Tester',
                'year': 1,
                'organization_name': 'Testers',
                'organization_code': 'secret'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), self.user.username)
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertNotEquals(userform['email'].value(), self.user.email)
        self.assertEquals(userform['email'].value(), 'test02@gmail.com')
        self.assertEqual(re.sub(r'\* ', '', userform['email'].errors.as_text()),
            'Email already in use')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), self.user.first_name)
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), self.user.last_name)
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), self.info.gender)
        self.assertEqual(infoform['gender'].errors.as_text(), '')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), self.info.major)
        self.assertEqual(infoform['major'].errors.as_text(), '')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), str(self.info.year))
        self.assertEqual(infoform['year'].errors.as_text(), '')

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), self.organization.name)
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), self.organization.code)
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

    def testGenderNotValid(self):
        """ Account Settings - Gender not valid.
            Verify that submitting a POST request with an
            invalid gender choice rerenders the page with
            a form error.
        """

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test',
                'email': 'test@gmail.com',
                'first_name': 'test',
                'last_name': 'user',

                # Info fields
                'gender': 'NA',
                'major': 'Tester',
                'year': 1,
                'organization_name': 'Testers',
                'organization_code': 'secret'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test')
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test@gmail.com')
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), 'test')
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), 'user')
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), 'NA')
        self.assertEqual(re.sub(r'\* ', '', infoform['gender'].errors.as_text()),
            'Select a valid choice. NA is not one of the available choices.')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), 'Tester')
        self.assertEqual(infoform['major'].errors.as_text(), '')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['year'].errors.as_text(), '')

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), self.organization.name)
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), self.organization.code)
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

    def testYearNotValid(self):
        """ Account Settings - Year not valid.
            Verify that submitting an invalid year
            kicks back an error
        """

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test',
                'email': 'test@gmail.com',
                'first_name': 'test',
                'last_name': 'user',

                # Info fields
                'gender': 'M',
                'major': 'Tester',
                'year': 0,
                'organization_name': 'Testers',
                'organization_code': 'secret'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test')
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test@gmail.com')
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), 'test')
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), 'user')
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['gender'].errors.as_text(), '')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), 'Tester')
        self.assertEqual(infoform['major'].errors.as_text(), '')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), '0')
        self.assertEqual(re.sub(r'\* ', '', infoform['year'].errors.as_text()),
            'Select a valid choice. 0 is not one of the available choices.')

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), self.organization.name)
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), self.organization.code)
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

    def testOrganizationNameNotValid(self):
        """ Account Settings - Organization name not vaild.
            Verify an error is shown if the selected
            organization does not exist.
        """
        # TODO split into organization_name and organization_code

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test',
                'email': 'test@gmail.com',
                'first_name': 'test',
                'last_name': 'user',

                # Info fields
                'gender': 'M',
                'major': 'Tester',
                'year': 1,
                'organization_name': 'Not Valid',
                'organization_code': 'secret'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test')
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test@gmail.com')
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), 'test')
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), 'user')
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['gender'].errors.as_text(), '')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), 'Tester')
        self.assertEqual(infoform['major'].errors.as_text(), '')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['year'].errors.as_text(), '')

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), 'Not Valid')
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), self.organization.code)
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

        self.assertEqual(re.sub(r'\* ', '', infoform.non_field_errors()[0]),
            'Organization name or code not recognized')

    def testOrganizationCodeNotValid(self):
        """ Account Settings - Organization code not vaild.
            Verify an error is shown if the selected
            organization code does not match the actual.
        """
        # TODO split into organization_name and organization_code

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test',
                'email': 'test@gmail.com',
                'first_name': 'test',
                'last_name': 'user',

                # Info fields
                'gender': 'M',
                'major': 'Tester',
                'year': 1,
                'organization_name': 'Testers',
                'organization_code': 'notvalid'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test')
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test@gmail.com')
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), 'test')
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), 'user')
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in infoform
        infoform = response.context['infoform']

        self.assertTrue('user' not in infoform.fields)

        self.assertTrue('gender' in infoform.fields)
        self.assertEqual(infoform['gender'].value(), 'M')
        self.assertEqual(infoform['gender'].errors.as_text(), '')

        self.assertTrue('major' in infoform.fields)
        self.assertEqual(infoform['major'].value(), 'Tester')
        self.assertEqual(infoform['major'].errors.as_text(), '')

        self.assertTrue('year' in infoform.fields)
        self.assertEqual(infoform['year'].value(), '1')
        self.assertEqual(infoform['year'].errors.as_text(), '')

        self.assertTrue('organization_name' in infoform.fields)
        self.assertEqual(infoform['organization_name'].value(), self.organization.name)
        self.assertEqual(infoform['organization_name'].errors.as_text(), '')

        self.assertTrue('organization_code' in infoform.fields)
        self.assertEqual(infoform['organization_code'].value(), 'notvalid')
        self.assertEqual(infoform['organization_code'].errors.as_text(), '')

        self.assertEqual(re.sub(r'\* ', '', infoform.non_field_errors()[0]),
            'Organization name or code not recognized')

    def testValidSubmission(self):
        """ Account Settings - Valid submission.
            Verify that a valid submission updates the
            user and info, sets a success message,
            and redirects to the index page.
        """

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'test02',
                'email': 'test02@gmail.com',
                'first_name': 'test02',
                'last_name': 'user02',

                # Info fields
                'gender': 'F',
                'major': 'Tester',
                'year': 1,
                'organization_name': 'Testers',
                'organization_code': 'secret'
            }, follow = True)

        # Verify redirected to index
        self.assertRedirects(response, '/')

        # Verify message is set
        self.assertEqual(len(response.context['messages']), 1)
        for message in response.context['messages']:
            self.assertEqual(message.message, 'Account Settings updated successfully')

        # Verify user
        user = response.context['user']
        self.assertEqual(user.username, 'test02')
        self.assertEqual(user.email, 'test02@gmail.com')
        self.assertEqual(user.first_name, 'test02')
        self.assertEqual(user.last_name, 'user02')

        # Verify info
        info = user.leaduserinfo
        self.assertEqual(info.gender, 'F')
        self.assertEqual(info.major, 'Tester')
        self.assertEqual(info.year, 1)
        self.assertEqual(info.organization, self.organization)

class testAccountViews_Password(TestCase):
    """ Test class for the change password view """

    def setUp(self):
        """ Password - Set up.
            Set up a user account for testing.
        """

        self.user = User.objects.create_user(username = 'test', email='test@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        self.organization = Organization.objects.create(name = "Testers", code = "secret")

        self.info = LeadUserInfo.objects.create(user = self.user, gender = 'M',
            major = 'Tester', year = 1, organization = self.organization)

    def testLoginRequired(self):
        """ Password - Log in required.
            Verify a user must be logged in to get to the page.
        """

        # Make the GET request
        response = self.client.get('/account-settings/password', follow = True)

        # Verify redirects to the login page
        self.assertRedirects(response, '/login')

    def testGETRequest(self):
        """ Password - GET request
            Verify the view loads the correct form
            on a GET request.
        """

        # Login
        self.client.login(username = 'test', password = 'pass')

        # Make the GET request
        response = self.client.get('/account-settings/password', follow = True)

        # Verify the correct template was rendered
        self.assertTemplateUsed(response, 'user/password.html')

        # Verify the form exists in the response context
        self.assertTrue('form' in response.context)

        # Verify form fields
        form = response.context['form']

        self.assertTrue('password1' in form.fields)
        self.assertTrue('password2' in form.fields)

        self.assertEqual(form['password1'].value(), None)
        self.assertEqual(form['password2'].value(), None)

        self.assertEqual(form['password1'].errors.as_text(), '')
        self.assertEqual(form['password2'].errors.as_text(), '')

    def testMismatchedPasswords(self):
        """ Password - Mismatched passwords.
            Verify mismatched passwords throws an error.
        """

        # Login
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings/password', {
                'password1': 'password',
                'password2': 'wrong'
            }, follow = True)

        # Verify the correct template was rendered
        self.assertTemplateUsed(response, 'user/password.html')

        # Verify the form exists in the response context
        self.assertTrue('form' in response.context)

        # Verify form fields
        form = response.context['form']

        self.assertTrue('password1' in form.fields)
        self.assertTrue('password2' in form.fields)

        self.assertEqual(form['password1'].value(), 'password')
        self.assertEqual(form['password2'].value(), 'wrong')

        self.assertEqual(form['password1'].errors.as_text(), '')
        self.assertEqual(form['password2'].errors.as_text(), '')

        # Verify form errors
        self.assertEqual(form.errors['__all__'][0], "Passwords did not match")

    def testValidInput(self):
        """ Password - Valid input.
            Test submitting matching, valid, passwords.
        """

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings/password', {
                'password1': 'password',
                'password2': 'password'
            }, follow = True)

        # Verify redirected to the account-settings page
        self.assertRedirects(response, '/account-settings')

        # Verify messages
        self.assertEqual(len(response.context['messages']), 1)
        for message in response.context['messages']:
            self.assertEqual(message.message, "Password set successfully")

        # Verify user password changed
        self.client.logout()
        self.assertTrue(self.client.login(username = 'test', password = 'password'))
