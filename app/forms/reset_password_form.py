from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

#Email entry field with custom validation
class EmailField(forms.EmailField):
    def validate(self, value):
        super(EmailField, self).validate(value)
        if not User.objects.filter(email=value).exists():
            raise ValidationError(
               'There is no account associated with this email address.'
            )

class SendEmailForm(forms.Form):
    email = EmailField(
        label = "Email",
        required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control'}),
    )
