# Regex parser
import re

class AccountFormValidator:
    """ Common superclass for a django test case """

    FIELD_ERRORS = {
        'username': 'A user with that username already exists.',
        'email': 'Email already in use',
        'password2': 'The two password fields didn\'t match.',
        'organization_code': 'Invalid organization code.',
        'gender': 'Select a valid choice. i is not one of the available choices.',
        'graduation_date': 'Enter a valid date.'
    }

    def validate_form(self, account_form, expected_form, expected_errors):
        """ Validate that an account_form matches the expected_form """

        # Validate each field
        for field in account_form:
            # All fields should be equal
            self.assertEquals(str(field.value()), str(expected_form[field.name]))

            # Verify the error is correct
            if (field.name in expected_errors):
                self.assertEqual(re.sub(r'\* ', '', field.errors.as_text()),
                    self.FIELD_ERRORS[field.name])
            else:
                self.assertEqual(field.errors, [])
