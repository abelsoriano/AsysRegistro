from django.contrib import admin
from app.models import *

# Register your models here.
admin.site.register(Miembro)
admin.site.register(Cargo)
admin.site.register(Estado)
admin.site.register(Servicio)
admin.site.register(Nota)
admin.site.register(Tarea)



class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('miembro', 'date', 'present')
# class DirectivaCargoInline(admin.TabularInline):
#     model = DirectivaCargo
#     extra = 1

# @admin.register(CambioDirectiva)
# class CambioDirectivaAdmin(admin.ModelAdmin):
#     inlines = [DirectivaCargoInline]



admin.site.register(Attendance, AttendanceAdmin)


