from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.forms import model_to_dict
from django.utils import timezone
from app.choices import *
from setting.settings import MEDIA_URL
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Estado(models.Model):
    name = models.CharField(max_length=50, verbose_name="Estado")

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Estado"
        verbose_name_plural = "Estados"
        db_table = "estado"
        ordering = ["id"]


class Cargo(models.Model):
    """Cargos dinámicos para cada sección"""
    nombre = models.CharField(max_length=50, verbose_name="Nombre del Cargo")
    # seccion = models.ForeignKey(SeccionIglesia, on_delete=models.CASCADE, related_name='cargos')
    es_cargo_principal = models.BooleanField(default=False)
    orden_jerarquico = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.nombre} "
    
    def toJSON(self):
        item = model_to_dict(self)
        return item


# Crearte miembros
class Miembro(models.Model):
    name = models.CharField(max_length=50, verbose_name="NOMBRE")
    lastname = models.CharField(max_length=50, verbose_name="APELLIDOS")
    dni = models.CharField(max_length=13, verbose_name="CEDULA", unique=True, null=True, blank=True)
    gender = models.CharField(max_length=15, choices=gender_choices, verbose_name="GENERO"    )
    date_joined = models.DateField(verbose_name="FECHA DE NACIMIENTO")
    address = models.CharField(max_length=150, verbose_name="DIRECCION")
    fecha_ingreso = models.DateField(verbose_name="FECHA DE INGRESO")
    phone = models.CharField(max_length=12, null=True, blank=True, verbose_name="TELEFONO")
    email = models.CharField(max_length=30, null=True, blank=True, verbose_name="CORREO ELECTRONICO")
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="CARGO")
    image = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name="IMAGEN")
    state = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="ESTADO")
    category = models.CharField(max_length=20, choices=category_choices, verbose_name="CATEGORIA")

    def is_birthday_today(self):
        return (
            self.date_joined.month == date.today().month
            and self.date_joined.day == date.today().day
        )

    def read_image(self):
        if self.image:
            try:
                with self.image.open() as f:
                    return f.read()
            except FileNotFoundError:
                pass
        return None

    def __str__(self):
        return self.name + " " + self.lastname

    def get_image(self):
        if self.image:
            return "{}{}".format(MEDIA_URL, self.image)
        return "{}{}".format(MEDIA_URL, "img/empty.png")

    def toJSON(self):
        data = model_to_dict(self)
        data["state"] = self.state.toJSON() if self.state else None
        data["cargo"] = self.cargo.toJSON() if self.cargo else None
        data["image"] = self.get_image()
        return data

    class Meta:
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"
        db_table = "miembro"
        ordering = ["id"]


class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="NOMBRE")
    apellido = models.CharField(max_length=100, verbose_name="APELLIDO")
    
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['nombre', 'apellido']
        unique_together = ['nombre', 'apellido']
    
    def clean(self):
        if Persona.objects.filter(
            nombre__iexact=self.nombre,
            apellido__iexact=self.apellido
        ).exists() and not self.pk:  # Añadido check para edición
            raise ValidationError('Ya existe una persona con este nombre y apellido')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Servicio(models.Model):
    tipo_servicio = models.CharField(max_length=20, choices=secciones_choices, verbose_name="TIPO DE SERVICIO")
    fecha = models.DateField(default=timezone.now, verbose_name="FECHA DE SERVICIO" )
    direccion = models.CharField(max_length=50, verbose_name="DIRECCIÓN DEL CULTO")
    lectura = models.TextField(max_length=50, verbose_name="LECTURA DE LA PALABRA")
    devocional = models.TextField(max_length=50, verbose_name="DEVOCIONAL")
    director_cultural = models.ForeignKey(Persona, on_delete=models.PROTECT, related_name='servicios_dirigidos', verbose_name="DIRECTOR DEL CULTURAL")
    participantes = models.ManyToManyField(Persona, related_name="eventos_participados", blank=True, verbose_name="PARTICIPANTES DEL CULTURAL")
    mensaje = models.TextField(max_length=50, verbose_name="MENSAJE DE LA PALABRA")
    ofrenda = models.CharField(max_length=13, verbose_name="OFRENDA")
    descripcion = models.TextField(blank=True, null=True, verbose_name="DESCRIPCIÓN")

    def __str__(self):
        return f"Servicio {self.get_tipo_servicio_display()} - {self.fecha}"

    def toJSON(self):
        item = model_to_dict(self)
        item['tipo_servicio'] = self.get_tipo_servicio_display()
        item['director_cultural'] = str(self.director_cultural)
        # Corregir la forma de obtener los participantes
        item['participantes'] = ", ".join(str(p) for p in self.participantes.all())
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['ofrenda'] = float(self.ofrenda)
        return item

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['-fecha']

 
class AttendanceType(models.TextChoices):
    GENERAL = 'GEN', _('General')
    YOUTH = 'YTH', _('Jóvenes')
    LADIES = 'LDS', _('Damas')
    GENTLEMEN = 'GNT', _('Caballeros')
    ESTUDIO = 'EST', 'Estudio Bíblico'
    

