

from collections import defaultdict
from django.utils import timezone

import json
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator

from django.views import View
from django.views.generic import RedirectView

from app.models import Attendance, AttendanceType, Miembro, Persona, Servicio
import login
from login.form import RegistroForm
import setting.settings as setting
from django.shortcuts import render
from django.db.models import Count, Q

import re


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

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')  # Redirige a la página de inicio después del registro
    else:
        form = RegistroForm()
    return render(request, 'registration/crearUsuarioForm.html', {'form': form})


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
    servicios = Servicio.objects.all()
    participaciones_por_nombre = defaultdict(int)
    total_oportunidades = 0
    total_participantes = set() 
    
    for servicio in servicios:
        for persona in servicio.participantes.all():
            nombre_completo = f"{persona.nombre} {persona.apellido}"
            participaciones_por_nombre[nombre_completo] += 1
            total_oportunidades += 1
            total_participantes.add(nombre_completo)
    
    for servicio in servicios:
        for campo in ['direccion', 'devocional', 'mensaje']:
            nombres = extraer_nombres(getattr(servicio, campo))
            for nombre in nombres:
                participaciones_por_nombre[nombre] += 1
                total_oportunidades += 1
                total_participantes.add(nombre)
    
    nombres_mas_participaciones = sorted(
        participaciones_por_nombre.items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    
    nombres_labels = [nombre for nombre, _ in nombres_mas_participaciones]
    nombres_data = [total for _, total in nombres_mas_participaciones]
    
    total_miembros = Miembro.objects.count()
    total_cultos = Attendance.objects.values('date', 'attendance_type').distinct().count()
    
    asistencia_total = Attendance.objects.filter(present=True).count()
    registros_totales = Attendance.objects.count()
    asistencia_promedio = round((asistencia_total / registros_totales) * 100, 1) if registros_totales > 0 else 0
    
    ultimo_culto = Attendance.objects.order_by('-date').values('date').first()
    ultimo_culto_fecha = ultimo_culto['date'].strftime('%d %b') if ultimo_culto else '-'
    
    tendencia_data = []
    tendencia_labels = []
    
    for i in range(5, -1, -1):
        fecha_mes = timezone.now() - timezone.timedelta(days=30 * i)
        mes = fecha_mes.strftime('%b')
        tendencia_labels.append(mes)
        
        inicio_mes = fecha_mes.replace(day=1)
        fin_mes = (fecha_mes.replace(day=1) + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)
        
        asistencias_mes = Attendance.objects.filter(date__range=[inicio_mes, fin_mes])
        total_registros_mes = asistencias_mes.count()
        
        porcentaje_asistencia = round((asistencias_mes.filter(present=True).count() / total_registros_mes) * 100, 1) if total_registros_mes > 0 else 0
        tendencia_data.append(porcentaje_asistencia)
    
    attendance_counts = Attendance.objects.filter(present=True).values('attendance_type').annotate(total=Count('attendance_type'))
    grupos_labels = [str(AttendanceType(tipo['attendance_type']).label) for tipo in attendance_counts]
    grupos_data = [tipo['total'] for tipo in attendance_counts]
    
    context = {
        'inasistencias_labels': json.dumps(inasistencias_labels),
        'inasistencias_data': json.dumps(inasistencias_data),
        'cultos_labels': json.dumps(cultos_labels),
        'cultos_data': json.dumps(cultos_data),
        'nombres_labels': json.dumps(nombres_labels),
        'nombres_data': json.dumps(nombres_data),
        'tendencia_labels': json.dumps(tendencia_labels),
        'tendencia_data': json.dumps(tendencia_data),
        'grupos_labels': json.dumps(grupos_labels),
        'grupos_data': json.dumps(grupos_data),
        'total_miembros': total_miembros,
        'total_cultos': total_cultos,
        'asistencia_promedio': asistencia_promedio,
        'ultimo_culto': ultimo_culto_fecha,
        'total_oportunidades': total_oportunidades,
        'total_participantes': len(total_participantes),
    }
    
    return render(request, 'dashboard_unificados.html', context)


