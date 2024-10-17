from datetime import timedelta, datetime
import json
import logging
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q, Subquery
from django.db.models.functions import Trunc, Concat, ExtractWeekDay

from django.db.models import Value, CharField

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt

from django.views.generic import *

from app.forms import AsistenciaForm
from app.models import *

from django.shortcuts import get_object_or_404

from app.signals import *


class BaseAttendanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'

    def process_attendance(self, request, miembros, attendance_type):
        response_data = {'success': False}
        try:
            current_day = date.today().strftime('%A')
            current_month = timezone.now().month

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    
                    # Crear la asistencia
                    Attendance.objects.create(
                        miembro=miembro,
                        present=present,
                        date=timezone.now().date(),
                        day_of_week=current_day,
                        user=request.user,
                        attendance_type=attendance_type
                    )
                    
                    # Verificar faltas este mes
                    if not present:
                        monthly_absences = Attendance.objects.filter(
                            miembro=miembro,
                            attendance_type=attendance_type,
                            date__month=current_month,
                            present=False
                        ).count()
                        
                        if monthly_absences >= 2:
                            attendance_type_display = dict(AttendanceType.choices)[attendance_type]
                            miembro_id_tag = f"miembro_id:{miembro.id}"
                            messages.warning(
                                request,
                                f"{miembro.name} {miembro.lastname} tiene {monthly_absences} faltas este mes en los culto de {attendance_type_display}.",
                                extra_tags=f"modal_trigger {miembro_id_tag}"
                            )
                    
                except Exception as e:
                    messages.error(request, f"Error al registrar asistencia para {miembro.name}: {str(e)}")
            
            response_data['success'] = True
            
        except Exception as e:
            messages.error(request, f"Error general: {str(e)}")
            response_data['error'] = str(e)
        
        return response_data


class AttendanceCreateViewGeneral(GeneralAccessMixin, BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia_general')

    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.all()
        response_data = self.process_attendance(request, miembros, AttendanceType.GENERAL)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia General',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': Miembro.objects.all()
        })
        return context


class AttendanceCreateViewJovenes(JovenesAccessMixin, BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia')

    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.filter(category='joven')
        response_data = self.process_attendance(request, miembros, AttendanceType.YOUTH)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia de Jóvenes',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': Miembro.objects.filter(category='joven')
        })
        

        # Paginación
        miembros = Miembro.objects.filter(category='joven')
        paginator = Paginator(miembros, 90)  # Dividir en páginas de 90 miembros cada una
        page_number = self.request.GET.get('page')
        try:
            miembros_pagina = paginator.page(page_number)
        except PageNotAnInteger:
            miembros_pagina = paginator.page(1)
        except EmptyPage:
            miembros_pagina = paginator.page(paginator.num_pages)
        context['miembros'] = miembros_pagina

        return context


class AttendanceCreateViewCaballeros(CaballerosAccessMixin, BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia_caballeros')

    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.filter(category='caballero')
        response_data = self.process_attendance(request, miembros, AttendanceType.GENTLEMEN)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia de Caballero',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': Miembro.objects.filter(category='caballero')
        })
        

        # Paginación
        miembros = Miembro.objects.filter(category='caballero')
        paginator = Paginator(miembros, 90)  # Dividir en páginas de 90 miembros cada una
        page_number = self.request.GET.get('page')
        try:
            miembros_pagina = paginator.page(page_number)
        except PageNotAnInteger:
            miembros_pagina = paginator.page(1)
        except EmptyPage:
            miembros_pagina = paginator.page(paginator.num_pages)
        context['miembros'] = miembros_pagina

        return context


class AttendanceCreateViewDamas(DamasAccessMixin,BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia_damas')

    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.filter(category='dama')
        response_data = self.process_attendance(request, miembros, AttendanceType.LADIES)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia de Jóvenes',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': Miembro.objects.filter(category='dama')
        })
        return context


