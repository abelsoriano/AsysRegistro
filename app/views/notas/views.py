import json
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.http import require_http_methods
from app.forms import NotaForm
from app.models import Nota


class NotaView(CreateView, ListView):
    model = Nota
    form_class = NotaForm
    template_name = 'notas/listaNota.html'
    context_object_name = 'notas'
    success_url = reverse_lazy('asys:nota_list')
    ordering = ['-fecha_modificacion']

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        # Manejar petición AJAX para obtener una nota específica
        if is_ajax:
            if 'id' in kwargs:
                try:
                    nota = Nota.objects.get(pk=kwargs['id'])
                    return JsonResponse({
                        'success': True,
                        'nota': {
                            'titulo': nota.titulo,
                            'contenido': nota.contenido
                        }
                    })
                except Nota.DoesNotExist:
                    return JsonResponse({
                        'success': False, 
                        'error': 'Nota no encontrada'
                    })
            
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
        
        if is_ajax:
            try:
                # Si los datos vienen como JSON (para "ver más")
                if request.headers.get('Content-Type') == 'application/json':
                    body = json.loads(request.body)
                    offset = int(body.get('offset', 0))
                    limit = 3
                    notas = Nota.objects.all().order_by('fecha_creacion')[offset:offset+limit]
                    data = serializers.serialize('json', notas)
                    return JsonResponse(data, safe=False)
                
                # Si es un formulario (crear/actualizar)
                else:
                    action = request.POST.get('action', None)
                    
                    if action == 'update':
                        nota_id = request.POST.get('notaId')
                        nota = Nota.objects.get(pk=nota_id)
                        nota.titulo = request.POST.get('titulo')
                        nota.contenido = request.POST.get('contenido')
                        nota.save()
                    else:
                        # Crear nueva nota
                        form = self.form_class(request.POST)
                        if form.is_valid():
                            form.save()
                        else:
                            return JsonResponse({
                                'success': False,
                                'error': 'Datos inválidos'
                            })
                    
                    return JsonResponse({
                        'success': True
                    })
                    
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
                
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Notas'
        context['create_url'] = reverse_lazy('asys:nota_create')
        context['list_url'] = reverse_lazy('nota_list')
        context['entity'] = 'Nota'
        return context
    


@require_http_methods(["POST"])
def nota_delete(request, pk):
    try:
        nota = Nota.objects.get(pk=pk)
        nota.delete()
        return JsonResponse({'success': True})
    except Nota.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Nota no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

