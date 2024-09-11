from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User




# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(label='Correo Eletronico')
#     firstname = forms.CharField(label='Nombre')
#     lastname = forms.CharField(label='Apellido')
#
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'firstname', 'lastname', 'password1', 'password2')