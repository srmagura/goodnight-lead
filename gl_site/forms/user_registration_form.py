from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.forms import ModelForm
from gl_site.models import LeadUserInfo, Organization

#Custom validators
def validate_email(value):
    if(User.objects.filter(email=value).exists()):
        raise ValidationError(
            "Email already in use"
        )
#Need to pass the old email to the validator, best way to do this seems to be
#to write a function which returns a function.
#Set the validator to the outer function and pass it the old email
def validate_email_uniqueOrUnchanged(old_email):
    def validate(new_email):
        if(old_email != new_email and User.objects.filter(email=new_email).exists()):
            raise ValidationError(
                "Email already in use"
            )
    return validate

#The part of the form which deals with the User object
class UserForm(UserCreationForm):
    class Meta:
        #Use the User object as a model with the desired fields
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        #Set custom widgets and validators
        self.fields['email'].validators = [validate_email]

        #Set custom class on all widgets
        for name, field in self.fields.items():
            field.required = True
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

    #Override the default save method to set the password correctly
    def save(self, commit=True):
        user = super(UserForm, self).save(commit = False)
        user.set_password(self.cleaned_data['password1'])

        #Save to the db
        if(commit):
            user.save()

        return user

#The part of the form which deals with the LeadUserInfo object
class InfoForm(ModelForm):
    class Meta:
        model = LeadUserInfo
        exclude = ('user', 'organization')

    # The name of the organization a user would like to sign up for
    organization_name = forms.CharField(max_length=120)

    # The entry code for the specified organization
    organization_code = forms.CharField(max_length=120)

    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)

        #Set custom class on all widgets
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

    def clean(self):
        """ Override the default clean (validation) method """

        # Call clean on super
        super(InfoForm, self).clean()

        # If an organization name and code were entered, verify
        # that both exist
        if ('organization_name' in self.cleaned_data and 'organization_code' in self.cleaned_data):
            try:
                org = Organization.objects.get(name=self.cleaned_data['organization_name'])
            except Organization.DoesNotExist:
                org = None

            if org is None or org.code != self.cleaned_data['organization_code']:
                raise ValidationError("Organization name or code not recognized")

        return self.cleaned_data

#Used for changing all user info except passwords.
class UserSettingsForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserSettingsForm, self).__init__(*args, **kwargs)

        #get rid of the password field we dont want
        del self.fields['password']

        #set validators
        self.fields['email'].validators = [validate_email_uniqueOrUnchanged(self.instance.email)]

        #Set custom class on all widgets
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

class PasswordChangeForm(forms.Form):
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

        self.fields['password1'].label = "New Password"
        self.fields['password2'].label = "Password Confirmation"

        #Set custom class on all widgets
        for name, field in self.fields.items():
            if 'class' in field.widget.attrs:
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})

    def clean(self):
        super(PasswordChangeForm, self).clean()

        if('password1' in self.cleaned_data and 'password2' in self.cleaned_data):
            pass1 = self.cleaned_data['password1']
            pass2 = self.cleaned_data['password2']

            if(pass1 != pass2):
                raise ValidationError("Passwords did not match")