class Attendance(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE, verbose_name="Miembro")
    date = models.DateField(default=timezone.now, verbose_name="Fecha")
    present = models.BooleanField(default=False, verbose_name="Presente")
    day_of_week = models.CharField(max_length=10, blank=True, editable=False, verbose_name="Día de la Semana")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario que registró")
    attendance_type = models.CharField(max_length=3, choices=AttendanceType.choices, default=AttendanceType.GENERAL, verbose_name="Tipo de Asistencia")
    reason = models.TextField(blank=True, null=True, verbose_name="Motivo de Inasistencia")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def save(self, *args, **kwargs):
        # Actualizar el día de la semana automáticamente
        if not self.day_of_week:
            self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)

    @classmethod
    def get_monthly_absences(cls, miembro, month=None, year=None, attendance_type=None):
        queryset = cls.objects.filter(miembro=miembro, present=False)
        
        if month and year:
            queryset = queryset.filter(date__year=year, date__month=month)
        elif month:
            current_year = timezone.now().year
            queryset = queryset.filter(date__year=current_year, date__month=month)
        
        if attendance_type:
            queryset = queryset.filter(attendance_type=attendance_type)
        
        return queryset.count()

    def get_absence_alert(self):
        """
        Retorna un mensaje de alerta si el miembro tiene más de 2 faltas en el mes actual
        """
        current_month = self.date.month
        current_year = self.date.year
        absences = self.get_monthly_absences(
            self.miembro, 
            month=current_month,
            year=current_year,
            attendance_type=self.attendance_type
        )
        
        if absences >= 2:
            return {
                'alert': True,
                'message': f"{self.miembro.name} tiene {absences} faltas en el culto de {self.get_attendance_type_display()} este mes.",
                'absences': absences
            }
        return None

    def __str__(self):
        return f"Asistencia de {self.miembro} el {self.date} - {self.get_attendance_type_display()}"

    class Meta:
        verbose_name = "Asistencia"
        verbose_name_plural = "Asistencias"
        unique_together = ['miembro', 'date', 'attendance_type']
        ordering = ['-date', 'miembro']
        indexes = [
            models.Index(fields=['date', 'attendance_type']),
            models.Index(fields=['miembro', 'date']),
            models.Index(fields=['present', 'date']),
        ]

