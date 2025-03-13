from django.db import models
from django.contrib.auth.models import AbstractUser


class UsuarioPersonalizado(AbstractUser):
    nombre = models.CharField(max_length=30, blank=True)
    apellido = models.CharField(max_length=30, blank=True)

    # Define related_name únicos para evitar conflictos
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="usuario_personalizado_groups",  
        related_query_name="usuario_personalizado",
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="usuario_personalizado_user_permissions", 
        related_query_name="usuario_personalizado",
    )