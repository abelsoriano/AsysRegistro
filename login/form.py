from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import UsuarioPersonalizado

class RegistroForm(UserCreationForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Grupo de usuario",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'nombre', 'apellido', 'password1', 'password2', 'grupo')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(RegistroForm, self).__init__(*args, **kwargs)
        # Aplicar la clase form-control a los campos de contraseña
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class EditarUsuarioForm(forms.ModelForm):
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label="Grupos"
    )
    
    is_active = forms.BooleanField(
        required=False,
        label="Usuario activo",
        help_text="Desmarque esta opción para desactivar el usuario sin eliminarlo."
    )
    
    class Meta:
        model = UsuarioPersonalizado
        fields = ('username', 'email', 'nombre', 'apellido', 'is_active', 'grupos')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['grupos'].initial = self.instance.groups.all()
            
    def save(self, commit=True):
        usuario = super().save(commit=commit)
        if commit:
            usuario.groups.clear()
            usuario.groups.add(*self.cleaned_data['grupos'])
        return usuario