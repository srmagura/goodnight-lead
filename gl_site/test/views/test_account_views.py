# Import test case
from django.test import TestCase

# Object factory for testing
from gl_site.test.Factory import Factory

# Regex parser
import re

class testAccountViews_AccountSettings(TestCase):
    """ Test class for verifying the account settings view """


    def setUp(self):
        """ Set Up
            Create a user account and user info
            to be used for testing
        """
        self.user = Factory.createUser()

        self.organization = Factory.createOrganization(self.user)

        self.session = Factory.createSession(self.organization, self.user)

        self.info = Factory.createDemographics(self.user, self.organization, self.session)

    def testLoginRequired(self):
        """ Account Settings - Log in required.
            Verify that the user cannot navigate to this page
            if not logged in.
        """
        # Make a GET request of the view
        response = self.client.get('/account-settings', follow = True)

        # Verify view redirects to the homepage
        self.assertRedirects(response, '/home')

    def testViewLoadsWithLogin(self):
        """ Account Settings - View loads with login.
            Verify that the view loads when logged in
            and that all the provided information is
            present and correct.
        """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the GET request
        response = self.client.get('/account-settings', follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        userform = response.context['user_form']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), self.user.username)

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), self.user.email)

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), self.user.first_name)

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), self.user.last_name)

        # Validate field values in info_form
        info_form = response.context['info_form']

        self.assertTrue('user' not in info_form.fields)

        self.assertTrue('gender' in info_form.fields)
        self.assertEqual(info_form['gender'].value(), self.info.gender)

        self.assertTrue('major' in info_form.fields)
        self.assertEqual(info_form['major'].value(), self.info.major)

        self.assertTrue('year' in info_form.fields)
        self.assertEqual(info_form['year'].value(), self.info.year)

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)
        self.assertEqual(response.context['session'].name, self.session.name)

    def testUsernameNotUnique(self):
        """ Account Settings - Username not unique.
            Verify that attempting to change to a username
            already in use rerenders the page with a form
            error.
        """

        # Create a second user
        user2 = Factory.createUser()
        Factory.createDemographics(user2, self.organization, self.session)

        # Log in as the first user
        self.client.login(username = self.user, password = Factory.defaultPassword)

        # Get the post info and change username
        settingsform = Factory.createUserSettingsPostDict(self.user, self.info)
        settingsform['username'] = user2.username

        # Make the POST request
        response = self.client.post('/account-settings', settingsform, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        userform = response.context['user_form']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), user2.username)
        self.assertEqual(re.sub(r'\* ', '', userform['username'].errors.as_text()),
            'A user with that username already exists.')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), self.user.email)
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), self.user.first_name)
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), self.user.last_name)
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in info_form
        info_form = response.context['info_form']

        self.assertTrue('user' not in info_form.fields)

        self.assertTrue('gender' in info_form.fields)
        self.assertEqual(info_form['gender'].value(), self.info.gender)
        self.assertEqual(info_form['gender'].errors.as_text(), '')

        self.assertTrue('major' in info_form.fields)
        self.assertEqual(info_form['major'].value(), self.info.major)
        self.assertEqual(info_form['major'].errors.as_text(), '')

        self.assertTrue('year' in info_form.fields)
        self.assertEqual(info_form['year'].value(), str(self.info.year))
        self.assertEqual(info_form['year'].errors.as_text(), '')

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)
        self.assertEqual(response.context['session'].name, self.session.name)

    def testEmailNotUnique(self):
        """ Account Settings - Email already taken.
            Verify that attempting to change to an email
            already in use rerenders the page with a form
            error.
        """

        # Create a second user
        user2 = Factory.createUser()
        Factory.createDemographics(user2, self.organization, self.session)

        # Log in as the first user
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Get the post dict and set email not unique
        settingsform = Factory.createUserSettingsPostDict(self.user, self.info)
        settingsform['email'] = user2.email

        # Make the POST request
        response = self.client.post('/account-settings', settingsform, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        userform = response.context['user_form']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), self.user.username)
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertNotEquals(userform['email'].value(), self.user.email)
        self.assertEquals(userform['email'].value(), user2.email)
        self.assertEqual(re.sub(r'\* ', '', userform['email'].errors.as_text()),
            'Email already in use')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), self.user.first_name)
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), self.user.last_name)
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in info_form
        info_form = response.context['info_form']

        self.assertTrue('user' not in info_form.fields)

        self.assertTrue('gender' in info_form.fields)
        self.assertEqual(info_form['gender'].value(), self.info.gender)
        self.assertEqual(info_form['gender'].errors.as_text(), '')

        self.assertTrue('major' in info_form.fields)
        self.assertEqual(info_form['major'].value(), self.info.major)
        self.assertEqual(info_form['major'].errors.as_text(), '')

        self.assertTrue('year' in info_form.fields)
        self.assertEqual(info_form['year'].value(), str(self.info.year))
        self.assertEqual(info_form['year'].errors.as_text(), '')

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)
        self.assertEqual(response.context['session'].name, self.session.name)

    def testGenderNotValid(self):
        """ Account Settings - Gender not valid.
            Verify that submitting a POST request with an
            invalid gender choice rerenders the page with
            a form error.
        """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Get the post dict and change gender choice
        settingsform = Factory.createUserSettingsPostDict(self.user, self.info)
        settingsform['gender'] = 'i'

        # Make the POST request
        response = self.client.post('/account-settings', settingsform, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        userform = response.context['user_form']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), self.user.username)
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), self.user.email)
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), self.user.first_name)
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), self.user.last_name)
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in info_form
        info_form = response.context['info_form']

        self.assertTrue('user' not in info_form.fields)

        self.assertTrue('gender' in info_form.fields)
        self.assertEqual(info_form['gender'].value(), 'i')
        self.assertEqual(re.sub(r'\* ', '', info_form['gender'].errors.as_text()),
            'Select a valid choice. i is not one of the available choices.')

        self.assertTrue('major' in info_form.fields)
        self.assertEqual(info_form['major'].value(), self.info.major)
        self.assertEqual(info_form['major'].errors.as_text(), '')

        self.assertTrue('year' in info_form.fields)
        self.assertEqual(info_form['year'].value(), str(self.info.year))
        self.assertEqual(info_form['year'].errors.as_text(), '')

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)
        self.assertEqual(response.context['session'].name, self.session.name)

    def testYearNotValid(self):
        """ Account Settings - Year not valid.
            Verify that submitting an invalid year
            kicks back an error
        """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Create the post dict and set year
        settingsform = Factory.createUserSettingsPostDict(self.user, self.info)
        settingsform['year'] = -1

        # Make the POST request
        response = self.client.post('/account-settings', settingsform, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        userform = response.context['user_form']

        self.assertTrue('username' in userform.fields)
        self.assertEquals(userform['username'].value(), self.user.username)
        self.assertEqual(userform['username'].errors.as_text(), '')

        self.assertTrue('email' in userform.fields)
        self.assertEquals(userform['email'].value(), self.user.email)
        self.assertEqual(userform['email'].errors.as_text(), '')

        self.assertTrue('first_name' in userform.fields)
        self.assertEquals(userform['first_name'].value(), self.user.first_name)
        self.assertEqual(userform['first_name'].errors.as_text(), '')

        self.assertTrue('last_name' in userform.fields)
        self.assertEquals(userform['last_name'].value(), self.user.last_name)
        self.assertEqual(userform['last_name'].errors.as_text(), '')

        # Validate field values in info_form
        info_form = response.context['info_form']

        self.assertTrue('user' not in info_form.fields)

        self.assertTrue('gender' in info_form.fields)
        self.assertEqual(info_form['gender'].value(), self.info.gender)
        self.assertEqual(info_form['gender'].errors.as_text(), '')

        self.assertTrue('major' in info_form.fields)
        self.assertEqual(info_form['major'].value(), self.info.major)
        self.assertEqual(info_form['major'].errors.as_text(), '')

        self.assertTrue('year' in info_form.fields)
        self.assertEqual(info_form['year'].value(), '-1')
        self.assertEqual(re.sub(r'\* ', '', info_form['year'].errors.as_text()),
            'Select a valid choice. -1 is not one of the available choices.')

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)

    def testValidSubmission(self):
        """ Account Settings - Valid submission.
            Verify that a valid submission updates the
            user and info, sets a success message,
            and redirects to the index page.
        """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the POST request
        response = self.client.post('/account-settings', {
                # User fields
                'username': 'unique01',
                'email': 'unique01@gmail.com',
                'first_name': 'unique01',
                'last_name': 'user01',

                # Info fields
                'gender': 'F',
                'major': 'Original Major',
                'year': 4,
            }, follow = True)

        # Verify redirected to index
        self.assertRedirects(response, '/')

        # Verify message is set
        self.assertEqual(len(response.context['messages']), 1)
        for message in response.context['messages']:
            self.assertEqual(message.message, 'Account Settings updated successfully')

        # Verify user
        user = response.context['user']
        self.assertEqual(user.username, 'unique01')
        self.assertEqual(user.email, 'unique01@gmail.com')
        self.assertEqual(user.first_name, 'unique01')
        self.assertEqual(user.last_name, 'user01')

        # Verify info
        info = user.leaduserinfo
        self.assertEqual(info.gender, 'F')
        self.assertEqual(info.major, 'Original Major')
        self.assertEqual(info.year, 4)
        self.assertEqual(info.organization, self.organization)
        self.assertEqual(info.session, self.session)

