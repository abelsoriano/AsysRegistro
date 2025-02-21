from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from app.models import PresentacionNino
from app.forms import PresentacionNinoForm

class PresentacionNinoCreateView(SuccessMessageMixin, CreateView):
    model = PresentacionNino
    form_class = PresentacionNinoForm
    template_name = 'presentacion/presentacion_nino_form.html'
    success_url = reverse_lazy('lista_presentaciones')
    success_message = "Presentación registrada exitosamente"


class PresentacionListView(ListView):
    model = PresentacionNino
    template_name = 'presentacion/presentacion_list.html'
    context_object_name = 'presentaciones'
    ordering = ['-fecha_presentacion']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Presentaciones'
        return context

class PresentacionDetailView(DetailView):
    model = PresentacionNino
    template_name = 'presentacion/presentacion_detail.html'
    context_object_name = 'presentacion'

class PresentacionDeleteView(SuccessMessageMixin, DeleteView):
    model = PresentacionNino
    template_name = 'presentacion/presentacion_confirm_delete.html'
    success_url = reverse_lazy('lista_presentaciones')
    success_message = "Registro eliminado exitosamente"