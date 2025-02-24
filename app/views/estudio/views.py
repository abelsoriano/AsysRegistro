# views.py
from django.db.models import Count
from django.db import models  # Importa el módulo models
from django.db.models import Q, F, Count  
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from app.forms import EstudioBiblicoForm
from app.models import Attendance, AttendanceType, EstudioBiblico, Miembro

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
        for miembro_id in request.POST.getlist('presentes'):
            Attendance.objects.update_or_create(
                miembro_id=miembro_id,
                date=estudio.fecha,
                attendance_type=AttendanceType.ESTUDIO,
                defaults={
                    'present': True,
                    'user': request.user,
                }
            )
        
        Attendance.objects.filter(
            date=estudio.fecha,
            attendance_type=AttendanceType.ESTUDIO
        ).exclude(
            miembro_id__in=request.POST.getlist('presentes')
        ).update(
            present=False,
            user=request.user
        )

        messages.success(request, 'Asistencia registrada exitosamente.')
        return redirect('asys:lista_estudios')

    asistencias = Attendance.objects.filter(
        date=estudio.fecha,
        attendance_type=AttendanceType.ESTUDIO,
        present=True
    )
    asistencias_ids = set(asistencias.values_list('miembro_id', flat=True))

    return render(request, 'estudio/registrar_asistencia.html', {
        'estudio': estudio,
        'miembros': miembros,
        'asistencias_ids': asistencias_ids,
    })

@login_required
def lista_estudios(request):
    estudios = EstudioBiblico.objects.values(
        'fecha', 'tema', 'maestro', 'id'
    ).annotate(
        total_presentes=Count('maestro__attendance', 
            filter=models.Q(
                maestro__attendance__date=models.F('fecha'),
                maestro__attendance__present=True,
                maestro__attendance__attendance_type=AttendanceType.ESTUDIO
            )
        ),
        total_ausentes=Count('maestro__attendance',
            filter=models.Q(
                maestro__attendance__date=models.F('fecha'),
                maestro__attendance__present=False,
                maestro__attendance__attendance_type=AttendanceType.ESTUDIO
            )
        )
    ).order_by('-fecha', '-id')

    # Obtener los detalles del maestro para cada estudio
    for estudio in estudios:
        estudio['maestro_nombre'] = Miembro.objects.get(id=estudio['maestro']).name

    return render(request, 'estudio/lista_estudios.html', {
        'estudios': estudios
    })

@login_required
def detalle_estudio(request, estudio_id):
    estudio = get_object_or_404(EstudioBiblico, id=estudio_id)
    asistencias = Attendance.objects.filter(
        date=estudio.fecha,
        attendance_type=AttendanceType.ESTUDIO
    ).select_related('miembro')

    presentes = asistencias.filter(present=True)
    ausentes = asistencias.filter(present=False)

    return render(request, 'estudio/detalle_estudio.html', {
        'estudio': estudio,
        'presentes': presentes,
        'ausentes': ausentes,
        'total_presentes': presentes.count(),
        'total_ausentes': ausentes.count()
    })