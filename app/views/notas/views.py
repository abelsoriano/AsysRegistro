from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers

from app.forms import NotaForm
from app.models import Nota


class NotaView(CreateView, ListView):
    model = Nota
    form_class = NotaForm
    template_name = 'notas/listaNota.html'
    context_object_name = 'notas'
    success_url = reverse_lazy('asys:nota_list')
    ordering = ['-fecha_modificacion']  # Ordenar por fecha de modificación descendente

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == "POST":
            import json
            body = json.loads(request.body)
            offset = int(body.get('offset', 0))
            limit = 3
            notas = Nota.objects.all().order_by('fecha_creacion')[offset:offset+limit]
            data = serializers.serialize('json', notas)
            return JsonResponse(data, safe=False)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Notas'
        context['create_url'] = reverse_lazy('asys:nota_create')
        context['list_url'] = reverse_lazy('nota_list')
        context['entity'] = 'Nota'
        return context

@method_decorator(csrf_exempt, name='dispatch')
class NotaDeleteView(DeleteView):
    model = Nota
    success_url = reverse_lazy('asys:nota_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'success': True})  


class NotaUpdateView(UpdateView):
    model = Nota
    form_class = NotaForm
    template_name = 'notas/listaNota.html'
    success_url = reverse_lazy('asys:nota_list')

    

@csrf_exempt
def cargar_mas_notas(request):
    if request.method == 'POST':
        offset = int(request.POST.get('offset', 0))
        limit = 3
        notas = Nota.objects.all().order_by('-fecha_modificacion')[offset:offset+limit]
        data = serializers.serialize('json', notas)
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)