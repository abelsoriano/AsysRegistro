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


# @receiver(post_save, sender=CambioDirectiva)
# def update_miembros_cargo(sender, instance, **kwargs):
#     cargos = {
#         'presidente': instance.presidente,
#         'vicepresidente': instance.vicepresidente,
#         'secretario': instance.secretario,
#         'sub_secretario': instance.sub_secretario,
#         'tesorero': instance.tesorero,
#         'primer_vocal': instance.primer_vocal,
#     }

#     try:
#         cargo_miembro_default = Cargo.objects.get(name="Miembro")
#     except Cargo.DoesNotExist:
#         print("El cargo 'Miembro' no existe en la base de datos.")
#         return

#     for cargo_name, miembro in cargos.items():
#         if miembro:
#             cargo = Cargo.objects.get(name=cargo_name.capitalize())

#             # Ensure no other member in the same category has this role
#             Miembro.objects.filter(cargo=cargo, category=miembro.category).update(cargo=cargo_miembro_default)

#             # Assign the new role to the current member
#             miembro.cargo = cargo
#             miembro.save()

#     # Update roles for outgoing members to "Miembro"
#     miembros_salientes = Miembro.objects.filter(cargo__name__in=cargos.keys()).exclude(
#         id__in=[miembro.id for miembro in cargos.values() if miembro is not None])

#     for miembro in miembros_salientes:
#         miembro.cargo = cargo_miembro_default
#         miembro.save()




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