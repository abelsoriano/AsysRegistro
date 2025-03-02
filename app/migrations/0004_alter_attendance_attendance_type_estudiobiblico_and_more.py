# Generated by Django 4.2.19 on 2025-02-25 17:44

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0003_presentacionnino_acta_nacimiento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance_type',
            field=models.CharField(choices=[('GEN', 'General'), ('YTH', 'Jóvenes'), ('LDS', 'Damas'), ('GNT', 'Caballeros'), ('EST', 'Estudio Bíblico')], default='GEN', max_length=3, verbose_name='Tipo de Asistencia'),
        ),
        migrations.CreateModel(
            name='EstudioBiblico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(default=django.utils.timezone.now)),
                ('tema', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('versiculo_clave', models.CharField(blank=True, max_length=200)),
                ('duracion', models.PositiveIntegerField(help_text='Duración en minutos', validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('maestro', models.ForeignKey(limit_choices_to={'cargo__nombre': 'Maestro'}, on_delete=django.db.models.deletion.PROTECT, related_name='estudios_impartidos', to='app.miembro')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que registró')),
            ],
            options={
                'verbose_name': 'Estudio Bíblico',
                'verbose_name_plural': 'Estudios Bíblicos',
                'ordering': ['-fecha'],
            },
        ),
        migrations.CreateModel(
            name='AsistenciaEstudio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Fecha')),
                ('presente', models.BooleanField(default=True)),
                ('attendance_type', models.CharField(choices=[('GEN', 'General'), ('YTH', 'Jóvenes'), ('LDS', 'Damas'), ('GNT', 'Caballeros'), ('EST', 'Estudio Bíblico')], default='GEN', max_length=3, verbose_name='Tipo de Asistencia')),
                ('miembro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.miembro', verbose_name='Miembro')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario que registró')),
            ],
            options={
                'verbose_name': 'AsistenciaEstudio',
                'verbose_name_plural': 'AsistenciaEstudios',
                'ordering': ['-date', 'miembro'],
                'indexes': [models.Index(fields=['date', 'attendance_type'], name='app_asisten_date_3acd55_idx'), models.Index(fields=['miembro', 'date'], name='app_asisten_miembro_288493_idx'), models.Index(fields=['presente', 'date'], name='app_asisten_present_36ee40_idx')],
                'unique_together': {('miembro', 'date', 'attendance_type')},
            },
        ),
    ]
