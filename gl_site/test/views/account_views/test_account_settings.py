# Import test case
from django.test import TestCase

# Object factory for testing
from gl_site.test.Factory import Factory

# Import for constants
from gl_site.models import LeadUserInfo

# Regex parser
import re

# Date utilities
from datetime import date

# Common validation
from gl_site.test.form_validation import AccountFormValidator

class TestAccountSettings(TestCase, AccountFormValidator):
    """ Test class for verifying the account settings view """

    def setUp(self):
        """ Set Up
            Create a user account and user info
            to be used for testing
        """
        self.user, self.info = Factory.createUser()
        self.organization = self.info.organization
        self.session = self.info.session

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
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Make the GET request
        response = self.client.get('/account-settings', follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Expected form values
        settings_form = Factory.createUserSettingsPostDict(self.user, self.info)

        # Validate field values in user_form
        user_form = response.context['user_form']
        self.validate_form(user_form, settings_form, ())

        # Validate field values in info_form
        info_form = response.context['info_form']
        self.validate_form(info_form, settings_form, ())

    def testUsernameNotUnique(self):
        """ Account Settings - Username not unique.
            Verify that attempting to change to a username
            already in use rerenders the page with a form
            error.
        """

        # Create a second user
        user2, user2_info = Factory.createUser()

        # Log in as the first user
        self.client.login(username = self.user, password = Factory.defaultPassword)

        # Get the post info and change username
        settings_form = Factory.createUserSettingsPostDict(self.user, self.info)
        settings_form['username'] = user2.username

        # Make the POST request
        response = self.client.post('/account-settings', settings_form, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        user_form = response.context['user_form']
        self.validate_form(user_form, settings_form, ('username'))

        # Validate field values in info_form
        info_form = response.context['info_form']
        self.validate_form(info_form, settings_form, ())

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
        user2, user2_info = Factory.createUser()

        # Log in as the first user
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Get the post dict and set email not unique
        settings_form = Factory.createUserSettingsPostDict(self.user, self.info)
        settings_form['email'] = user2.email

        # Make the POST request
        response = self.client.post('/account-settings', settings_form, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        user_form = response.context['user_form']
        self.validate_form(user_form, settings_form, ('email'))

        # Validate field values in info_form
        info_form = response.context['info_form']
        self.validate_form(info_form, settings_form, ())

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
        settings_form = Factory.createUserSettingsPostDict(self.user, self.info)
        settings_form['gender'] = 'i'

        # Make the POST request
        response = self.client.post('/account-settings', settings_form, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        user_form = response.context['user_form']
        self.validate_form(user_form, settings_form, ())

        # Validate field values in info_form
        info_form = response.context['info_form']
        self.validate_form(info_form, settings_form, ('gender'))

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)
        self.assertEqual(response.context['session'].name, self.session.name)

    def testGradDateNotValid(self):
        """ Account Settings - graduation_date not valid.
            Verify that submitting an invalid graduation_date
            kicks back an error
        """

        # Log in
        self.client.login(username = self.user.username, password = Factory.defaultPassword)

        # Create the post dict and set graduation_date
        settings_form = Factory.createUserSettingsPostDict(self.user, self.info)
        settings_form['graduation_date'] = -1

        # Make the POST request
        response = self.client.post('/account-settings', settings_form, follow = True)

        # Verify the correct template was used
        self.assertTemplateUsed(response, 'user/settings.html')

        # Verify both the epxected forms were passed to the template
        self.assertTrue('user_form' in response.context)
        self.assertTrue('info_form' in response.context)

        # Validate field values in user_form
        user_form = response.context['user_form']
        self.validate_form(user_form, settings_form, ())

        # Validate field values in info_form
        info_form = response.context['info_form']
        self.validate_form(info_form, settings_form, ('graduation_date'))

        self.assertTrue('organization' in response.context)
        self.assertEqual(response.context['organization'].name, self.organization.name)

        self.assertTrue('session' in response.context)
        self.assertEqual(response.context['session'].name, self.session.name)

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
                'major': LeadUserInfo.ENGINEERING,
                'education': 'SE',
                'graduation_date': str(date(2000, 1, 1)),
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
        self.assertEqual(info.major, LeadUserInfo.ENGINEERING)
        self.assertEqual(info.graduation_date, date(2000, 1, 1))
        self.assertEqual(info.organization, self.organization)
        self.assertEqual(info.session, self.session)
