from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

#Username entry field with custom validation - username must be unique
class UsernameRegistrationField(forms.CharField):
    def validate(self, value):
        super(UsernameRegistrationField, self).validate(value)
        if(User.objects.filter(username=value).exists()):
            raise ValidationError(
                "Username is already taken"
            )

#Email entry field with custom validation - email must be unique    
class EmailRegistrationField(forms.EmailField):
    def validate(self, value):
        super(EmailRegistrationField, self).validate(value)
        if(User.objects.filter(email=value).exists()):
            raise ValidationError(
                "Email already in use"
            )

#Gender entry field which validates that an appropriate char was entered.
class GenderRegistrationField(forms.CharField):
    def validate(self, value):
        super(GenderRegistrationField, self).validate(value)
        if(not (value=='m' or value=='M' or value=='f' or value=='F')):
            raise ValidationError(
                "Must be M or F"
            )

#Form used for registering a new user account.
class UserRegistrationForm(forms.Form):
    
    firstname = forms.CharField(
        label="First Name",
        required=True,
        max_length = 30,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Enter your first name'}),
    )

    lastname = forms.CharField(
        label="Last Name",
        required=True,
        max_length = 30,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Enter your last name'}),
    )

    username = UsernameRegistrationField(
        label = "Username",
        required = True,
        max_length = 30,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Select a username'}),
    )
    
    email = EmailRegistrationField(
        label = "Email",
        required = True,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Enter your email address'}),
    )

    password = forms.CharField(
        widget = forms.PasswordInput(attrs = {'class': 'form-control', 'placeholder': 'Create a password'}),
    )
    
    gender = GenderRegistrationField(
        label="Gender",
        required=True,
        max_length = 1,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Gender'}),
    )
    
    major = forms.CharField(
        label="Major",
        required=True,
        max_length = 100,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Enter your current major'}),
    )
    
    year = forms.IntegerField(
        label="Year in university",
        required = True,
        min_value = 1,
        max_value = 4,
        localize = True,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '1 - 4'}),
    )
    
    organization = forms.CharField(
        label="Group",
        required=True,
        max_length = 100,
        widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Group or organization you are associated with'}),
    )