from  django.urls import include, path

from login.views import *

urlpatterns = [
    # path('', LoginFormView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('home/', dashboard_unificado , name='index'),
    path('registro/', registro, name='registro'),
    path('usuarios/', ListaUsuariosView.as_view(), name='lista_usuarios'),
    path('usuarios/<int:pk>/eliminar/', eliminar_usuario, name='eliminar_usuario'),
    path('usuarios/<int:pk>/editar/', EditarUsuarioView.as_view(), name='editar_usuario'),
    path('usuarios/<int:pk>/cambiar-password/', AdminPasswordChangeView.as_view(), name='admin_password_change'),

        
]
