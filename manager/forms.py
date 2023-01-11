from django.forms import ModelForm, Form
from django.contrib.auth.models import User
from django.forms import CharField, TextInput, PasswordInput


class CreateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class LoginForm(Form):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']

