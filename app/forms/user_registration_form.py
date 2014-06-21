from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from django.forms import ModelForm
from app.models import LeadUserInfo

#Custom validators    
def validate_email(value):
        if(User.objects.filter(email=value).exists()):
            raise ValidationError(
                "Email already in use"
            )
def validate_gender(value):           
    if(not (value=='m' or value=='M' or value=='f' or value=='F')):
            raise ValidationError(
                "Must be M or F"
            )
                
#The part of the form which deals with the User object    
class UserForm(UserCreationForm):
    class Meta:
        #Use the User object as a model with the desired fields
        model = User
        fields = ['username', 'email',  'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        #Set custom widgets and validators
        self.fields['email'].validators = [validate_email]
        
        #Set custom class on all widgets
        for name, field in self.fields.items():
            field.required = True
            if field.widget.attrs.has_key('class'):
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
        exclude = ('user',)
    def __init__(self, *args, **kwargs):
        super(InfoForm, self).__init__(*args, **kwargs)
        
        #Set custom validators
        self.fields['gender'].validators = [validate_gender]
        
        #Set custom class on all widgets
        for name, field in self.fields.items():
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})
                
class UserSettingsForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.CharField()
    
    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly')
        super(UserSettingsForm, self).__init__(*args, **kwargs)
        
        #Set custom class on all widgets
        for name, field in self.fields.items():
            if(readonly):
                field.widget.attrs['readonly'] = True
                
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})