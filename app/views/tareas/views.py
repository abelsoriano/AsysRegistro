import json
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from app.models import Tarea
from django.contrib.auth.mixins import LoginRequiredMixin
from app.forms import TareaForm

from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse


# Lista de tareas
class TareaListView(LoginRequiredMixin, ListView):
    model = Tarea
    template_name = 'tareas/tarea_list.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        return Tarea.objects.filter(usuario_asignado=self.request.user).order_by('fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TareaForm()
        return context

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        form = TareaForm(request.POST)
        
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuario_asignado = request.user
            tarea.save()
            
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'message': 'Tarea creada exitosamente'
                })
            return redirect('asys:tareas-list')
        
        if is_ajax:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
        
        # Si no es AJAX y hay errores, volver a mostrar el formulario
        return self.get(request, *args, **kwargs)

@require_http_methods(["POST"])
def completar_tarea(request, pk):
    try:
        data = json.loads(request.body)
        tarea = Tarea.objects.get(pk=pk, usuario_asignado=request.user)
        tarea.completado = data.get('completado', False)
        tarea.save()
        return JsonResponse({'success': True})
    except Tarea.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Tarea no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)



# @require_http_methods(["GET"])
def obtener_tarea(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            tarea = get_object_or_404(Tarea, pk=pk)
            print("Tarea obtenida:", tarea)
            data = {
                "nombre": tarea.nombre,
                "descripcion": tarea.descripcion,
               "fecha": tarea.fecha.strftime('%Y-%m-%dT%H:%M'),
                "usuario_asignado": tarea.usuario_asignado.id if tarea.usuario_asignado else None,
            }
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    else:
        return JsonResponse({"error": "Solicitud no válida"}, status=400)

class TareaUpdateView(LoginRequiredMixin, UpdateView):
    model = Tarea
    form_class = TareaForm
    template_name = 'tareas/tarea_list.html'
    success_url = reverse_lazy('asys:tareas-list')

    def get_object(self):
        return get_object_or_404(Tarea, pk=self.kwargs['pk'], usuario_asignado=self.request.user)

    def form_valid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fecha = form.cleaned_data['fecha']
                usuario_asignado = self.request.user

                # Verificar tareas conflictivas
                tareas_conflictivas = Tarea.objects.filter(
                    fecha__date=fecha.date(),
                    usuario_asignado=usuario_asignado
                ).exclude(id=self.object.id)

                if tareas_conflictivas.exists():
                    return JsonResponse({
                        'success': False,
                        'errors': f"Ya existe una tarea programada para esa fecha: {tareas_conflictivas[0].nombre}"
                    })

                self.object = form.save(commit=False)
                self.object.usuario_asignado = usuario_asignado
                self.object.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'errors': str(e)})
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
        return super().form_invalid(form)

