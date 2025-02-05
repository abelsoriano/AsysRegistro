from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Miembro, Cargo, Attendance

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin


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



class JovenesAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Jovenes_Secretary').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta vista.')
        return redirect('index')


class CaballerosAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Caballeros_Secretary').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta vista.')
        return redirect('index')
    
class DamasAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Damas_Secretary').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta vista.')
        return redirect('index')


class GeneralAccessMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='General_Secretary').exists()

    def handle_no_permission(self):
        messages.error(self.request, 'No tienes permiso para acceder a esta vista.')
        return redirect('index')


def create_permissions():
    content_type = ContentType.objects.get_for_model(Attendance)
    Permission.objects.create(
        codename='can_view_all_attendances',
        name='Can view all attendances',
        content_type=content_type
    )