from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

#User Registration Form
class UserRegisterForm(UserCreationForm):
    class Meta :
        model = User
        fields = ['username', 'email', 'password1','password2']    