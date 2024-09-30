from datetime import date

from django.db import models

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.utils import timezone
from app.choices import *
from setting.settings import MEDIA_URL
from django.contrib.auth.models import User


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
    name = models.CharField(max_length=50, verbose_name="Nombre")

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = "Cargo"
        verbose_name_plural = "Cargos"
        db_table = "cargo"
        ordering = ["id"]


# Crearte miembros
class Miembro(models.Model):
    name = models.CharField(max_length=50, verbose_name="NOMBRE")
    lastname = models.CharField(max_length=50, verbose_name="APELLIDOS")
    dni = models.CharField(
        max_length=13, verbose_name="CEDULA", unique=True, null=True, blank=True
    )
    gender = models.CharField(
        max_length=15, choices=gender_choices, verbose_name="GENERO"
    )
    date_joined = models.DateField(verbose_name="FECHA DE NACIMIENTO")
    address = models.CharField(max_length=150, verbose_name="DIRECCION")
    fecha_ingreso = models.DateField(verbose_name="FECHA DE INGRESO")
    phone = models.CharField(
        max_length=12, null=True, blank=True, verbose_name="TELEFONO"
    )
    email = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="CORREO ELECTRONICO"
    )
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name="CARGO")
    image = models.ImageField(
        upload_to="avatar", null=True, blank=True, verbose_name="IMAGEN"
    )
    state = models.ForeignKey(Estado, on_delete=models.CASCADE, verbose_name="ESTADO")
    category = models.CharField(
        max_length=20, choices=category_choices, verbose_name="CATEGORIA"
    )

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


# class CambioDirectiva(models.Model):
#     cantidad_miembros_recibidos = models.IntegerField(verbose_name='Cantidad de Miembros Recibidos')
#     fondos_recibidos = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Fondos Recibidos')
#     fecha_cambio = models.DateField(auto_now_add=True, verbose_name='Fecha de Cambio')

#     class Meta:
#         verbose_name = 'Cambio de Directiva'
#         verbose_name_plural = 'Cambios de Directivas'
#         db_table = 'cambio_directiva'
#         ordering = ['fecha_cambio']

# class DirectivaCargo(models.Model):
#     cambio_directiva = models.ForeignKey(CambioDirectiva, on_delete=models.CASCADE)
#     cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)
#     miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)


class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.message


class Persona(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre")

    def __str__(self):
        return self.nombre

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Servicio(models.Model):
    fecha = models.DateField(default=timezone.now, verbose_name="FECHA DE SERVICIO")
    direccion = models.CharField(
        max_length=50, verbose_name="DIRECCION DEL CULTO DE ALTAR"
    )
    lectura = models.TextField(max_length=50, verbose_name="LECTURA DE LA PALABRAS")
    devocional = models.TextField(max_length=50, verbose_name="DEVOCIONAL")
    cultural_1 = models.ForeignKey(
        "Persona",
        on_delete=models.CASCADE,
        related_name="eventos_dirigidos",
        verbose_name="Director del Cultural",
    )
    participantes = models.ManyToManyField(
        "Persona",
        related_name="eventos_participados",
        blank=True,
        verbose_name="Participantes del Cultural",
    )
    mensaje = models.TextField(max_length=50, verbose_name="MENSAJE DE LAS PALABRAS")
    ofrenda = models.CharField(max_length=13, verbose_name="OFRENDA")
    description = models.TextField(blank=True, null=True, verbose_name="DESCRIPCION")

    def __str__(self):
        return f"Evento dirigido por {self.cultural_1}"

    def toJSON(self):
        data = model_to_dict(self)
        data["cultural_1"] = self.cultural_1.toJSON() if self.cultural_1 else None
        data["participantes"] = [
            p.nombre for p in self.participantes.all()
        ]  # Asegúrate de que `Persona` tenga un método `toJSON`
        return data

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"


# class Attendance(models.Model):
#     miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
#     date = models.DateField(default=timezone.now)
#     present = models.BooleanField(default=False, null=True, blank=True, verbose_name='PRESENTE')
#     day_of_week = models.CharField(max_length=10, blank=True, editable=False, verbose_name='DÍA DE LA SEMANA')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def toJSON(self):
#         data = model_to_dict(self)
#         data['miembro'] = self.miembro.toJSON() if self.miembro else None
#         return data
#
#     class Meta:
#         verbose_name = 'Asistencia'
#         verbose_name_plural = 'Asistencias'


class Attendance(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    present = models.BooleanField(default=False)
    day_of_week = models.CharField(
        max_length=10, blank=True, editable=False, verbose_name="DÍA DE LA SEMANA"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Asistencia de {self.miembro} el {self.date}"

        class Meta:
            verbose_name = "Asistencia"
            verbose_name_plural = "Asistencias"


class MiembroStatus(models.Model):
    miembro = models.ForeignKey(Miembro, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100,
        choices=(
            ("enfermo", "Miembro se encuentra enfermo"),
            ("visitar", "Miembro necesita ser visitado"),
            ("permiso", "Miembro tiene permiso o excusa"),
        ),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.miembro.name} - {self.status}"

    class Meta:
        verbose_name = "StatusMiembro"
        verbose_name_plural = "StatusMiembros"


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
        item = model_to_dict(self)
        return item
