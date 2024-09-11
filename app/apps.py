from django.apps import AppConfig
from django.contrib import admin


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        import app.signals

# class AttendanceAdmin(admin.ModelAdmin):