class Nota(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(
        auto_now=True
    )  # Este campo se actualiza automáticamente

    def __str__(self):
        return self.titulo

    def toJSON(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "contenido": self.contenido,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion,
        }


class Tarea(models.Model):
    nombre = models.CharField(max_length=200, verbose_name="Titulo de la actividad")
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(verbose_name="Ingresa la fecha de la actividad")
    usuario_asignado = models.ForeignKey(User, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False, verbose_name="¿Tarea completada?")

    def __str__(self):
        return self.nombre

    def toJSON(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'fecha': self.fecha.strftime('%Y-%m-%d %H:%M'),
            'completado': self.completado,
            'usuario_asignado': f"{self.usuario_asignado.first_name} {self.usuario_asignado.last_name}"
        }

#create directiva model
class PeriodoDirectiva(models.Model):
    seccion = models.CharField(max_length=50, choices=secciones_choices, default='JOVENES')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PLANEANDO')
    
    def __str__(self):
        return f"{self.seccion} - {self.fecha_inicio} a {self.fecha_fin or 'Actual'} ({self.get_estado_display()})"

class AsignacionDirectiva(models.Model):
    """Asignación de miembros a cargos en un período específico"""
    miembro = models.ForeignKey('Miembro', on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    periodo = models.ForeignKey(PeriodoDirectiva, on_delete=models.CASCADE)
    fecha_asignacion = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ['miembro', 'cargo', 'periodo']
    
    def __str__(self):
        return f"{self.miembro} - {self.cargo} ({self.periodo})"

class ProcesoTransicion(models.Model):
    """Proceso de cambio de directiva"""
    seccion = models.CharField(max_length=50, choices=secciones_choices, default='JOVENES')
    periodo_anterior = models.ForeignKey(PeriodoDirectiva, related_name='transicion_anterior', on_delete=models.CASCADE)
    periodo_nuevo = models.ForeignKey(PeriodoDirectiva, related_name='transicion_nuevo', on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=TRANSACION_CHOICES, default='PREPARACION')
    
    fecha_inicio = models.DateField()
    fecha_fin_planeada = models.DateField()
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Transición {self.seccion} - {self.fecha_inicio}"
    
@receiver(post_save, sender=ProcesoTransicion)
def actualizar_estados_periodos(sender, instance, **kwargs):
    if instance.estado == 'COMPLETADO':
        # Actualizar el período anterior a FINALIZADO
        periodo_anterior = instance.periodo_anterior
        periodo_anterior.estado = 'FINALIZADO'
        periodo_anterior.fecha_fin = timezone.now()
        periodo_anterior.save()

        # Actualizar el período nuevo a ACTIVO
        periodo_nuevo = instance.periodo_nuevo
        periodo_nuevo.estado = 'ACTIVO'
        periodo_nuevo.save()

class CandidatoTransicion(models.Model):
    """Candidatos para cargos en el proceso de transición"""
    proceso_transicion = models.ForeignKey(ProcesoTransicion, on_delete=models.CASCADE)
    miembro = models.ForeignKey('Miembro', on_delete=models.CASCADE)
    cargo_postulado = models.ForeignKey(Cargo, on_delete=models.CASCADE)
    votos = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ['proceso_transicion', 'miembro', 'cargo_postulado']
    
    def __str__(self):
        return f"{self.miembro} - Candidato a {self.cargo_postulado}"
    
    def toJSON(self):
        item = model_to_dict(self)
        return item

class RegistroFinanzas(models.Model):
    """Registro de finanzas por período de directiva"""
    periodo = models.ForeignKey(PeriodoDirectiva, on_delete=models.CASCADE)
    total_miembros_recibidos = models.IntegerField(default=0)
    total_fondos_recibidos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    fecha_registro = models.DateField(default=timezone.now)
    observaciones = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Registro Financiero {self.periodo}"

#Presentacion de niño
class PresentacionNino(models.Model):
    # Datos del niño
    nombre_nino = models.CharField(max_length=100, verbose_name="Nombre del Niño")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    lugar_nacimiento = models.CharField(max_length=200, verbose_name="Lugar de Nacimiento")
    acta_nacimiento = models.FileField(
        upload_to='actas_nacimiento/', 
        verbose_name="Acta de Nacimiento",
        help_text="Puede subir el acta de nacimiento en formato PDF o imagen",
        blank=True,
        null=True
    )
    
    # Datos de los padres
    nombre_padre = models.CharField(max_length=100, verbose_name="Nombre del Padre")
    nombre_madre = models.CharField(max_length=100, verbose_name="Nombre de la Madre")
    direccion = models.CharField(max_length=200, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo Electrónico")
    
    # Datos de la ceremonia
    fecha_presentacion = models.DateField(default=timezone.now, verbose_name="Fecha de Presentación")
    pastor_oficiante = models.CharField(max_length=100, verbose_name="Pastor Oficiante")
    
    # Campos adicionales
    testigos = models.TextField(blank=True, verbose_name="Testigos")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    
    class Meta:
        verbose_name = "Presentación de Niño"
        verbose_name_plural = "Presentaciones de Niños"
    
    def __str__(self):
        return f"Presentación de {self.nombre_nino} - {self.fecha_presentacion}"

class EstudioBiblico(models.Model):
    fecha = models.DateField(default=timezone.now)
    tema = models.CharField(max_length=200)
    maestro = models.ForeignKey('Miembro', on_delete=models.PROTECT, limit_choices_to={'cargo__nombre': 'Maestro'}, related_name='estudios_impartidos' )
    descripcion = models.TextField(blank=True)
    versiculo_clave = models.CharField(max_length=200, blank=True)
    duracion = models.PositiveIntegerField(help_text="Duración en minutos", validators=[MinValueValidator(1)])
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que registró")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Estudio Bíblico"
        verbose_name_plural = "Estudios Bíblicos"
        ordering = ['-fecha']

    def __str__(self):
        return f"Estudio: {self.tema} - {self.fecha}"

    def get_attendance_count(self):
        return Attendance.objects.filter(
            date=self.fecha,
            attendance_type=AttendanceType.ESTUDIO,
            present=True
        ).count()