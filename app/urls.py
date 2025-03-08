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
from app.views.cambioDirectiva.views import *
from app.views.presentacionNino.view import *
from app.views.estudio.views import *


app_name = 'asys'

urlpatterns = [
    # url page Persona
    path('persona/list/', MembersListView.as_view(), name='miembro_list'),
    path('persona/add/', MembersCreate.as_view(), name='members_create'),
    path('persona/edit/<int:pk>/', MembersUpdate.as_view(), name='members_update'),
    path('persona/delete/<int:pk>/', MembersDelete.as_view(), name='miembro_delete'),

    # Url page Servico
    path('servicio/create/', login_required(ServicioCreateView.as_view()), name='servicio_create'),
    path('add_persona/', PersonaCreateView.as_view(), name='add_persona'),
    path('servicio/list/', ServicioListView.as_view(), name='service_list'),
    path('servicio/update/<int:pk>/', ServiceUpdate.as_view(), name='service_update'),
    path('servicio/delete/<int:pk>/', ServicioDeleteView.as_view(), name='servicio_delete'),
    path('servicio/detail/<int:pk>/', ServicioDetailView.as_view(), name='servicio_detail'),
    

    # Url page Asistencia
    path('asistencia/crear-general/', AttendanceCreateViewGeneral.as_view(), name='create_asistencia_general'),
    path('asistencia/crear-caballero/', AttendanceCreateViewCaballeros.as_view(), name='create_asistencia-caballero'),
    path('asistencia/crear-damas/', AttendanceCreateViewDamas.as_view(), name='create_asistencia_damas'),
    path('crear-asistencia/', AttendanceCreateViewJovenes.as_view(), name='crear_asistencia'),

    #Url page Asistencia
    path('asistencia/caballeros/', AttendanceListCaballeros.as_view(), name='list_asistencia_caballeros'),
    path('asistencia/list-damas/', AttendanceListDamas.as_view(), name='list_asistencia_damas'),
    path('asistencia/general-list/', AttendanceListGeneral.as_view(), name='list_asistencia_general'),
    path('lista-asistencia/', AttendanceListJovenes.as_view(), name='list_asistencia'),

    path('details/', AttendanceDetailsView.as_view(), name='details_asistencia'),
    path('guardar-status/', views.update_attendance_reason, name='guardar_status'),
    path('asistencia/editar/grupal/<date>/<type>/', AttendanceUpdateGroup.as_view(), name='edit_asistencia_group'),

    # Notas
    path('notas/list', NotaView.as_view(), name='nota_list'),
    path('notas/delete/<int:pk>/', nota_delete, name='nota_delete'),
    path('notas/get/<int:id>/', NotaView.as_view(), name='nota_get'),
    

    #lista de tareas
    path('tareas/', TareaListView.as_view(), name='tareas-list'),
    path('editar/<int:pk>/', TareaUpdateView.as_view(), name='tarea-editar'),
    path('obtener/<int:pk>/', obtener_tarea, name='tarea-obtener'),
    path('completar/<int:pk>/', completar_tarea, name='tarea-completar'),
    # path('cargar-mas-tareas/', cargar_mas_tareas, name='cargar-mas-tareas'),

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

    #cambio de directiva
    path('procesos/', ProcesoTransicionListView.as_view(), name='proceso_transicion_list'),
    path('procesos/nuevo/', ProcesoTransicionCreateView.as_view(), name='proceso_transicion_create'),
    path('procesos/<int:pk>/', ProcesoTransicionDetailView.as_view(), name='proceso_transicion_detail'),
    path('procesos/<int:proceso_id>/registrar-candidato/', registrar_candidato, name='registrar_candidato'),
    path('procesos/<int:proceso_id>/iniciar-votacion/', iniciar_votacion, name='iniciar_votacion'),
    path('proceso/<int:proceso_id>/finanza_list/', RegistroFinanzasListView.as_view(), name='finalizar_list'),
    path('proceso/<int:proceso_id>/registrar_finanzas/', RegistroFinanzasCreateView.as_view(), name='registro_finanzas_create'),
    path('proceso/<int:proceso_id>/registro_finanzas/<int:pk>/editar/', RegistroFinanzasUpdateView.as_view(), name='registro_finanzas_edit'),
    path('proceso/<int:proceso_id>/registro_finanzas/<int:pk>/eliminar/', RegistroFinanzasDeleteView.as_view(), name='registro_finanzas_delete'),
    path('periodos/list', PeriodoDirectivaListView.as_view(), name='periodo_directiva_list'),
    path('periodos/nuevo_periodo/', PeriodoDirectivaCreateView.as_view(), name='periodo_directiva_create'),
    path('periodos/<int:pk>/editar/', PeriodoDirectivaUpdateView.as_view(), name='periodo_directiva_edit'),
    path('periodos/<int:pk>/eliminar/', PeriodoDirectivaDeleteView.as_view(), name='periodo_directiva_delete'),
    path('api/periodos-activos/<str:seccion_id>/', get_periodos_activos, name='api_periodos_activos'),
    path('api/periodos-planeados/<str:seccion_id>/', get_periodos_planeados, name='api_periodos_planeados'),

    #Presentacion de niño
    path('presentacion/', PresentacionListView.as_view(), name='lista_presentaciones'),
    path('presentacion/nueva/', PresentacionNinoCreateView.as_view(), name='nueva_presentacion'),
    path('presentacion/<int:pk>/', PresentacionDetailView.as_view(), name='detalle_presentacion'),
    path('presentacion/<int:pk>/eliminar/', PresentacionDeleteView.as_view(), name='eliminar_presentacion'),

    #Estudio Biblico
    path('estudios/nuevo/', crear_estudio, name='crear_estudio'),
    path('estudios/<int:estudio_id>/asistencia/', registrar_asistencia, name='registrar_asistencia'),
    path('estudios/<int:estudio_id>/', detalle_estudio, name='detalle_estudio'),
    path('estudios/', lista_estudios, name='lista_estudios'),






]
