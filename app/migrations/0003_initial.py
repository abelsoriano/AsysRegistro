# migrations/0002_create_initial_groups.py (ajusta el número según tus migraciones existentes)
from django.db import migrations

def crear_grupos_iniciales(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    grupos = ['jovenes', 'damas', 'caballeros', 'general']
    for grupo_nombre in grupos:
        Group.objects.get_or_create(name=grupo_nombre)

def eliminar_grupos(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['jovenes', 'damas', 'caballeros', 'general']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('app', '0002_initial'),  # Asegúrate de que esta sea la migración anterior correcta
    ]

    operations = [
        migrations.RunPython(crear_grupos_iniciales, eliminar_grupos),
    ]