

from collections import defaultdict
from django.utils import timezone

import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import RedirectView

from app.models import Attendance, AttendanceType, Miembro, Persona, Servicio
import setting.settings as setting



class LoginFormView(LoginView):
    template_name = 'registration/login.html'

    def dispatch(self, request, *args, **kwargs):
       if request.user.is_authenticated:
           return HttpResponseRedirect(setting.LOGIN_REDIRECT_URL)
       return super().dispatch(request,*args, **kwargs)



class LogoutView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)


from django.shortcuts import render
from django.db.models import Count, Q

import re

def extraer_nombres(texto):
    """
    Extrae nombres de un texto. Detecta nombres compuestos y maneja mayúsculas/minúsculas.
    """
    if not texto:
        return []
    # Expresión regular mejorada
    nombres = re.findall(r'\b[A-ZÁÉÍÓÚ][a-záéíóú]+\b(?:\s[A-ZÁÉÍÓÚ][a-záéíóú]+\b)*', texto)
    return nombres


def dashboard_unificado(request):
    # Lógica de asistencia
    inasistencias_miembros = (
        Attendance.objects.filter(present=False)
        .values('miembro__name', 'miembro__lastname')
        .annotate(total_inasistencias=Count('miembro'))
        .order_by('-total_inasistencias')[:10]
    )
    
    cultos_menos_asistencia = (
        Attendance.objects.values('attendance_type', 'date')
        .annotate(total_asistencia=Count('id', filter=Q(present=True)))
        .order_by('total_asistencia')[:10]
    )
    
    # Preparar datos para los gráficos de asistencia
    inasistencias_labels = [f"{item['miembro__name']} {item['miembro__lastname']}" for item in inasistencias_miembros]
    inasistencias_data = [item['total_inasistencias'] for item in inasistencias_miembros]
    
    cultos_labels = [f"{dict(AttendanceType.choices)[item['attendance_type']]} - {item['date'].strftime('%Y-%m-%d')}" for item in cultos_menos_asistencia]
    cultos_data = [item['total_asistencia'] for item in cultos_menos_asistencia]
    
    # Lógica de oportunidades
    participaciones_por_nombre = defaultdict(int)
    
    servicios = Servicio.objects.all()
    for servicio in servicios:
        for persona in servicio.participantes.all():
            nombre_completo = f"{persona.nombre} {persona.apellido}"
            participaciones_por_nombre[nombre_completo] += 1
    
    # Contar participaciones en los campos de texto
    for servicio in servicios:
        nombres_direccion = extraer_nombres(servicio.direccion)
        nombres_devocional = extraer_nombres(servicio.devocional)
        nombres_mensaje = extraer_nombres(servicio.mensaje)
        
        for nombre in nombres_direccion + nombres_devocional + nombres_mensaje:
            participaciones_por_nombre[nombre] += 1
    
    # Convertir el diccionario a una lista ordenada
    nombres_mas_participaciones = sorted(
        participaciones_por_nombre.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]  # Top 10 nombres con más participaciones
    
    # Preparar datos para el gráfico de participaciones
    nombres_labels = [nombre for nombre, _ in nombres_mas_participaciones]
    nombres_data = [total for _, total in nombres_mas_participaciones]
    
    # Calcular estadísticas adicionales para el panel de resumen
    total_miembros = Miembro.objects.count()
    total_cultos = Attendance.objects.values('date', 'attendance_type').distinct().count()
    
    # Calcular asistencia promedio
    asistencia_total = Attendance.objects.filter(present=True).count()
    registros_totales = Attendance.objects.count()
    if registros_totales > 0:
        asistencia_promedio = round((asistencia_total / registros_totales) * 100, 1)
    else:
        asistencia_promedio = 0
    
    # Obtener la fecha del último culto
    ultimo_culto = Attendance.objects.order_by('-date').values('date').first()
    if ultimo_culto:
        ultimo_culto_fecha = ultimo_culto['date'].strftime('%d %b')
    else:
        ultimo_culto_fecha = '-'
    
    # Calcular tendencia de asistencia por mes
    tendencia_data = []
    tendencia_labels = []
    
    # Últimos 6 meses
    for i in range(5, -1, -1):
        fecha_mes = timezone.now() - timezone.timedelta(days=30*i)
        mes = fecha_mes.strftime('%b')
        tendencia_labels.append(mes)
        
        # Contar asistencias del mes
        inicio_mes = fecha_mes.replace(day=1)
        if i > 0:
            fin_mes = (fecha_mes.replace(day=1) + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
        else:
            fin_mes = timezone.now()
        
        asistencias_mes = Attendance.objects.filter(date__range=[inicio_mes, fin_mes])
        total_registros_mes = asistencias_mes.count()
        
        if total_registros_mes > 0:
            porcentaje_asistencia = round((asistencias_mes.filter(present=True).count() / total_registros_mes) * 100, 1)
        else:
            porcentaje_asistencia = 0
        
        tendencia_data.append(porcentaje_asistencia)
    
    # Distribución por grupos (ejemplo - ajusta según tu modelo)
    # Puedes reemplazar esto con tus propios datos de grupos
    grupos_labels = ['Jóvenes', 'Adultos', 'Niños', 'Ancianos', 'Familias']
    grupos_data = [25, 40, 15, 10, 10]  # Reemplaza con datos reales
    
    # Unificar contexto
    context = {
        # Datos de asistencia
        'inasistencias_labels': json.dumps(inasistencias_labels),
        'inasistencias_data': json.dumps(inasistencias_data),
        'cultos_labels': json.dumps(cultos_labels),
        'cultos_data': json.dumps(cultos_data),
        
        # Datos de oportunidades
        'nombres_labels': json.dumps(nombres_labels),
        'nombres_data': json.dumps(nombres_data),
        
        # Datos para tendencia
        'tendencia_labels': json.dumps(tendencia_labels),
        'tendencia_data': json.dumps(tendencia_data),
        
        # Datos para grupos
        'grupos_labels': json.dumps(grupos_labels),
        'grupos_data': json.dumps(grupos_data),
        
        # Datos para el panel de resumen
        'total_miembros': total_miembros,
        'total_cultos': total_cultos,
        'asistencia_promedio': asistencia_promedio,
        'ultimo_culto': ultimo_culto_fecha,
    }
    
    return render(request, 'dashboard_unificados.html', context)