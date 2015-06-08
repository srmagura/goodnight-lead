# Import test case
from django.test import TestCase

# Import user for authentication
from django.contrib.auth.models import User

# Import user info
from app.models import LeadUserInfo

# Regex parser
import re

class testAccountViews_AccountSettings(TestCase):
    """
    Test class for verifying the account settings view
    """

    def setUp(self):
        """
        Set up by creating a user account and user info
        to be used for testing
        """
        user = User.objects.create_user(username = 'test', email='test@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        LeadUserInfo.objects.create(user = user, gender = 'M',
            major = 'Tester', year = 1, organization = 'gsp')

    def testLoginRequired(self):
        """
        Verify that the user cannot navigate to this page
        if not logged in
        """
        # Make a GET request of the view
        response = self.client.get('/account-settings', follow = True)

        # Verify view redirects to the login page
        self.assertRedirects(response, '/login')

    def testViewLoadsWithLogin(self):
        """
        Verify that the view loads when logged in
        and that all the provided information is
        present and correct
        """

        # Log in
        self.client.login(username = 'test', password = 'pass')

        # Make the GET request
        response = self.client.get('/account-settings', follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user_templates/account_settings.html')

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

        self.assertTrue('organization' in infoform.fields)
        self.assertEqual(infoform['organization'].value(), 'gsp')

    def testUsernameNotUnique(self):
        """
        Verify that attempting to change to a username
        already in use rerenders the page with a form
        error
        """

        # Create a second user
        user = User.objects.create_user(username = 'test02', email='test02@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        LeadUserInfo.objects.create(user = user, gender = 'F',
            major = 'Tester', year = 2, organization = 'gsp')

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
                'organization': 'gsp'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user_templates/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test02')
        self.assertEqual(re.sub(r'\* ', '', userform['username'].errors.as_text()),
            'User with this Username already exists.')

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

        self.assertTrue('organization' in infoform.fields)
        self.assertEqual(infoform['organization'].value(), 'gsp')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testEmailNotUnique(self):
        """
        Verify that attempting to change to an email
        already in use rerenders the page with a form
        error
        """

        # Create a second user
        user = User.objects.create_user(username = 'test02', email='test02@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        LeadUserInfo.objects.create(user = user, gender = 'F',
            major = 'Tester', year = 2, organization = 'gsp')

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
                'organization': 'gsp'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user_templates/account_settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('usersettingsform' in response.context)
        self.assertTrue('infoform' in response.context)

        # Validate field values in usersettingsform
        userform = response.context['usersettingsform']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), 'test')
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), 'test02@gmail.com')
        self.assertEqual(re.sub(r'\* ', '', userform['email'].errors.as_text()),
            'Email already in use')

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

        self.assertTrue('organization' in infoform.fields)
        self.assertEqual(infoform['organization'].value(), 'gsp')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testGenderNotValid(self):
        """
        Verify that submitting a POST request with an
        invalid gender choice rerenders the page with
        a form error
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
                'organization': 'gsp'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user_templates/account_settings.html')

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

        self.assertTrue('organization' in infoform.fields)
        self.assertEqual(infoform['organization'].value(), 'gsp')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testYearNotValid(self):
        """
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
                'organization': 'gsp'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user_templates/account_settings.html')

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

        self.assertTrue('organization' in infoform.fields)
        self.assertEqual(infoform['organization'].value(), 'gsp')
        self.assertEqual(infoform['organization'].errors.as_text(), '')

    def testOrganizationNotValid(self):
        """
        Verify an error is shown if the selected
        organization is not in the list of choices
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
                'year': 1,
                'organization': 'NA'
            }, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user_templates/account_settings.html')

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

        self.assertTrue('organization' in infoform.fields)
        self.assertEqual(infoform['organization'].value(), 'NA')
        self.assertEqual(re.sub(r'\* ', '', infoform['organization'].errors.as_text()),
            'Select a valid choice. NA is not one of the available choices.')

    def testValidSubmission(self):
        """
        Verify that a valid submission updates the
        user and info, sets a success message,
        and redirects to the index page
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
                'organization': 'gsp'
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
        self.assertEqual(info.organization, 'gsp')

class testAccountViews_Password(TestCase):
    """
    Test class for the change password view
    """

    def setUp(self):
        """
        Set up a user account for testing
        """

        user = User.objects.create_user(username = 'test', email='test@gmail.com',
            password='pass', first_name = 'test', last_name = 'user')

        LeadUserInfo.objects.create(user = user, gender = 'M',
            major = 'Tester', year = 1, organization = 'gsp')

    def testLoginRequired(self):
        """
        Verify a user must be logged in to get to the page
        """

        # Make the GET request
        response = self.client.get('/account-settings/password', follow = True)

        # Verify redirects to the login page
        self.assertRedirects(response, '/login')

    def testGETRequest(self):
        """
        Verify the view loads the correct form
        on a GET request
        """

        # Login
        self.client.login(username = 'test', password = 'pass')

        # Make the GET request
        response = self.client.get('/account-settings/password', follow = True)

        # Verify the correct template was rendered
        self.assertTemplateUsed(response, 'user_templates/password.html')

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
        """
        Verify mismatched passwords throws an error
        """

        # Login
        self.client.login(username = 'test', password = 'pass')

        # Make the POST request
        response = self.client.post('/account-settings/password', {
                'password1': 'password',
                'password2': 'wrong'
            }, follow = True)

        # Verify the correct template was rendered
        self.assertTemplateUsed(response, 'user_templates/password.html')

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
        """
        Test submitting matching, valid, passwords
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
