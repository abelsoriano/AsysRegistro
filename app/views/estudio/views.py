# views.py
from django.db.models import Count
from django.db import models  # Importa el módulo models
from django.db.models import Q, F, Count  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.forms import EstudioBiblicoForm
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


@login_required
def lista_estudios(request):
    estudios = EstudioBiblico.objects.all().order_by('-fecha', '-id')
    
    # Process attendance counts for each study
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
    
    return render(request, 'estudio/lista_estudios.html', {
        'estudios': estudios_data
    })

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