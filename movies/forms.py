from django import forms
from allauth.account.forms import LoginForm, SignupForm
from . import validators
from .models import User

class MyCustomLoginForm(LoginForm):
    class Meta:
        model = User
        fields = ['email']
    def login(self, *args, **kwargs):
        # Add your own processing here.

        # You must return the original result.
        return super(MyCustomLoginForm, self).login(*args, **kwargs)
    

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

    def signup(self, request, user):
        user.email = self.cleaned_data['email']
        user.save