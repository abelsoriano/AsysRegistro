from datetime import timedelta, datetime

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


class AttendanceCreateViewGeneral(GeneralAccessMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia_general')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {'success': False}
        try:
            # Filtrar todos los miembros sin limitar a una categoría específica
            miembros = Miembro.objects.all()
            current_day = date.today().strftime('%A')

            # Filtrar las inasistencias por el día específico para todas las categorías
            miembros_con_inasistencias = Attendance.objects.filter(
                present=False,
                day_of_week=current_day
            ).values('miembro').annotate(total_inasistencias=Count('id'))

            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if
                                              miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    # Crear la asistencia, asignando también el usuario actual
                    attendance = Attendance.objects.create(
                        miembro=miembro,
                        present=present,
                        date=timezone.now(),
                        day_of_week=current_day,
                        user=request.user  # Asigna el usuario actual
                    )

                    if not present and miembro.id in miembros_ids_con_inasistencias:
                        miembro_obj = Miembro.objects.get(id=miembro.id)
                        inasistencias = Attendance.objects.filter(
                            miembro=miembro_obj,
                            present=False,
                            day_of_week=current_day  # Contar solo inasistencias del día específico
                        ).count()
                        miembro_id_tag = f"miembro_id:{miembro_obj.id}"
                        messages.warning(request,
                                         f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias en {current_day}.",
                                         extra_tags=f"modal_trigger {miembro_id_tag}")

                except Exception as e:
                    messages.error(request,
                                   f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

            response_data['success'] = True
            return JsonResponse(response_data)

        except Exception as e:
            messages.error(request, f"Ha ocurrido un error al registrar la asistencia. Error: {str(e)}")
            response_data['error'] = str(e)
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Attendance'
        context['title'] = 'Creando Asistencia General'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['miembros'] = Miembro.objects.all()  # Mostrar todos los miembros en el contexto
        return context


class AttendanceCreateViewJovenes(JovenesAccessMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
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
            # Filtrar miembros por la categoría 'joven'
            miembros = Miembro.objects.filter(category='joven')
            current_day = date.today().strftime('%A')

            # Filtrar las inasistencias por el día específico y la categoría 'joven'
            miembros_con_inasistencias = Attendance.objects.filter(
                miembro__category='joven',
                present=False,
                day_of_week=current_day
            ).values('miembro').annotate(total_inasistencias=Count('id'))

            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if
                                              miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    attendance = Attendance.objects.create(
                        miembro=miembro,
                        present=present,
                        date=timezone.now(),
                        day_of_week=current_day,
                        user=request.user  # Asigna el usuario actual
                    )

                    if not present and miembro.id in miembros_ids_con_inasistencias:
                        miembro_obj = Miembro.objects.get(id=miembro.id)
                        inasistencias = Attendance.objects.filter(
                            miembro=miembro_obj,
                            present=False,
                            day_of_week=current_day  # Contar solo inasistencias del día específico
                        ).count()
                        miembro_id_tag = f"miembro_id:{miembro_obj.id}"
                        messages.warning(request,
                                         f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias en {current_day}.",
                                         extra_tags=f"modal_trigger {miembro_id_tag}")

                except Exception as e:
                    messages.error(request,
                                   f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

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
        context['title'] = 'Creando nueva Asistencia de los Jovenes'
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


class AttendanceCreateViewCaballeros(CaballerosAccessMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia_caballeros')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {'success': False}
        try:
            # Filtrar miembros por la categoría 'joven'
            miembros = Miembro.objects.filter(category='caballero')
            current_day = date.today().strftime('%A')

            # Filtrar las inasistencias por el día específico y la categoría 'joven'
            miembros_con_inasistencias = Attendance.objects.filter(
                miembro__category='caballero',
                present=False,
                day_of_week=current_day
            ).values('miembro').annotate(total_inasistencias=Count('id'))

            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if
                                              miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    attendance = Attendance.objects.create(
                        miembro=miembro,
                        present=present,
                        date=timezone.now(),
                        day_of_week=current_day
                    )

                    if not present and miembro.id in miembros_ids_con_inasistencias:
                        miembro_obj = Miembro.objects.get(id=miembro.id)
                        inasistencias = Attendance.objects.filter(
                            miembro=miembro_obj,
                            present=False,
                            day_of_week=current_day  # Contar solo inasistencias del día específico
                        ).count()
                        miembro_id_tag = f"miembro_id:{miembro_obj.id}"
                        messages.warning(request,
                                         f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias en {current_day}.",
                                         extra_tags=f"modal_trigger {miembro_id_tag}")

                except Exception as e:
                    messages.error(request,
                                   f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

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
        context['title'] = 'Creando nueva Asistencia de Caballeros'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class AttendanceCreateViewDamas(DamasAccessMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attendance
    form_class = AsistenciaForm
    template_name = 'asistencia/AsistenciaCreate.html'
    success_url = reverse_lazy('asys:list_asistencia_damas')

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        response_data = {'success': False}
        try:
            # Filtrar miembros por la categoría 'joven'
            miembros = Miembro.objects.filter(category='dama')
            current_day = date.today().strftime('%A')

            # Filtrar las inasistencias por el día específico y la categoría 'joven'
            miembros_con_inasistencias = Attendance.objects.filter(
                miembro__category='dama',
                present=False,
                day_of_week=current_day
            ).values('miembro').annotate(total_inasistencias=Count('id'))

            miembros_ids_con_inasistencias = [miembro['miembro'] for miembro in miembros_con_inasistencias if
                                              miembro['total_inasistencias'] >= 1]

            for miembro in miembros:
                try:
                    present = request.POST.get(f'presente_{miembro.id}', 'False') == 'True'
                    attendance = Attendance.objects.create(
                        miembro=miembro,
                        present=present,
                        date=timezone.now(),
                        day_of_week=current_day
                    )

                    if not present and miembro.id in miembros_ids_con_inasistencias:
                        miembro_obj = Miembro.objects.get(id=miembro.id)
                        inasistencias = Attendance.objects.filter(
                            miembro=miembro_obj,
                            present=False,
                            day_of_week=current_day  # Contar solo inasistencias del día específico
                        ).count()
                        miembro_id_tag = f"miembro_id:{miembro_obj.id}"
                        messages.warning(request,
                                         f"El miembro {miembro_obj.name} {miembro_obj.lastname} ha alcanzado {inasistencias} inasistencias en {current_day}.",
                                         extra_tags=f"modal_trigger {miembro_id_tag}")

                except Exception as e:
                    messages.error(request,
                                   f"Ha ocurrido un error al registrar la asistencia para el miembro {miembro.name}. Error: {str(e)}")

            response_data['success'] = True
            return JsonResponse(response_data)

        except Exception as e:
            messages.error(request, f"Ha ocurrido un error al registrar la asistencia. Error: {str(e)}")
            response_data['error'] = str(e)
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['miembros'] = Miembro.objects.filter(category='dama')
        context['entity'] = 'Attendance'
        context['title'] = 'Creando nueva Asistencia de las Damas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


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


# return redirect('asys:list_asistencia')

class AttendanceListJovenes(JovenesAccessMixin, ListView):
    model = Attendance
    template_name = 'asistencia/AsistenciaList.html'
    context_object_name = 'asistencias'
    permission_required = 'app.can_view_joven_attendances'

    def get_inattendance_count(self):
        current_month = date.today().month
        current_year = date.today().year
        month_start = date(current_year, current_month, 1)
        month_end = month_start + timedelta(days=31 - month_start.day)

        # Get all attendances for the current month
        user_attendances = Attendance.objects.filter(
            date__gte=month_start,
            date__lte=month_end,
            miembro__category='joven', present=False
        ).values('miembro').annotate(total_inasistencias=Count('id'))

        inattendance_count = user_attendances.count()
        return inattendance_count

    def get_queryset(self):
        # Filtrar solo las asistencias de la categoría
        queryset = Attendance.objects.filter(miembro__category='joven').annotate(
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
        context['title'] = 'Listado de los Jovenes'
        context['create_url'] = reverse_lazy('asys:crear_asistencia')
        context['list_url'] = reverse_lazy('list_asistencia')
        context['entity'] = 'Miembros'
        return context


class AttendanceListCaballeros(CaballerosAccessMixin, ListView):
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
            miembro__category='caballero', present=False
        ).values('miembro').annotate(total_inasistencias=Count('id'))

        inattendance_count = user_attendances.count()
        return inattendance_count

    def get_queryset(self):
        # Filtrar solo las asistencias de la categoría "caballero"
        queryset = Attendance.objects.filter(miembro__category='caballero').annotate(
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
        context['title'] = 'Listado de Caballeros'
        context['create_url'] = reverse_lazy('asys:create_asistencia-caballero')
        context['list_url'] = reverse_lazy('list_asistencia_caballeros')
        context['entity'] = 'Miembros'
        return context


class AttendanceListDamas(DamasAccessMixin, ListView):
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
            miembro__category='dama', present=False
        ).values('miembro').annotate(total_inasistencias=Count('id'))

        inattendance_count = user_attendances.count()
        return inattendance_count

    def get_queryset(self):
        # Filtrar solo las asistencias de la categoría
        queryset = Attendance.objects.filter(miembro__category='dama').annotate(
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
        context['title'] = 'Listado de las Damas'
        context['create_url'] = reverse_lazy('asys:create_asistencia_damas')
        context['list_url'] = reverse_lazy('list_asistencia_damas')
        context['entity'] = 'Miembros'
        return context


class AttendanceListGeneral(GeneralAccessMixin, ListView):
    model = Attendance
    template_name = 'asistencia/AsistenciaList.html'
    context_object_name = 'asistencias'
    permission_required = 'app_name.can_view_all_attendances'

    def get_inattendance_count(self):
        current_month = date.today().month
        current_year = date.today().year
        month_start = date(current_year, current_month, 1)
        month_end = month_start + timedelta(days=31 - month_start.day)

        user_attendances = Attendance.objects.filter(
            date__gte=month_start,
            date__lte=month_end,
            present=False
        ).exclude(
            miembro__category=['joven', 'dama', 'caballero']
        ).values('miembro').annotate(total_inasistencias=Count('id'))

        inattendance_count = user_attendances.count()
        return inattendance_count

    def get_queryset(self):
        # Obtener todas las asistencias, excluyendo las categorías específicas
        queryset = Attendance.objects.exclude(
            miembro__category__in=['joven', 'dama', 'caballero']
        ).annotate(
            fecha=Trunc('date', 'day'),
            weekday_name=ExtractWeekDay('date') - 1
        ).values('fecha', 'weekday_name').annotate(
            total=Count('id'),
            total_true=Count('id', filter=Q(present=True)),
            total_false=Count('id', filter=Q(present=False)),
        ).order_by('-fecha')

        # Convertir el número del día en nombre con un mapeo de días
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
        context['title'] = 'Listado General de Asistencias (Excluyendo Jóvenes, Damas y Caballeros)'
        context['create_url'] = reverse_lazy('asys:create_asistencia_general')
        context['list_url'] = reverse_lazy('asys:list_asistencia_general')
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
