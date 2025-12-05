from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms
class UserRegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields=["username","first_name","email","affiliation","nationality","password1","password2"]
        widgets={
            "email":forms.EmailInput(),
            "password1":forms.PasswordInput()
        }