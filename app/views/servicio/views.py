import json
from django.db.models import Count, Q

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *
from django.db import transaction
from app.forms import ServicioForm
from app.models import Servicio, Persona


class ServicioCreateView(CreateView):
    model = Servicio
    form_class = ServicioForm
    template_name = 'servicio/CreateServicios.html'
    success_url = reverse_lazy('asys:service_list')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', 'add')

            if action == 'add':
                with transaction.atomic():
                    form = self.get_form()
                    if form.is_valid():
                        servicio = form.save()  
                        data['success'] = True
                        redirect_url = self.success_url
                        data['redirect_url'] = redirect_url
                    else:
                        data['success'] = False
                        data['errors'] = form.errors
                        data['error_message'] = '\n'.join([
                            f"{field}: {', '.join(errors)}"
                            for field, errors in form.errors.items()
                        ])

            elif action == 'get_personas':
                term = request.POST.get('term', '')
                personas = Persona.objects.filter(
                    Q(nombre__icontains=term) | Q(apellido__icontains=term)
                ).values('id', 'nombre', 'apellido')[:10]
                data = [
                    {
                        'id': persona['id'],
                        'text': f"{persona['nombre']} {persona['apellido']}"
                    } for persona in personas
                ]

        except Exception as e:
            data['success'] = False
            data['error_message'] = str(e)

        return JsonResponse(data, safe=False)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Servicio'
        context['entity'] = 'Servicio'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class PersonaCreateView(CreateView):
    model = Persona
    fields = ['nombre', 'apellido']

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            
            # Primero intentamos obtener la persona si ya existe
            persona, created = Persona.objects.get_or_create(
                nombre=nombre,
                apellido=apellido
            )
            
            # Ya sea que se creó o ya existía, devolvemos los datos
            return JsonResponse({
                'id': persona.id,
                'text': f"{persona.nombre} {persona.apellido}",
                'created': created  # opcional, por si quieres saber si fue creada o ya existía
            })
                
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Error al decodificar JSON'
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)

def get_personas(request):
    term = request.GET.get('term', '')
    personas = Persona.objects.filter(nombre__icontains=term)[:10]
    results = [{'id': p.id, 'text': f"{p.nombre} {p.apellido}"} for p in personas]
    return JsonResponse({'results': results})


class ServicioListView(ListView):
    model = Servicio
    template_name = 'servicio/ServiceList.html'
    paginate_by = 10  # Agregamos paginación
    success_url = reverse_lazy('asys:service_list')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action')
            if action == 'searchdata':
                # Agregamos filtros básicos
                term = request.POST.get('term', '')
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                tipo = request.POST.get('tipo')

                queryset = self.model.objects.all()

                if term:
                    queryset = queryset.filter(
                        descripcion__icontains=term
                    )
                if start_date:
                    queryset = queryset.filter(fecha__gte=start_date)
                if end_date:
                    queryset = queryset.filter(fecha__lte=end_date)
                if tipo:
                    queryset = queryset.filter(tipo_servicio=tipo)

                data = [servicio.toJSON() for servicio in queryset]
            else:
                data['error'] = 'No se especificó una acción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Listado de Servicios',
            'create_url': reverse_lazy('asys:servicio_create'),
            'list_url': reverse_lazy('asys:service_list'),
            'entity': 'Servicios',
            'tipos_servicio': dict(Servicio._meta.get_field('tipo_servicio').choices) 
        })
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
                action = request.POST.get('action')
                if action == 'edit':
                    form = self.get_form()
                    if form.is_valid():
                        form.save()
                        data['success'] = True
                        data['redirect_url'] = self.success_url
                    else:
                        data['success'] = False
                        data['error_message'] = '\n'.join([
                            f"{field}: {', '.join(errors)}"
                            for field, errors in form.errors.items()
                        ])
                else:
                    data['success'] = False
                    data['error_message'] = 'No ha ingresado a ninguna opción'
            except Exception as e:
                data['success'] = False
                data['error_message'] = str(e)
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Servicio'
        context['entity'] = 'Servicio'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class ServicioDeleteView(DeleteView):
    model = Servicio
    template_name = 'servicio/delete.html'
    success_url = reverse_lazy('asys:service_list')

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object = self.get_object()
            self.object.delete()
            data['success'] = True
            data['message'] = 'Servicio eliminado correctamente'
        except Exception as e:
            data['success'] = False
            data['error_message'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': 'Eliminación de un Servicio',
            'entity': 'Servicios',
            'list_url': self.success_url,
        })
        return context