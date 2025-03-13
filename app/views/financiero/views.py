from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Sum
from django.utils import timezone
import datetime

from app.models import RegistroFinanciero
from app.forms import RegistroFinancieroForm

# Vistas para RegistroFinanciero
class RegistroFinancieroListView(LoginRequiredMixin, ListView):
    model = RegistroFinanciero
    template_name = 'finanza/registro_list.html'
    context_object_name = 'registros'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros opcionales para la fecha
        fecha_inicio = self.request.GET.get('fecha_inicio')
        fecha_fin = self.request.GET.get('fecha_fin')
        
        if fecha_inicio:
            queryset = queryset.filter(fecha__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha__lte=fecha_fin)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        
        # Agregamos totales
        totales = queryset.aggregate(
            total_diezmo=Sum('diezmo'),
            total_ofrenda=Sum('ofrenda')
        )
        
        # Calculamos el total general
        total_general = 0
        if totales['total_diezmo']:
            total_general += totales['total_diezmo']
        if totales['total_ofrenda']:
            total_general += totales['total_ofrenda']
            
        context['totales'] = totales
        context['total_general'] = total_general
        
        # Conservamos los filtros actuales
        context['filtros'] = {
            'fecha_inicio': self.request.GET.get('fecha_inicio', ''),
            'fecha_fin': self.request.GET.get('fecha_fin', '')
        }
        
        return context

class RegistroFinancieroDetailView(LoginRequiredMixin, DetailView):
    model = RegistroFinanciero
    template_name = 'finanza/registro_detail.html'
    context_object_name = 'registro'

class RegistroFinancieroCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = RegistroFinanciero
    form_class = RegistroFinancieroForm
    template_name = 'finanza/registro_form.html'
    success_url = reverse_lazy('asys:registro_list')
    success_message = "Registro financiero creado con éxito"
    
    def get_initial(self):
        return {'fecha': timezone.now().date()}

class RegistroFinancieroUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = RegistroFinanciero
    form_class = RegistroFinancieroForm
    template_name = 'finanza/registro_form.html'
    success_url = reverse_lazy('asys:registro_list')
    success_message = "Registro financiero actualizado con éxito"

class RegistroFinancieroDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = RegistroFinanciero
    template_name = 'finanza/registro_confirm_delete.html'
    success_url = reverse_lazy('asys:registro_list')
    success_message = "Registro financiero eliminado con éxito"
