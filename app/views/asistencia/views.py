from datetime import timedelta, datetime
import json
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.db.models.functions import Trunc, Concat, ExtractWeekDay

from django.db.models import Value, CharField

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from app.mixins import *

from django.views.decorators.csrf import csrf_exempt

from django.views.generic import *

from app.forms import AsistenciaForm
from app.models import *

from app.signals import *


# views.py
class BaseAttendanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    items_per_page = 90  # Definimos aquí el número de items por página

    def process_attendance(self, request, miembros, attendance_type):
        response_data = {'success': False, 'alerts': [], 'updated': 0, 'created': 0}
        try:
            current_day = date.today().strftime('%A')
            current_date = timezone.now().date()
            current_month = current_date.month

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    
                    # Intentar obtener registro existente o crear uno nuevo
                    attendance, created = Attendance.objects.get_or_create(
                        miembro=miembro,
                        date=current_date,
                        attendance_type=attendance_type,
                        defaults={
                            'present': present,
                            'day_of_week': current_day,
                            'user': request.user
                        }
                    )

                    if not created:
                        # Actualizar registro existente
                        attendance.present = present
                        attendance.user = request.user
                        attendance.save()
                        response_data['updated'] += 1
                    else:
                        response_data['created'] += 1

                    # Verificar faltas este mes
                    if not present:
                        monthly_absences = Attendance.objects.filter(
                            miembro=miembro,
                            attendance_type=attendance_type,
                            date__month=current_month,
                            date__year=current_date.year,
                            present=False
                        ).count()

                        if monthly_absences >= 2:
                            attendance_type_display = dict(AttendanceType.choices)[attendance_type]
                            alert = {
                                'miembro_id': miembro.id,
                                'name': f"{miembro.name} {miembro.lastname}",
                                'absences': monthly_absences,
                                'type': attendance_type_display
                            }
                            response_data['alerts'].append(alert)
                            messages.warning(
                                request,
                                f"{miembro.name} {miembro.lastname} tiene {monthly_absences} faltas este mes en {attendance_type_display}.",
                                extra_tags=f"modal_trigger miembro_id:{miembro.id}"
                            )

                except Exception as e:
                    messages.error(request, f"Error al procesar asistencia para {miembro.name}: {str(e)}")

            response_data['success'] = True
            if response_data['updated'] > 0:
                messages.info(request, f"Se actualizaron {response_data['updated']} registros existentes.")
            if response_data['created'] > 0:
                messages.success(request, f"Se crearon {response_data['created']} nuevos registros.")

        except Exception as e:
            messages.error(request, f"Error general: {str(e)}")
            response_data['error'] = str(e)

        return response_data

    def get_paginated_members(self, queryset):
        paginator = Paginator(queryset, self.items_per_page)
        page = self.request.GET.get('page')
        try:
            return paginator.page(page)
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)


class AttendanceCreateViewGeneral(BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia_general')
    
    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.all()
        response_data = self.process_attendance(request, miembros, AttendanceType.GENERAL)
        response_data['redirect_url'] = str(self.success_url)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        miembros = Miembro.objects.all()
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia General',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': self.get_paginated_members(miembros),
            'total_miembros': miembros.count(),
        })
        return context


class AttendanceCreateViewJovenes(BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia')
    
    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.filter(category='joven')
        response_data = self.process_attendance(request, miembros, AttendanceType.YOUTH)
        response_data['redirect_url'] = str(self.success_url)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        miembros = Miembro.objects.filter(category='joven')
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia de Jóvenes',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': self.get_paginated_members(miembros),
            'total_miembros': miembros.count()
        })
        return context

class AttendanceCreateViewCaballeros(BaseAttendanceCreateView):
    group_name = 'caballeros' 
    success_url = reverse_lazy('asys:list_asistencia_caballeros')
    
    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.filter(category='caballero')
        response_data = self.process_attendance(request, miembros, AttendanceType.GENTLEMEN)
        response_data['redirect_url'] = str(self.success_url)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        miembros = Miembro.objects.filter(category='caballero')
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia de Caballero',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': self.get_paginated_members(miembros),
            'total_miembros': miembros.count()
        })
        return context


class AttendanceCreateViewDamas(BaseAttendanceCreateView):
    success_url = reverse_lazy('asys:list_asistencia_damas')
    
    def post(self, request, *args, **kwargs):
        miembros = Miembro.objects.filter(category='dama')
        response_data = self.process_attendance(request, miembros, AttendanceType.LADIES)
        response_data['redirect_url'] = str(self.success_url)
        return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        miembros = Miembro.objects.filter(category='dama')
        context.update({
            'entity': 'Attendance',
            'title': 'Creando Asistencia de Damas',
            'list_url': self.success_url,
            'action': 'add',
            'miembros': self.get_paginated_members(miembros),
            'total_miembros': miembros.count()
        })
        return context




@require_http_methods(["POST"])
@csrf_exempt
def update_attendance_reason(request):
    try:
        data = json.loads(request.body)
        miembro_id = data.get('id')
        status = data.get('status')
        
        if not miembro_id or not status:
            return JsonResponse({
                'error': 'Se requiere ID del miembro y estado'
            }, status=400)
        
        # Obtener la asistencia más reciente del miembro
        attendance = Attendance.objects.filter(
            miembro_id=miembro_id,
            date=timezone.now().date()
        ).latest('created_at')
        
        # Mapear los estados a razones más descriptivas
        status_reasons = {
            'enfermo': 'Miembro se encuentra enfermo',
            'visitar': 'Miembro necesita ser visitado',
            'permiso': 'Miembro tiene permiso o excusa'
        }
        
        attendance.reason = status_reasons.get(status, status)
        attendance.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Estado actualizado exitosamente'
        })
    
    except Attendance.DoesNotExist:
        return JsonResponse({
            'error': 'No se encontró registro de asistencia para este miembro'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Datos JSON inválidos'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=500)


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

class AttendanceListJovenes(GroupRequiredMixin, BaseAttendanceListView, LoginRequiredMixin):
    group_name = 'jovenes' 
    attendance_type = AttendanceType.YOUTH
    
    

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
            'inattendance_count': self.get_inattendance_count(),
            'attendance_type': self.attendance_type 
        })
        return context