class testAccountViews_Password(TestCase):
    """ Test class for the change password view """

    def setUp(self):
        """ Password - Set up.
            Set up a user account for testing.
        """

        self.user = Factory.createUser()

        self.organization = Factory.createOrganization(self.user)

        self.session = Factory.createSession(self.organization, self.user)

        self.info = Factory.createDemographics(self.user, self.organization, self.session)

    def testLoginRequired(self):
        """ Password - Log in required.
            Verify a user must be logged in to get to the page.
        """

        # Make the GET request
        response = self.client.get('/account-settings/password', follow = True)

        # Verify redirects to the homepage
        self.assertRedirects(response, '/home')

    def testGETRequest(self):
        """ Password - GET request
            Verify the view loads the correct form
            on a GET request.
        """

        # Login
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

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
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the POST request
        response = self.client.post('/account-settings/password', {
                'password1': Factory.defaultPassword,
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

        self.assertEqual(form['password1'].value(), Factory.defaultPassword)
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
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the POST request
        response = self.client.post('/account-settings/password', {
                'password1': 'new',
                'password2': 'new'
            }, follow = True)

        # Verify redirected to the account-settings page
        self.assertRedirects(response, '/account-settings')

        # Verify messages
        self.assertEqual(len(response.context['messages']), 1)
        for message in response.context['messages']:
            self.assertEqual(message.message, "Password set successfully")

        # Verify user password changed
        self.client.logout()
        self.assertTrue(self.client.login(username = self.user.username, password = 'new'))
