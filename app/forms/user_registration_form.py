from django import forms
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
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        
        #Set custom widgets and validators
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['email'].validators = [validate_email]
        
        #Set custom class on all widgets
        for name, field in self.fields.items():
            field.required = True
            if field.widget.attrs.has_key('class'):
                field.widget.attrs['class'] += 'form-control'
            else:
                field.widget.attrs.update({'class':'form-control'})
                
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