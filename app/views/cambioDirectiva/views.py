
# from django.views.generic import *

# from django.utils.decorators import method_decorator
# from django.urls import reverse_lazy
# from django.contrib.auth.decorators import login_required
# from app.forms import CambioDirectivaForm
# from app.models import CambioDirectiva, Cargo, Miembro
# from django.http import JsonResponse



# class DirectivaCreate(CreateView):
#     model = CambioDirectiva
#     form_class = CambioDirectivaForm
#     template_name = 'cambioDirectiva/cambioDirectiva.html'
#     success_url = reverse_lazy('asys:miembro_list')

#     @method_decorator(login_required)
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         data = {}
#         try:
#             form = self.get_form()
#             print(f"Datos del formulario: {request.POST}")
#             if form.is_valid():
#                 form.save()
#                 data['success'] = True
#             else:
#                 data['success'] = False
#                 data['errors'] = form.errors.as_json()
#                 print(f"Errores del formulario: {form.errors}")
#         except Exception as e:
#             data['success'] = False
#             data['errors'] = str(e)
#             print(f"Error en el proceso de guardado: {e}")
#         return JsonResponse(data)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Cambio de directiva'
#         context['entity'] = 'CambioDirectiva'
#         context['list_url'] = self.success_url
#         context['action'] = 'add'
#         context['cargos'] = Cargo.objects.all()  # Asegúrate de cargar los cargos
#         context['miembros'] = Miembro.objects.all()  # Asegúrate de cargar los miembros
#         return context