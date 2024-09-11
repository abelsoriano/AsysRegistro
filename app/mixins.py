from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Crear roles
def create_roles():
    Group.objects.get_or_create(name='Jovenes_Secretary')
    Group.objects.get_or_create(name='Caballeros_Secretary')
    Group.objects.get_or_create(name='Damas_Secretary')
    Group.objects.get_or_create(name='General_Secretary')