class AttendanceListCaballeros(GroupRequiredMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.GENTLEMEN
    group_name = 'caballeros' 

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
            'inattendance_count': self.get_inattendance_count(),
            'attendance_type': self.attendance_type 
        })
        return context


class AttendanceListDamas(GroupRequiredMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.LADIES
    group_name = 'damas' 

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
            'inattendance_count': self.get_inattendance_count(),
            'attendance_type': self.attendance_type 
        })
        return context


class AttendanceListGeneral(GroupRequiredMixin, BaseAttendanceListView):
    attendance_type = AttendanceType.GENERAL
    group_name = 'general' 

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
            'inattendance_count': self.get_inattendance_count(),
            'attendance_type': self.attendance_type 
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

class AttendanceUpdateGroup(TemplateView):
    template_name = 'asistencia/AsistenciaGroupEdit.html'

    def get_success_url(self, attendance_type=None):
        # Determinar la URL de redirección basada en el tipo de asistencia
        if attendance_type == AttendanceType.YOUTH:
            return reverse_lazy('asys:list_asistencia')
        elif attendance_type == AttendanceType.LADIES:
            return reverse_lazy('asys:list_asistencia_damas')
        elif attendance_type == AttendanceType.GENTLEMEN:
            return reverse_lazy('asys:list_asistencia_caballeros')
        elif attendance_type == AttendanceType.GENERAL:
            return reverse_lazy('asys:list_asistencia_general')
        return reverse_lazy('asys:list_asistencia')  # URL por defecto

    def get(self, request, *args, **kwargs):
        date_str = self.kwargs.get('date')
        attendance_type = self.kwargs.get('type')  # Obtener el tipo de la URL
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        day_of_week = date.strftime('%A')

        # Filtrar por fecha y tipo de asistencia
        attendances = Attendance.objects.filter(
            date=date,
            attendance_type=attendance_type
        )

        if not attendances.exists():
            # Filtrar miembros según el tipo de asistencia
            if attendance_type == AttendanceType.YOUTH:
                miembros = Miembro.objects.filter(category='joven')
            elif attendance_type == AttendanceType.LADIES:
                miembros = Miembro.objects.filter(category='dama')
            elif attendance_type == AttendanceType.GENERAL:
                miembros = Miembro.objects.all()
            elif attendance_type == AttendanceType.GENTLEMEN:
                miembros = Miembro.objects.filter(category='caballero')
            else:
                miembros = Miembro.objects.all()

            for miembro in miembros:
                Attendance.objects.create(
                    miembro=miembro,
                    date=date,
                    present=False,
                    day_of_week=day_of_week,
                    attendance_type=attendance_type
                )
            attendances = Attendance.objects.filter(
                date=date,
                attendance_type=attendance_type
            )

        context = self.get_context_data(
            attendances=attendances, 
            date=date_str,
            attendance_type=attendance_type
        )
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        date_str = self.kwargs.get('date')
        attendance_type = self.kwargs.get('type')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        attendances = Attendance.objects.filter(
            date=date,
            attendance_type=attendance_type
        )

        success_url = self.get_success_url(attendance_type)

        try:
            for attendance in attendances:
                attendance.present = request.POST.get(f'presente_{attendance.miembro.id}') == 'True'
                attendance.save()

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': success_url
                })
            return redirect(success_url)

        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error al actualizar la asistencia: {str(e)}')
            return redirect(success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        attendance_type = kwargs.get('attendance_type')
        
        # Determinar el título según el tipo de asistencia
        title_map = {
            AttendanceType.YOUTH: 'Editar Asistencia de Jóvenes',
            AttendanceType.LADIES: 'Editar Asistencia de Damas',
            AttendanceType.GENTLEMEN: 'Editar Asistencia de Caballeros',
            AttendanceType.GENERAL: 'Editar Asistencia General'
        }

        # Cambiar a `attendances` en lugar de `miembros`
        attendances = kwargs.get('attendances')
        
        context.update({
            'title': title_map.get(attendance_type, 'Editar Asistencia'),
            'entity': 'Attendance',
            'list_url': self.get_success_url(attendance_type),
            'action': 'edit',
            'attendances': attendances,
            'miembros': kwargs.get('attendances'),
            'date': kwargs.get('date')
        })
        return context

class AttendanceDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendance
    template_name = 'asistencia/delete.html'
    
    def get_success_url(self):
        # Determinar la URL de redirección basada en el tipo de asistencia
        attendance_type = self.object.attendance_type
        if attendance_type == AttendanceType.YOUTH:
            return reverse_lazy('asys:list_asistencia_jovenes')
        elif attendance_type == AttendanceType.LADIES:
            return reverse_lazy('asys:list_asistencia_damas')
        elif attendance_type == AttendanceType.GENTLEMEN:
            return reverse_lazy('asys:list_asistencia_caballeros')
        return reverse_lazy('asys:list_asistencia')  # URL por defecto

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'redirect_url': self.get_success_url()
                })
            return response
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=400)
            messages.error(request, f'Error al eliminar la asistencia: {str(e)}')
            return redirect(self.get_success_url())