from django.urls import path

from app.views.asistencia import views
from app.views.asistencia.views import *
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
    path('asistencia/crear/', AttendanceCreateViewCaballeros.as_view(), name='create_asistencia-caballero'),
    path('asistencia/caballeros/', AttendanceListCaballeros.as_view(), name='list_asistencia_caballeros'),

    path('asistencia/list/', AttendanceListDamas.as_view(), name='list_asistencia_damas'),
    path('asistencia/damas/', AttendanceCreateViewDamas.as_view(), name='create_asistencia_damas'),
    path('asistencia/general-list/', AttendanceListGeneral.as_view(), name='list_asistencia_general'),
    path('asistencia/general/', AttendanceCreateViewGeneral.as_view(), name='create_asistencia_general'),


    path('crear-asistencia/', AttendanceCreateViewJovenes.as_view(), name='crear_asistencia'),
    path('lista-asistencia/', AttendanceListJovenes.as_view(), name='list_asistencia'),
    path('details/', AttendanceDetailsView.as_view(), name='details_asistencia'),
    path('guardar-status/', views.guardar_status, name='guardar_status'),
    path('asistencia/editar/<int:pk>/', AttendaceUpdate.as_view(), name='update_asistencia'),

     path('asistencia/editar/grupal/<date>/', AttendanceUpdateGroup.as_view(), name='edit_asistencia_group'),

    path('notas/list', NotaView.as_view(), name='nota_list'),
    path('notas/delete/<int:pk>/', NotaDeleteView.as_view(), name='nota_delete'),
    path('notas/cargar_mas/', cargar_mas_notas, name='cargar_mas_notas'),
    path('notas/update/<int:pk>/', NotaUpdateView.as_view(), name='nota_update'),


    # path('crear_directiva', DirectivaCreate.as_view(), name='crear_directiva'),
    


    #lista de tareas
    path('crear/', TareaCreateView.as_view(), name='tarea-crear'),
    path('lista/', TareaListView.as_view(), name='tarea-lista'),
    path('<int:pk>/editar/', TareaUpdateView.as_view(), name='tarea-editar'),


]
