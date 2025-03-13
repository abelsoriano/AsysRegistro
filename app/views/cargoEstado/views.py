
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from app.forms import EstadoForm, CargoForm
from app.mixins import GroupRequiredMixin
from app.models import Estado, Cargo
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

class ModelEstadoCreateView(CreateView):
    model = Estado
    group_name = 'general' 
    form_class = EstadoForm
    template_name = 'cargoEstado/estadoList.html'
    success_url = reverse_lazy('asys:list-estado')

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
        context['titulo'] = 'Creando nuevo Estado'
        context['entity'] = 'Estado'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context
    
class ModelEstadoList(GroupRequiredMixin, ListView):
    group_name = 'general'
    model = Estado
      
    template_name='cargoEstado/estadoList.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'searchdata':
                for estado in Estado.objects.all():
                    data.append({
                        'id': estado.id,
                        'name': estado.name,
                        'desc': estado.desc if hasattr(estado, 'desc') else ''
                    })
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Estado'
        context['titulo'] = 'Creando nuevo Estado'
        context['list_url'] = reverse_lazy('list-estado')
        context['entity'] = 'Estado'
        return context

class EstadoUpdateView(UpdateView):
    model = Estado
    form_class = EstadoForm
    template_name = 'cargoEstado/estadoList.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            data = {}
            try:
                action = request.POST.get("action", None)
                if action == "edit":
                    form = self.get_form()
                    if form.is_valid():
                        form.save()
                        data["success"] = True
                        data["message"] = "Estado actualizado con éxito"
                    else:
                        data["success"] = False
                        data["errors"] = form.errors
                else:
                    data["error"] = "No ha ingresado a ninguna opción"
            except Exception as e:
                data["error"] = str(e)
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Estado'
        context['entity'] = 'Estado'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class DeleteEstado(DeleteView):
    model = Estado
    template_name = 'cargoEstado/estadoList.html'
    success_url = reverse_lazy('asys:list-estado')
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST.get('action', '')
            if action == 'delete':
                self.object.delete()
                data['success'] = True
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['entity'] = 'Estado'
        context['list_url'] = self.success_url
        context['action'] = 'delete'
        return context

@login_required
def get_estado(request, pk):
    try:
        estado = Estado.objects.get(pk=pk)
        data = {'name': estado.name}
        return JsonResponse(data)
    except Estado.DoesNotExist:
        return JsonResponse({'error': 'El estado no existe'}, status=404)
    
@require_http_methods(["POST"])
def delete_estado(request, id):
    try:
        estado = get_object_or_404(Estado, id=id)
        estado.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Este bloque es para la parte de cargo
class CargoList(GroupRequiredMixin, ListView):
    model = Cargo
    group_name = 'general' 
    template_name='cargoEstado/cargoFormList.html'

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = []
        try:
            action = request.POST['action']
            if action == 'searchdata':
                for cargo in Cargo.objects.all():
                    data.append({
                        'id': cargo.id,
                        'nombre': cargo.nombre,
                        # 'seccion': cargo.seccion,
                        'desc': cargo.desc if hasattr(cargo, 'desc') else ''
                    })
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data = {'error': str(e)}
        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Cargos'
        context['titulo'] = 'Creando nuevo Estado'
        context['list_url'] = reverse_lazy('list-cargo')
        context['entity'] = 'Cargo'
        return context


class CargoCreateView(CreateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargoEstado/cargoFormList.html'
    success_url = reverse_lazy('asys:list-cargo')

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
        context['titulo'] = 'Creando nuevo Cargo'
        context['entity'] = 'Cargo'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

@login_required
def get_cargo(request, pk):
    try:
        cargo = Cargo.objects.get(pk=pk)
        data = {'name': cargo.name}
        return JsonResponse(data)
    except Estado.DoesNotExist:
        return JsonResponse({'error': 'El estado no existe'}, status=404)
    
class CargoUpdateView(UpdateView):
    model = Cargo
    form_class = CargoForm
    template_name = 'cargoEstado/cargoList.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            data = {}
            try:
                action = request.POST.get("action", None)
                if action == "edit":
                    form = self.get_form()
                    if form.is_valid():
                        form.save()
                        data["success"] = True
                        data["message"] = "Estado actualizado con éxito"
                    else:
                        data["success"] = False
                        data["errors"] = form.errors
                else:
                    data["error"] = "No ha ingresado a ninguna opción"
            except Exception as e:
                data["error"] = str(e)
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Cargo'
        context['entity'] = 'Cargo'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context