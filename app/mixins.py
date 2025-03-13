from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Crear roles
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse

class GroupRequiredMixin(UserPassesTestMixin):
    group_name = None  # Nombre del grupo requerido
    permission_denied_message = 'No tienes permiso para acceder a esta página.'
    
    def test_func(self):
        # Verificar si el usuario está autenticado y pertenece al grupo
        return (
            self.request.user.is_authenticated and
            self.request.user.groups.filter(name=self.group_name).exists()
        )
    
    def handle_no_permission(self):
        # Mostrar mensaje de error
        messages.error(self.request, self.permission_denied_message)
        
        # Redirigir a la página de inicio (o cualquier otra página)
        return HttpResponseRedirect(reverse('index'))  # Cambia 'index' por la URL a la que deseas redirigir
        

# class GrupoJovenesMixin:
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.groups.filter(name='jovenes').exists():
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({'error': 'No tienes permiso para acceder a esta pagina.'}, status=403)
#             else:
#                 return HttpResponseRedirect(reverse('index'))
#         return super().dispatch(request, *args, **kwargs)
    

class GrupoDamasMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='damas').exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve JSON
                return JsonResponse({'error': 'No tienes permiso para acceder a esta página.'}, status=403)
            else:
                # Si no es AJAX, redirige a la página de inicio
                return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)

class GrupoCaballerosMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.groups.filter(name='caballeros').exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                # Si es una solicitud AJAX, devuelve JSON
                return JsonResponse({'error': 'No tienes permiso para acceder a esta página.'}, status=403)
            else:
                # Si no es AJAX, redirige a la página de inicio
                return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)