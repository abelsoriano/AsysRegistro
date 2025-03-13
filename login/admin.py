from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import UsuarioPersonalizado

class UsuarioPersonalizadoAdmin(UserAdmin):
    list_display = ['username', 'email', 'nombre', 'apellido', 'is_active']
    
    # Añadir los campos personalizados al fieldset
    fieldsets = UserAdmin.fieldsets + (
        ('Información Personal', {'fields': ('nombre', 'apellido')}),
    )
    
    # También añadirlos al formulario de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Personal', {'fields': ('nombre', 'apellido')}),
    )

# Corregido: solo pasar dos argumentos, no tres
admin.site.register(UsuarioPersonalizado, UsuarioPersonalizadoAdmin)