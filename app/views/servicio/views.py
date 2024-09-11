from pyexpat.errors import messages

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from app.forms import ServicioForm
from app.models import Servicio, Persona


class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/CreateServicios.html'
    success_url = reverse_lazy('asys:service_list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Creando nuevo Servicio'
        context['entity'] = 'Servicios'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

@csrf_exempt
def add_persona(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        if nombre:
            persona, created = Persona.objects.get_or_create(nombre=nombre)
            return JsonResponse({'id': persona.id, 'nombre': persona.nombre})
        else:
            return JsonResponse({'error': 'Nombre no proporcionado'}, status=400)
    return JsonResponse({'error': 'Solicitud no válida'}, status=400)

class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicio/ServiceList.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = [i.toJSON() for i in Servicio.objects.all()]
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Servicio'
        context['create_url'] = reverse_lazy('asys:servicio_create')
        context['list_url'] = reverse_lazy('service_list')
        context['entity'] = 'Servicio'
        return context

class ServiceUpdate(UpdateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/CreateServicios.html'
    success_url = reverse_lazy('asys:service_list')

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
        context['title'] = 'Editar Servicio'
        context['entity'] = 'Miembros'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class ServiceDelete(DeleteView):
    model = Servicio
    template_name = 'servicio/delete.html'
    success_url = reverse_lazy('asys:service_list')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'delete':
                self.object.delete()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Borrar Servicio'
        context['entity'] = 'Servicio'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context

