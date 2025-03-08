from email.headerregistry import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from .models import Miembro, Cargo, Attendance

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.signals import post_migrate


# asys/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import ProcesoTransicion

@receiver(post_save, sender=ProcesoTransicion)
def actualizar_estados_periodos(sender, instance, **kwargs):
    if instance.estado == 'COMPLETADO':
        # Actualizar el período anterior a FINALIZADO
        periodo_anterior = instance.periodo_anterior
        periodo_anterior.estado = 'FINALIZADO'
        periodo_anterior.fecha_fin = timezone.now()
        periodo_anterior.save()

        # Actualizar el período nuevo a ACTIVO
        periodo_nuevo = instance.periodo_nuevo
        periodo_nuevo.estado = 'ACTIVO'
        periodo_nuevo.save()


def role_required(group_name):
    def in_group(user):
        return user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group)