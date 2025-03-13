# views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Q, F, Count  
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from app.forms import EstudioBiblicoForm
from app.mixins import GroupRequiredMixin
from app.models import AsistenciaEstudio, AttendanceType, EstudioBiblico, Miembro

@login_required
def crear_estudio(request):
    if request.method == 'POST':
        form = EstudioBiblicoForm(request.POST)
        if form.is_valid():
            estudio = form.save(commit=False)
            estudio.user = request.user
            estudio.save()
            messages.success(request, 'Estudio bíblico registrado exitosamente.')
            return redirect('asys:registrar_asistencia', estudio_id=estudio.id)
    else:
        form = EstudioBiblicoForm()
    
    context = {
        'form': form,
        'maestros': Miembro.objects.filter(cargo__nombre='Maestro')
    }
    return render(request, 'estudio/crear_estudio.html', context)

@login_required
def registrar_asistencia(request, estudio_id):
    estudio = get_object_or_404(EstudioBiblico, id=estudio_id)
    miembros = Miembro.objects.all()

    if request.method == 'POST':
        # Obtiene la lista de miembros marcados como presentes
        presentes_ids = request.POST.getlist('presentes')
        todos_miembros_ids = [str(miembro.id) for miembro in miembros]
        
        # Crear o actualizar registros para todos los miembros
        for miembro_id in todos_miembros_ids:
            # Determinar si el miembro está presente
            esta_presente = miembro_id in presentes_ids
            
            AsistenciaEstudio.objects.update_or_create(
                miembro_id=miembro_id,
                date=estudio.fecha,
                attendance_type=AttendanceType.ESTUDIO,
                defaults={
                    'presente': esta_presente,
                    'user': request.user,
                }
            )
        
        messages.success(request, 'Asistencia registrada exitosamente.')
        return redirect('asys:lista_estudios')

    # Obtener asistencias existentes para mostrar en el formulario
    asistencias = AsistenciaEstudio.objects.filter(
        date=estudio.fecha,
        attendance_type=AttendanceType.ESTUDIO,
        presente=True
    )
    asistencias_ids = set(asistencias.values_list('miembro_id', flat=True))

    return render(request, 'estudio/registrar_asistencia.html', {
        'estudio': estudio,
        'miembros': miembros,
        'asistencias_ids': asistencias_ids,
    })


class ListaEstudiosView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    model = EstudioBiblico
    template_name = 'estudio/lista_estudios.html'
    context_object_name = 'estudios'
    group_name = 'damas'  # Nombre del grupo requerido

    def get_queryset(self):
        estudios = EstudioBiblico.objects.all().order_by('-fecha', '-id')
        estudios_data = []
        for estudio in estudios:
            presentes = AsistenciaEstudio.objects.filter(
                date=estudio.fecha,
                attendance_type=AttendanceType.ESTUDIO,
                presente=True
            ).count()

            ausentes = AsistenciaEstudio.objects.filter(
                date=estudio.fecha,
                attendance_type=AttendanceType.ESTUDIO,
                presente=False
            ).count()

            estudios_data.append({
                'id': estudio.id,
                'fecha': estudio.fecha,
                'tema': estudio.tema,
                'maestro': estudio.maestro.id,
                'maestro_nombre': estudio.maestro.name,
                'maestro_lastname': estudio.maestro.lastname,
                'total_presentes': presentes,
                'total_ausentes': ausentes
            })
        return estudios_data

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('index'))

@login_required
def detalle_estudio(request, estudio_id):
    estudio = get_object_or_404(EstudioBiblico, id=estudio_id)
    asistencias = AsistenciaEstudio.objects.filter(
        date=estudio.fecha,
        attendance_type=AttendanceType.ESTUDIO
    ).select_related('miembro')

    presentes = asistencias.filter(presente=True)
    ausentes = asistencias.filter(presente=False)

    return render(request, 'estudio/detalle_estudio.html', {
        'estudio': estudio,
        'presentes': presentes,
        'ausentes': ausentes,
        'total_presentes': presentes.count(),
        'total_ausentes': ausentes.count()
    })