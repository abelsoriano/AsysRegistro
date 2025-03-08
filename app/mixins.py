from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Crear roles
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages

class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin para verificar si el usuario pertenece a un grupo específico."""
    group_name = None  # Nombre del grupo requerido
    login_url = '/login/'  # URL de redirección si el usuario no está autenticado
    permission_denied_message = "No tienes permiso para acceder a esta página."

    def test_func(self):
        """Verifica si el usuario pertenece al grupo."""
        if self.group_name is None:
            raise ValueError("El atributo 'group_name' debe ser definido.")
        return self.request.user.groups.filter(name=self.group_name).exists()

    def handle_no_permission(self):
        """Maneja el caso en que el usuario no tiene permiso."""
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.login_url)
