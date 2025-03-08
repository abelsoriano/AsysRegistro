from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from login.models import UsuarioPersonalizado

admin.site.register(UsuarioPersonalizado, UserAdmin)