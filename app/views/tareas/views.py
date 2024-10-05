from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from app.models import Tarea

from app.forms import TareasForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


# Lista de tareas
class TareaListView(ListView):
    model = Tarea
    template_name = 'tareas/tarea_list.html'

    def get_queryset(self):
        # Filtrar las tareas por el usuario actual
        return Tarea.objects.filter(usuario_asignado=self.request.user).order_by('fecha')


class TareaCreateView(CreateView):
    model = Tarea
    form_class = TareasForm
    template_name = 'tareas/crear_tarea.html'
    success_url = reverse_lazy('asys:tarea-lista')
    url_redirect = success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            data = {}
            try:
                action = request.POST.get('action', None)
                form = self.get_form()
                if action == 'add' and form.is_valid():
                    fecha = form.cleaned_data['fecha']

                    tareas_conflictivas = Tarea.objects.filter(fecha__date=fecha.date())
                    if tareas_conflictivas.exists():
                        # Si existe una tarea con la misma fecha, no guardar y mostrar advertencia
                        data['success'] = False
                        data[
                            'errors'] = f"Ya existe una tarea programada para esa fecha hecha por {tareas_conflictivas[0].usuario_asignado.first_name + ' ' + tareas_conflictivas[0].usuario_asignado.last_name}."
                    else:
                        # Asignar el usuario autenticado y guardar la tarea
                        tarea = form.save(commit=False)
                        tarea.usuario_asignado = request.user
                        tarea.save()
                        data['success'] = True
                else:
                    data['success'] = False
                    data['errors'] = form.errors.as_json()
            except Exception as e:
                data['success'] = False
                data['errors'] = str(e)
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creando una nueva tarea'
        context['entity'] = 'Tarea'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class CreateViewTareas(CreateView):
    model = Tarea
    form_class = TareasForm
    template_name = 'tareas/tarea_list.html'
    success_url = reverse_lazy('asys:tarea-lista')

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
        context['entity'] = 'Tarea'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

class TareaUpdateView(UpdateView):
    model = Tarea
    form_class = TareasForm
    template_name = 'tareas/crear_tarea.html'
    success_url = reverse_lazy('asys:tarea-lista')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = self.get_object()  # Cargar el objeto
            data = {}
            try:
                form = self.get_form()
                if form.is_valid():
                    fecha = form.cleaned_data['fecha']

                    # Verificar si hay otra tarea en la misma fecha
                    tareas_conflictivas = Tarea.objects.filter(fecha__date=fecha.date()).exclude(id=self.object.id)
                    if tareas_conflictivas.exists():
                        # Si existe una tarea conflictiva, mostrar advertencia
                        data['success'] = False
                        data[
                            'errors'] = f"Ya existe una tarea programada para esa fecha hecha por {tareas_conflictivas[0].usuario_asignado.first_name} {tareas_conflictivas[0].usuario_asignado.last_name}."
                    else:
                        # Guardar la tarea actualizada
                        form.save()
                        data['success'] = True
                else:
                    data['success'] = False
                    data['errors'] = form.errors.as_json()
            except Exception as e:
                data['success'] = False
                data['errors'] = str(e)
            return JsonResponse(data)
        else:
            return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editando una tarea'
        context['entity'] = 'Tarea'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


def get_estado(request, pk):
    try:
        tarea = Tarea.objects.get(pk=pk)
        data = {'nombre': tarea.nombre}
        return JsonResponse(data)
    except Tarea.DoesNotExist:
        return JsonResponse({'error': 'El estado no existe'}, status=404)