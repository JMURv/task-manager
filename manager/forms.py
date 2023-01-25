from django.forms import Form
from django.forms import CharField, TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]


class LoginForm(Form):
    username = CharField(widget=TextInput(attrs={'placeholder': 'Username'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))
    fields = ['username', 'password']

