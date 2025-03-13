from django.contrib import messages
from django.db import IntegrityError
from django.http import  JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from app.mixins import GroupRequiredMixin
from app.models import *
from app.forms import PeriodoDirectivaForm, ProcesoTransicionForm, CandidatoTransicionForm
from django.db.models import F
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

class ProcesoTransicionListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    model = ProcesoTransicion
    group_name = 'damas'
    template_name = 'directiva/proceso_transicion_list.html'
    context_object_name = 'procesos'

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get('estado')
        print(f"Estado seleccionado: {estado}")  # Para depuración
        if estado:
            queryset = queryset.filter(estado=estado)
            print(f"Cantidad de registros filtrados: {queryset.count()}")  # Para depuración
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['estados_choices'] = TRANSACION_CHOICES
        context['estado_seleccionado'] = self.request.GET.get('estado', '')
        return context

class ProcesoTransicionCreateView(LoginRequiredMixin, CreateView):
    model = ProcesoTransicion
    template_name = 'directiva/proceso_transicion_form.html'
    form_class = ProcesoTransicionForm
    success_url = reverse_lazy('asys:proceso_transicion_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Solo limpiar los querysets si es una petición GET (mostrar formulario)
        if self.request.method == 'GET':
            form.fields['periodo_nuevo'].queryset = PeriodoDirectiva.objects.none()
            form.fields['periodo_anterior'].queryset = PeriodoDirectiva.objects.none()
            
        # Si es POST, mantener los querysets completos para validación
        elif self.request.method == 'POST' and 'seccion' in self.request.POST:
            seccion_id = self.request.POST.get('seccion')
            form.fields['periodo_anterior'].queryset = PeriodoDirectiva.objects.filter(
                seccion=seccion_id,
                estado='ACTIVO'
            )
            form.fields['periodo_nuevo'].queryset = PeriodoDirectiva.objects.filter(
                seccion=seccion_id,
                estado='PLANEANDO'
            )
            
        return form

    def get_initial(self):
        initial = super().get_initial()
        initial['fecha_inicio'] = timezone.now()
        return initial

# Vistas API para cargar los períodos
def get_periodos_activos(request, seccion_id):
    periodos = PeriodoDirectiva.objects.filter(
        seccion=seccion_id,
        estado='ACTIVO'
    ).values('id', 'fecha_inicio', 'fecha_fin')
    periodos_list = list(periodos)
    # Formatear las fechas para mejor visualización
    for periodo in periodos_list:
        fecha_inicio = periodo['fecha_inicio'].strftime('%d/%m/%Y')
        fecha_fin = periodo['fecha_fin'].strftime('%d/%m/%Y') if periodo['fecha_fin'] else 'Actual'
        periodo['descripcion'] = f"Período {fecha_inicio} - {fecha_fin}"
    return JsonResponse(periodos_list, safe=False)

def get_periodos_planeados(request, seccion_id):
    periodos = PeriodoDirectiva.objects.filter(
        seccion=seccion_id,
        estado='PLANEANDO'
    ).values('id', 'fecha_inicio', 'fecha_fin')
    periodos_list = list(periodos)
    # Formatear las fechas para mejor visualización
    for periodo in periodos_list:
        fecha_inicio = periodo['fecha_inicio'].strftime('%d/%m/%Y')
        fecha_fin = periodo['fecha_fin'].strftime('%d/%m/%Y') if periodo['fecha_fin'] else 'No definido'
        periodo['descripcion'] = f"Período {fecha_inicio} - {fecha_fin}"
    return JsonResponse(periodos_list, safe=False)

class ProcesoTransicionDetailView(LoginRequiredMixin, DetailView):
    model = ProcesoTransicion
    template_name = 'directiva/proceso_transicion_detail.html'
    context_object_name = 'proceso'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las opciones del campo 'estado'
        estado_choices = self.model._meta.get_field('estado').choices
        context['estado_choices'] = estado_choices

        # Otros datos del contexto (candidatos, total de votos, etc.)
        candidatos = CandidatoTransicion.objects.filter(proceso_transicion=self.object)
        context['candidatos'] = candidatos
        context['total_votos'] = sum(c.votos for c in candidatos)
        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            with transaction.atomic():  # Añadimos transacción atómica
                proceso = self.get_object()
                nuevo_estado = request.POST.get('nuevo_estado')
                
                if nuevo_estado not in dict(TRANSACION_CHOICES).keys():
                    raise ValueError("Estado inválido")
                
                # Si el nuevo estado es COMPLETADO, actualizamos los períodos
                if nuevo_estado == 'COMPLETADO':
                    periodo_anterior = proceso.periodo_anterior
                    periodo_nuevo = proceso.periodo_nuevo
                    
                    # Actualizar período anterior
                    periodo_anterior.estado = 'FINALIZADO'
                    periodo_anterior.fecha_fin = timezone.now()
                    periodo_anterior.save()
                    
                    # Actualizar período nuevo
                    periodo_nuevo.estado = 'ACTIVO'
                    periodo_nuevo.save()
                
                proceso.estado = nuevo_estado
                proceso.save()
                
                if is_ajax:
                    return JsonResponse({
                        'success': True, 
                        'message': 'Estado actualizado correctamente'
                    })
                else:
                    messages.success(request, "Estado y períodos actualizados correctamente")
                    return redirect('asys:proceso_transicion_detail', pk=proceso.pk)
                
        except ValueError as e:
            if is_ajax:
                return JsonResponse({
                    'success': False, 
                    'errors': {'estado': [str(e)]}
                }, status=400)
            else:
                messages.error(request, str(e))
        except Exception as e:
            if is_ajax:
                return JsonResponse({
                    'success': False, 
                    'errors': {'general': [str(e)]}
                }, status=500)
            else:
                messages.error(request, f"Error al actualizar: {str(e)}")
        
        return redirect('asys:proceso_transicion_detail', pk=kwargs['pk'])
    
class RegistroFinanzasCreateView(LoginRequiredMixin, CreateView):
    model = RegistroFinanzas
    fields = ['periodo', 'total_miembros_recibidos', 'total_fondos_recibidos', 'observaciones']
    template_name = 'directiva/registro_finanzas_form.html'
    success_url = reverse_lazy('asys:finalizar_list')

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                form.save()
                data['success'] = True
            else:
                data['success'] = False
                data['errors'] = form.errors.as_json()
        except Exception as e:
            data['success'] = False
            data['errors'] = str(e)
        return JsonResponse(data)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        proceso_id = self.kwargs.get('proceso_id')  # Obtener el proceso_id desde los argumentos de la URL
        context['proceso_id'] = proceso_id
        return context

class RegistroFinanzasListView(LoginRequiredMixin, ListView):
    model = RegistroFinanzas
    template_name = 'directiva/registro_finanzas_list.html'
    context_object_name = 'registros'

    def get_queryset(self):
        proceso_id = self.kwargs.get('proceso_id')
        return RegistroFinanzas.objects.filter(periodo__transicion_nuevo__id=proceso_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proceso_id'] = self.kwargs.get('proceso_id')
        return context

class RegistroFinanzasUpdateView(LoginRequiredMixin, UpdateView):
    model = RegistroFinanzas
    fields = ['periodo', 'total_miembros_recibidos', 'total_fondos_recibidos', 'observaciones']
    template_name = 'directiva/registro_finanzas_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proceso_id'] = self.kwargs.get('proceso_id')
        return context

    def get_success_url(self):
        return reverse_lazy('asys:finalizar_list', kwargs={'proceso_id': self.kwargs['proceso_id']})

class RegistroFinanzasDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Obtiene el registro de finanzas a eliminar
        registro = get_object_or_404(RegistroFinanzas, pk=self.kwargs['pk'])
        # Elimina el registro
        registro.delete()
        # Redirige a la lista de registros financieros
        return redirect('asys:finalizar_list', proceso_id=self.kwargs['proceso_id'])

def registrar_candidato(request, proceso_id):
    proceso = get_object_or_404(ProcesoTransicion, pk=proceso_id)
    if request.method == 'POST':
        form = CandidatoTransicionForm(request.POST)
        if form.is_valid():
            candidato = form.save(commit=False)
            candidato.proceso_transicion = proceso
            try:
                candidato.save()
                messages.success(request, 'Candidato registrado exitosamente.')
            except IntegrityError:
                messages.error(request, 'Este candidato ya está registrado para este cargo.')
            return redirect('asys:proceso_transicion_detail', pk=proceso.id)
    else:
        form = CandidatoTransicionForm()
    return render(request, 'directiva/registrar_candidato.html', {'form': form, 'proceso': proceso})

def iniciar_votacion(request, proceso_id):
    proceso = get_object_or_404(ProcesoTransicion, pk=proceso_id)
    if request.method == 'POST':
        candidato_id = request.POST.get('candidato')
        try:
            candidato = CandidatoTransicion.objects.get(pk=candidato_id, proceso_transicion=proceso)
            candidato.votos = F('votos') + 1
            candidato.save()
        except CandidatoTransicion.DoesNotExist:
            messages.error(request, 'Candidato no válido.')
        return redirect('asys:proceso_transicion_detail', pk=proceso.id)
    candidatos = CandidatoTransicion.objects.filter(proceso_transicion=proceso)
    return render(request, 'directiva/iniciar_votacion.html', {'proceso': proceso, 'candidatos': candidatos})

class PeriodoDirectivaCreateView(LoginRequiredMixin, CreateView):
    model = PeriodoDirectiva
    template_name = 'directiva/periodo_directiva_form.html'
    form_class = PeriodoDirectivaForm  # Usamos el formulario personalizado
    success_url = reverse_lazy('asys:periodo_directiva_list')  # Redirige a la lista después de crear

    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Guardar el usuario creador
        return super().form_valid(form)
    

class PeriodoDirectivaListView(LoginRequiredMixin, ListView):
    model = PeriodoDirectiva
    template_name = 'directiva/periodo_directiva_list.html'
    context_object_name = 'periodos'

    def get_queryset(self):
        return PeriodoDirectiva.objects.all()  # Puedes personalizar la consulta según necesites


class PeriodoDirectivaUpdateView(LoginRequiredMixin, UpdateView):
    model = PeriodoDirectiva
    form_class = PeriodoDirectivaForm
    template_name = 'directiva/periodo_directiva_form.html'

    def get_success_url(self):
        return reverse_lazy('asys:periodo_directiva_list')  

class PeriodoDirectivaDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        periodo = get_object_or_404(PeriodoDirectiva, pk=self.kwargs['pk'])
        periodo.delete()
        return redirect('asys:periodo_directiva_list')
    
