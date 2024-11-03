from django.urls import path
from . import views
from app.views.asistencia import views
from app.views.asistencia.views import *
from app.views.cargoEstado.views import *
from app.views.notas.views import *
from app.views.persona.views import *
from app.views.servicio.views import *
from app.views.cambioDirectiva.views import *
from app.views.tareas.views import *


app_name = 'asys'

urlpatterns = [
    path('persona/list/', MembersListView.as_view(), name='miembro_list'),
    path('persona/add/', MembersCreate.as_view(), name='members_create'),
    path('persona/edit/<int:pk>/', MembersUpdate.as_view(), name='members_update'),
    path('persona/delete/<int:pk>/', MembersDelete.as_view(), name='members_delete'),

    # Url page Servico
    path('servicio/create/', login_required(ServicioCreateView.as_view()), name='servicio_create'),
    path('add-persona/', add_persona, name='add_persona'),
    path('servicio/list/', ServicioListView.as_view(), name='service_list'),
    path('service/edit/<int:pk>/', ServiceUpdate.as_view(), name='service_update'),
    path('service/delete/<int:pk>/', ServiceDelete.as_view(), name='service_delete'),

    # Url page Asistencia
    path('asistencia/crear-caballero/', AttendanceCreateViewCaballeros.as_view(), name='create_asistencia-caballero'),
    path('asistencia/caballeros/', AttendanceListCaballeros.as_view(), name='list_asistencia_caballeros'),

    path('asistencia/list-damas/', AttendanceListDamas.as_view(), name='list_asistencia_damas'),
    path('asistencia/crear-damas/', AttendanceCreateViewDamas.as_view(), name='create_asistencia_damas'),
    path('asistencia/general-list/', AttendanceListGeneral.as_view(), name='list_asistencia_general'),
    path('asistencia/crear-general/', AttendanceCreateViewGeneral.as_view(), name='create_asistencia_general'),


    path('crear-asistencia/', AttendanceCreateViewJovenes.as_view(), name='crear_asistencia'),
    path('lista-asistencia/', AttendanceListJovenes.as_view(), name='list_asistencia'),
    path('details/', AttendanceDetailsView.as_view(), name='details_asistencia'),
    path('guardar-status/', views.guardar_status, name='guardar_status'),
    # path('asistencia/editar/<int:pk>/', AttendaceUpdate.as_view(), name='update_asistencia'),

    path('asistencia/editar/grupal/<date>/', AttendanceUpdateGroup.as_view(), name='edit_asistencia_group'),

    path('notas/list', NotaView.as_view(), name='nota_list'),
    path('notas/delete/<int:pk>/', NotaDeleteView.as_view(), name='nota_delete'),
    path('notas/cargar_mas/', cargar_mas_notas, name='cargar_mas_notas'),
    path('notas/update/<int:pk>/', NotaUpdateView.as_view(), name='nota_update'),


    # path('crear_directiva', DirectivaCreate.as_view(), name='crear_directiva'),
    


    #lista de tareas

    path('tareas/', TareaListView.as_view(), name='tareas-list'),
    path('editar/<int:pk>/', TareaUpdateView.as_view(), name='tarea-editar'),
    path('obtener/<int:pk>/', obtener_tarea, name='tarea-obtener'),
    path('completar/<int:pk>/', completar_tarea, name='tarea-completar'),

    #Cargo y Estado
    path('crearEstado/', ModelEstadoCreateView.as_view(), name='create-estado'),
    path('listEstado/', ModelEstadoList.as_view(), name='list-estado'),
    path('getEstado/<int:pk>/', get_estado, name='get_estado'),
    path('updateEstado/<int:pk>/', EstadoUpdateView.as_view(), name='update-estado'),
    path('deleteEstado/<int:id>/', delete_estado, name='delete_estado'),
    # cargo
    path('cargoList/', CargoList.as_view(), name="list-cargo"),
    path('createCargo/', CargoCreateView.as_view(), name="create-cargo"),
    path('getCargo/<int:pk>/', get_cargo, name='get_cargo'),
    path('updateCargo/<int:pk>/', CargoUpdateView.as_view(), name='update-cargo'),





]
