class AuthTestUtil:
    """
    Utility functions for classes that test authentication.
    """

    def assert_invalid_login(self, username, password, expected_msg):
        """
        Try to login in via the login page, and assert that the attempt
        fails.

        expected_msg -- the expected error message
        """
        # Make the request with username and password set
        response = self.client.post('/login',
            {'username': username, 'password': password}, follow = True)

        # Get messages and verify
        messages = response.context['messages']
        self.assertEqual(len(messages), 1)
        for message in messages:
            self.assertEqual(message.message, expected_msg)

        # Correct template used
        self.assertTemplateUsed(response, template_name = 'user/login.html')

        # Not authenticated
        self.assertFalse(response.context['user'].is_authenticated)
