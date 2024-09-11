
from datetime import date, timedelta, datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, Q
from django.db.models.functions import  Trunc, Concat, ExtractWeekDay


from django.db.models import Value, CharField

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import *

from app.forms import AsistenciaForm, NotaForm
from app.models import *

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages


class AttendanceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {'success': False}
        try:
            miembros = Miembro.objects.filter(category='joven')
            miembros_con_inasistencias = Attendance.objects.filter(miembro__category='joven', present=False).values('miembro').annotate(total_inasistencias=Count('id'))
            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    attendance = Attendance.objects.create(miembro=miembro, present=present, date=timezone.now(), day_of_week=date.today().strftime('%A'))

                    if not present and miembro.id in miembros_ids_con_inasistencias:
                        miembro_obj = Miembro.objects.get(id=miembro.id)
                        inasistencias = Attendance.objects.filter(miembro=miembro_obj, present=False).count()
                        miembro_id_tag = f"miembro_id:{miembro_obj.id}"
                        messages.warning(request,
                                         f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias.",
                                         extra_tags=f"modal_trigger {miembro_id_tag}")

                except Exception as e:
                    messages.error(request, f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

            response_data['success'] = True
            return JsonResponse(response_data)

        except Exception as e:
            messages.error(request, f"Ha ocurrido un error al registrar la asistencia. Error: {str(e)}")
            response_data['error'] = str(e)
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['miembros'] = Miembro.objects.filter(category='joven')
        context['entity'] = 'Attendance'
        context['title'] = 'Creando nueva Asistencia'
        context['list_url'] = self.success_url
        context['action'] = 'add'

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

class AttendanceCreateViewGeneral(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {'success': False}
        try:
            miembros = Miembro.objects.filter(category='caballero')
            miembros_con_inasistencias = Attendance.objects.filter(miembro__category='caballero', present=False).values('miembro').annotate(total_inasistencias=Count('id'))
            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    attendance = Attendance.objects.create(miembro=miembro, present=present, date=timezone.now(), day_of_week=date.today().strftime('%A'))

                    if not present and miembro.id in miembros_ids_con_inasistencias:
                        miembro_obj = Miembro.objects.get(id=miembro.id)
                        inasistencias = Attendance.objects.filter(miembro=miembro_obj, present=False).count()
                        miembro_id_tag = f"miembro_id:{miembro_obj.id}"
                        messages.warning(request,
                                         f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias.",
                                         extra_tags=f"modal_trigger {miembro_id_tag}")

                except Exception as e:
                    messages.error(request, f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

            response_data['success'] = True
            return JsonResponse(response_data)

        except Exception as e:
            messages.error(request, f"Ha ocurrido un error al registrar la asistencia. Error: {str(e)}")
            response_data['error'] = str(e)
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['miembros'] = Miembro.objects.filter(category='caballero')
        context['entity'] = 'Attendance'
        context['title'] = 'Creando nueva Asistencia'
        context['list_url'] = self.success_url
        context['action'] = 'add'

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



#Esta funcion es para guarda el estatus
def guardar_status(request):
    if request.method == 'POST':
        miembro_id = request.POST.get('id')
        status = request.POST.get('status')

        # Validation (same as before)
        if not miembro_id:
            return JsonResponse({'error': 'El ID del miembro no puede estar vacío'}, status=400)

        if miembro_id and status:
            if miembro_id.isdigit():
                try:
                    miembro = get_object_or_404(Miembro, id=int(miembro_id))
                    MiembroStatus.objects.create(miembro=miembro, status=status)
                    return JsonResponse({'success': 'Estado guardado exitosamente'}, status=200)
                except Miembro.DoesNotExist:
                    return JsonResponse({'error': 'El ID del miembro no existe'}, status=404)
            else:
                return JsonResponse({'error': 'El ID del miembro no es un número entero'}, status=400)

    return JsonResponse({'error': 'Solicitud no permitida'}, status=405)

    return redirect('asys:list_asistencia')

class AttendanceList(ListView):
    model = Attendance
    template_name = 'asistencia/AsistenciaList.html'
    context_object_name = 'asistencias'

    def get_inattendance_count(self):
        current_month = date.today().month
        current_year = date.today().year
        month_start = date(current_year, current_month, 1)
        month_end = month_start + timedelta(days=31 - month_start.day)

        # Get all attendances for the current month
        user_attendances = Attendance.objects.filter(
            date__gte=month_start,
            date__lte=month_end,
            miembros = Miembro.objects.filter(category='joven'),
            miembro__category='caballero', present=False).values('miembro').annotate(total_inasistencias=Count('id')
        )
        inattendance_count = user_attendances.filter(present=False).count()
        return inattendance_count

    def get_queryset(self):

        queryset = Attendance.objects.annotate(
            fecha=Trunc('date', 'day'),
            weekday_name=ExtractWeekDay('date') - 1
        ).values('fecha', 'weekday_name', 'day_of_week').annotate(
            total=Count('id'),
            total_true=Count('id', filter=Q(present=True)),
            total_false=Count('id', filter=Q(present=False)),
        ).order_by('-fecha')

        # Convert day number to name with list comprehension
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Miembros'
        context['miembros'] = Miembro.objects.filter(category='caballero')
        context['create_url'] = reverse_lazy('asys:crear_asistencia')
        context['list_url'] = reverse_lazy('list_asistencia')
        context['entity'] = 'Miembros'
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

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {}
            try:
                action = request.POST.get('action', None)
                if action == 'edit':
                    form = self.get_form()
                    if form.is_valid():
                        form.save()
                        data['success'] = True
                    else:
                        data['success'] = False
                        data['errors'] = form.errors
                else:
                    data['error'] = 'No ha ingresado a ninguna opción'
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