@csrf_exempt
def guardar_status(request):
    print("Recibida petición para guardar status")  # Añadir este print
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print("Datos recibidos:", data)  # Añadir este print
            miembro_id = data.get('id')
            status = data.get('status')
            
            if not miembro_id or not status:
                return JsonResponse({
                    'error': 'ID del miembro y status son requeridos'
                }, status=400)
            
            miembro = get_object_or_404(Miembro, id=int(miembro_id))
            
            MiembroStatus.objects.create(
                miembro=miembro,
                status=status
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Estado guardado exitosamente'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Datos JSON inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
    
    return JsonResponse({
        'error': 'Método no permitido'
    }, status=405)


# return redirect('asys:list_asistencia')

class BaseAttendanceListView(ListView):
    model = Attendance
    template_name = 'asistencia/AsistenciaList.html'
    context_object_name = 'asistencias'

    def get_inattendance_count(self):
        current_month = date.today().month
        current_year = date.today().year
        month_start = date(current_year, current_month, 1)
        month_end = month_start + timedelta(days=31 - month_start.day)

        filters = {
            'date__gte': month_start,
            'date__lte': month_end,
            'present': False
        }
        
        if hasattr(self, 'attendance_type'):
            filters['attendance_type'] = self.attendance_type

        user_attendances = Attendance.objects.filter(
            **filters
        ).values('miembro').annotate(
            total_inasistencias=Count('id')
        )

        return user_attendances.count()

    def get_base_queryset(self):
        filters = {}
        if hasattr(self, 'attendance_type'):
            filters['attendance_type'] = self.attendance_type

        return Attendance.objects.filter(**filters).annotate(
            fecha=Trunc('date', 'day'),
            weekday_name=ExtractWeekDay('date') - 1
        ).values(
            'fecha',
            'weekday_name',
            'day_of_week'
        ).annotate(
            total=Count('id'),
            total_true=Count('id', filter=Q(present=True)),
            total_false=Count('id', filter=Q(present=False)),
        ).order_by('-fecha')

    def process_queryset(self, queryset):
        weekdays_mapping = {
            0: 'Domingo',
            1: 'Lunes',
            2: 'Martes',
            3: 'Miércoles',
            4: 'Jueves',
            5: 'Viernes',
            6: 'Sábado'
        }

        for entry in queryset:
            entry['weekday_name'] = weekdays_mapping.get(entry['weekday_name'], 'Desconocido')
        return queryset

class AttendanceListJovenes(JovenesAccessMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.YOUTH
    permission_required = 'app.can_view_joven_attendances'

    def get_queryset(self):
        queryset = self.get_base_queryset()
        return self.process_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Asistencia de Jóvenes',
            'create_url': reverse_lazy('asys:crear_asistencia'),
            'list_url': reverse_lazy('asys:list_asistencia'),
            'entity': 'Jóvenes',
            'inattendance_count': self.get_inattendance_count()
        })
        return context

class AttendanceListCaballeros(CaballerosAccessMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.GENTLEMEN
    permission_required = 'app.can_view_caballero_attendances'

    def get_queryset(self):
        queryset = self.get_base_queryset()
        return self.process_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Asistencia de Caballero',
            'create_url': reverse_lazy('asys:create_asistencia-caballero'),
            'list_url': reverse_lazy('asys:list_asistencia_caballeros'),
            'entity': 'Jóvenes',
            'inattendance_count': self.get_inattendance_count()
        })
        return context


class AttendanceListDamas(DamasAccessMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.LADIES
    permission_required = 'app.can_view_dama_attendances'

    def get_queryset(self):
        queryset = self.get_base_queryset()
        return self.process_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Asistencia de Damas',
            'create_url': reverse_lazy('asys:create_asistencia_damas'),
            'list_url': reverse_lazy('asys:list_asistencia_damas'),
            'entity': 'Jóvenes',
            'inattendance_count': self.get_inattendance_count()
        })
        return context


class AttendanceListGeneral(GeneralAccessMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.GENERAL
    permission_required = 'app_name.can_view_all_attendances'

    def get_queryset(self):
        queryset = self.get_base_queryset()
        return self.process_queryset(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado General de Asistencias',
            'create_url': reverse_lazy('asys:create_asistencia_general'),
            'list_url': reverse_lazy('asys:list_asistencia_general'),
            'entity': 'Miembros',
            'inattendance_count': self.get_inattendance_count()
        })
        return context


class AttendanceDetailsView(View):
    def get(self, request):
        date_str = request.GET.get('date')

        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Formato de fecha inválido. Debe ser YYYY-MM-DD.'}, status=400)

        details = list(Attendance.objects.filter(date=date).annotate(
            miembro_nombre_completo=Concat('miembro__name', Value(' '), 'miembro__lastname', output_field=CharField())
        ).values('id', 'miembro_nombre_completo', 'date', 'present'))

        return JsonResponse({'details': details})


class AttendaceUpdate(UpdateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Opcional: imprimir para depuración
        print(f'Editing object with id: {obj.id}')
        return obj

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {}
            try:
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    data['success'] = True
                else:
                    data['success'] = False
                    data['errors'] = form.errors
            except Exception as e:
                data['error'] = str(e)
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Asistencia'
        context['entity'] = 'Attendance'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class AttendanceUpdateGroup(TemplateView):
    template_name = 'asistencia/AsistenciaGroupEdit.html'
    success_url = reverse_lazy('asys:list_asistencia_caballeros')

    def get(self, request, *args, **kwargs):
        date_str = self.kwargs.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = date.strftime('%A')

        attendances = Attendance.objects.filter(date=date)

        if not attendances.exists():
            miembros = Miembro.objects.all()
            for miembro in miembros:
                Attendance.objects.create(
                    miembro=miembro,
                    date=date,
                    present=False,
                    day_of_week=day_of_week
                )
            attendances = Attendance.objects.filter(date=date)

        context = self.get_context_data(attendances=attendances, date=date_str)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        date_str = self.kwargs.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        attendances = Attendance.objects.filter(date=date)

        # Si es una solicitud AJAX, devolver JSONResponse
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {'success': True}
            try:
                for attendance in attendances:
                    attendance.present = request.POST.get(f'presente_{attendance.miembro.id}') == 'True'
                    attendance.save()
            except Exception as e:
                data['success'] = False
                data['errors'] = str(e)
            return JsonResponse(data)

        # Si no es AJAX, redirigir de forma tradicional
        for attendance in attendances:
            attendance.present = request.POST.get(f'presente_{attendance.miembro.id}') == 'True'
            attendance.save()

        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Asistencia'
        context['entity'] = 'Attendance'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context
