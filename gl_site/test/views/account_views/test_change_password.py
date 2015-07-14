# Import test case
from django.test import TestCase

# Object factory for testing
from gl_site.test.Factory import Factory

class TestChangePassword(TestCase):
    """ Test class for the change password view """

    def setUp(self):
        """ Password - Set up.
            Set up a user account for testing.
        """
        self.user, self.info = Factory.createUser()
        self.organization = self.info.organization
        self.session = self.info.session

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
