# Generated by Django 5.1.4 on 2025-02-19 03:12

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre del Cargo')),
                ('es_cargo_principal', models.BooleanField(default=False)),
                ('orden_jerarquico', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
                'db_table': 'estado',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('contenido', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='PeriodoDirectiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.CharField(choices=[('JOVENES', 'Sociedad de Jóvenes'), ('CABALLEROS', 'Sociedad de Caballeros'), ('DAMAS', 'Sociedad de Damas'), ('GENERAL', 'Servicio General')], default='JOVENES', max_length=50)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('ACTIVO', 'Período Activo'), ('FINALIZADO', 'Período Finalizado'), ('PLANEANDO', 'En Planificación')], default='PLANEANDO', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Miembro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='NOMBRE')),
                ('lastname', models.CharField(max_length=50, verbose_name='APELLIDOS')),
                ('dni', models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='CEDULA')),
                ('gender', models.CharField(choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino')], max_length=15, verbose_name='GENERO')),
                ('date_joined', models.DateField(verbose_name='FECHA DE NACIMIENTO')),
                ('address', models.CharField(max_length=150, verbose_name='DIRECCION')),
                ('fecha_ingreso', models.DateField(verbose_name='FECHA DE INGRESO')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name='TELEFONO')),
                ('email', models.CharField(blank=True, max_length=30, null=True, verbose_name='CORREO ELECTRONICO')),
                ('image', models.ImageField(blank=True, null=True, upload_to='avatar', verbose_name='IMAGEN')),
                ('category', models.CharField(choices=[('joven', 'Joven'), ('dama', 'Dama'), ('caballero', 'Caballero'), ('adolecente', 'Adolecente')], max_length=20, verbose_name='CATEGORIA')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cargo', verbose_name='CARGO')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.estado', verbose_name='ESTADO')),
            ],
            options={
                'verbose_name': 'Empleado',
                'verbose_name_plural': 'Empleados',
                'db_table': 'miembro',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='NOMBRE')),
                ('apellido', models.CharField(max_length=100, verbose_name='APELLIDO')),
            ],
            options={
                'verbose_name': 'Persona',
                'verbose_name_plural': 'Personas',
                'ordering': ['nombre', 'apellido'],
                'unique_together': {('nombre', 'apellido')},
            },
        ),
        migrations.CreateModel(
            name='ProcesoTransicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seccion', models.CharField(choices=[('JOVENES', 'Sociedad de Jóvenes'), ('CABALLEROS', 'Sociedad de Caballeros'), ('DAMAS', 'Sociedad de Damas'), ('GENERAL', 'Servicio General')], default='JOVENES', max_length=50)),
                ('estado', models.CharField(choices=[('PREPARACION', 'En Preparación'), ('INSCRIPCION', 'Inscripción de Candidatos'), ('VOTACION', 'Proceso de Votación'), ('CONFIRMACION', 'Confirmación'), ('COMPLETADO', 'Proceso Completado')], default='PREPARACION', max_length=20)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin_planeada', models.DateField()),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('periodo_anterior', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transicion_anterior', to='app.periododirectiva')),
                ('periodo_nuevo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transicion_nuevo', to='app.periododirectiva')),
            ],
        ),
        migrations.CreateModel(
            name='RegistroFinanzas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_miembros_recibidos', models.IntegerField(default=0)),
                ('total_fondos_recibidos', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('fecha_registro', models.DateField(default=django.utils.timezone.now)),
                ('observaciones', models.TextField(blank=True, null=True)),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.periododirectiva')),
            ],
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_servicio', models.CharField(choices=[('JOVENES', 'Sociedad de Jóvenes'), ('CABALLEROS', 'Sociedad de Caballeros'), ('DAMAS', 'Sociedad de Damas'), ('GENERAL', 'Servicio General')], max_length=20, verbose_name='TIPO DE SERVICIO')),
                ('fecha', models.DateField(default=django.utils.timezone.now, verbose_name='FECHA DE SERVICIO')),
                ('direccion', models.CharField(max_length=50, verbose_name='DIRECCIÓN DEL CULTO')),
                ('lectura', models.TextField(max_length=50, verbose_name='LECTURA DE LA PALABRA')),
                ('devocional', models.TextField(max_length=50, verbose_name='DEVOCIONAL')),
                ('mensaje', models.TextField(max_length=50, verbose_name='MENSAJE DE LA PALABRA')),
                ('ofrenda', models.CharField(max_length=13, verbose_name='OFRENDA')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='DESCRIPCIÓN')),
                ('director_cultural', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='servicios_dirigidos', to='app.persona', verbose_name='DIRECTOR DEL CULTURAL')),
                ('participantes', models.ManyToManyField(blank=True, related_name='eventos_participados', to='app.persona', verbose_name='PARTICIPANTES DEL CULTURAL')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='Tarea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, verbose_name='Titulo de la actividad')),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(verbose_name='Ingresa la fecha de la actividad')),
                ('completado', models.BooleanField(default=False, verbose_name='¿Tarea completada?')),
                ('usuario_asignado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('present', models.BooleanField(default=False, verbose_name='Presente')),
                ('day_of_week', models.CharField(blank=True, editable=False, max_length=10, verbose_name='Día de la Semana')),
                ('attendance_type', models.CharField(choices=[('GEN', 'General'), ('YTH', 'Jóvenes'), ('LDS', 'Damas'), ('GNT', 'Caballeros')], default='GEN', max_length=3, verbose_name='Tipo de Asistencia')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Motivo de Inasistencia')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Última Actualización')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que registró')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.miembro', verbose_name='Miembro')),
            ],
            options={
                'verbose_name': 'Asistencia',
                'verbose_name_plural': 'Asistencias',
                'ordering': ['-date', 'miembro'],
                'indexes': [models.Index(fields=['date', 'attendance_type'], name='app_attenda_date_d7a085_idx'), models.Index(fields=['miembro', 'date'], name='app_attenda_miembro_8e8303_idx'), models.Index(fields=['present', 'date'], name='app_attenda_present_bb07fa_idx')],
                'unique_together': {('miembro', 'date', 'attendance_type')},
            },
        ),
        migrations.CreateModel(
            name='AsignacionDirectiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateField(default=django.utils.timezone.now)),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cargo')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.miembro')),
                ('periodo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.periododirectiva')),
            ],
            options={
                'unique_together': {('miembro', 'cargo', 'periodo')},
            },
        ),
        migrations.CreateModel(
            name='CandidatoTransicion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votos', models.IntegerField(default=0)),
                ('cargo_postulado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.cargo')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.miembro')),
                ('proceso_transicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.procesotransicion')),
            ],
            options={
                'unique_together': {('proceso_transicion', 'miembro', 'cargo_postulado')},
            },
        ),
    ]
