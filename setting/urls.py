from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from app.views.servicio.views import get_personas
from login.views import LoginFormView, custom_404_view
from setting import settings

urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    path('', include('login.urls')),
    path('admin/', admin.site.urls),  # Corregido
    path('get_personas/', get_personas, name='get_personas'),
    path('select2/', include('django_select2.urls')),
    path('asys/', include('app.urls')),
]
handler404 = custom_404_view
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
