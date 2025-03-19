from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from setting import settings  # Importa las configuraciones de settings

from app.views.servicio.views import get_personas
from login.views import LoginFormView, custom_404_view

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('', include('login.urls')),
    path('admin/', admin.site.urls),
    path('get_personas/', get_personas, name='get_personas'),
    path('select2/', include('django_select2.urls')),
    path('asys/', include('app.urls')),
]

# Configurar el manejo de archivos estáticos y multimedia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Configuración personalizada para el manejo de errores 404
handler404 = custom_404_view
