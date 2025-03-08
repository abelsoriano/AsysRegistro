from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from login.models import UsuarioPersonalizado




class RegistroForm(UserCreationForm):
    # nombre = forms.CharField(max_length=30, required=True, help_text='Requerido. 30 caracteres o menos.')
    # apellido = forms.CharField(max_length=30, required=True, help_text='Requerido. 30 caracteres o menos.')
    # email = forms.EmailField(max_length=254, required=True, help_text='Requerido. Ingrese un email válido.')

    class Meta:
        model = UsuarioPersonalizado
        fields = ['username', 'nombre', 'apellido', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'email'}),
           'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
           'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
           'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
           'password2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),




        }

    