
from django.forms import *
from django import forms
from app.models import *
from django_select2.forms import  ModelSelect2Widget, ModelSelect2MultipleWidget



# Create Miembro
class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    cargo = forms.ModelChoiceField(queryset=Cargo.objects.all(), label="Cargos", empty_label="Seleccione un cargo", widget=forms.Select(attrs={'class': 'form-control'}))
    

    class Meta:
        model = Miembro
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese un nombre'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese su numero de identidad'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'date_joined': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Direccion'}),
            'fecha_ingreso': forms.DateInput(format='%Y-%m-%d', attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'type': 'phone','placeholder':  'Ingrese sin guión'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'type': 'email', 'placeholder': 'email'}),
            # 'cargo': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'type': 'file'})
        }


    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if dni:
            if len(dni) != 13 or not dni.replace("-", "").isdigit():
                raise forms.ValidationError("El campo Cedula debe contener 11 números.")
        return dni
       

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            if len(phone) != 12 or not phone.replace("-", "").isdigit():
                raise forms.ValidationError("El campo teléfono debe  contener 10 números.")
        return phone
        

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

# Formulario para crear servicio
class PersonaSelect2Widget(ModelSelect2Widget):
    model = Persona
    search_fields = ['nombre__icontains', 'apellido__icontains']

    def get_queryset(self):
        return Persona.objects.all()
    
    def label_from_instance(self, obj):
        return f"{obj.nombre} {obj.apellido}"

class ParticipantesSelect2Widget(ModelSelect2MultipleWidget):
    model = Persona
    search_fields = ['nombre__icontains', 'apellido__icontains']

    def get_queryset(self):
        return Persona.objects.all()
    
    def label_from_instance(self, obj):
        return f"{obj.nombre} {obj.apellido}"

class ServicioForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos opcionales
        self.fields['descripcion'].required = False
        
        # Agregar clases CSS y placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
            

    class Meta:
        model = Servicio
        fields = '__all__'
        widgets = {
            'fecha': DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    'placeholder': 'Seleccione fecha'
                }
            ),
            'tipo_servicio': Select(
                attrs={
                    'class': 'form-control select2',
                    'placeholder': 'Seleccione tipo de servicio'
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese la dirección del culto'
                }
            ),
            'lectura': TextInput(
                attrs={
                    'placeholder': 'Ingrese la lectura bíblica'
                }
            ),
            'devocional': TextInput(
                attrs={
                    'placeholder': 'Ingrese el devocional'
                }
            ),
            # 'director_cultural': PersonaSelect2Widget(
            #     attrs={
            #         'class': 'form-control select2',
            #         # 'data-placeholder': 'Seleccione el director',
            #         'data-allow-clear': 'true'
            #     }
            # ),
            # 'participantes': ParticipantesSelect2Widget(
            #     attrs={
            #         'class': 'form-control select2',
            #         'data-placeholder': 'Seleccione los participantes',
            #         'data-allow-clear': 'true',
            #         'data-maximum-selection-length': '3',
            #         # 'style': 'width: 100%'  # Impor
            #     }
            # ),
            'mensaje': TextInput(
                attrs={
                    'placeholder': 'Ingrese el mensaje'
                }
            ),
            'ofrenda': TextInput(
                attrs={
                    'type': 'text',
                    'class': 'form-control money-input',
                    'placeholder': 'Ingrese el monto de la ofrenda'
                }
            ),
            'descripcion': Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Descripción (opcional)',
                    'style': 'resize: none;'
                }
            ),
        }

    def clean_ofrenda(self):
        """Validación para el campo ofrenda"""
        ofrenda = self.cleaned_data.get('ofrenda')
        try:
            # Convertir la cadena a float, manejando el formato de moneda
            ofrenda = float(str(ofrenda).replace('$', '').replace(',', ''))
            if ofrenda < 0:
                raise forms.ValidationError('La ofrenda no puede ser negativa.')
            return ofrenda
        except ValueError:
            raise forms.ValidationError('Por favor ingrese un valor válido para la ofrenda.')

    def clean_participantes(self):
        """Validación para el campo participantes"""
        participantes = self.cleaned_data.get('participantes')
        if participantes and participantes.count() > 3:
            raise forms.ValidationError('Solo puede seleccionar hasta 3 participantes.')
        return participantes

    def clean(self):
        """Validación general del formulario"""
        cleaned_data = super().clean()
        director = cleaned_data.get('director_cultural')
        participantes = cleaned_data.get('participantes')

        if director and participantes and director in participantes:
            raise forms.ValidationError(
                'El director cultural no puede ser también un participante.'
            )

        return cleaned_data

    def save(self, commit=True):
        """Sobreescribir el método save para manejar el guardado correctamente"""
        instance = super().save(commit=False)
        
        if commit:
            instance.save()
            self.save_m2m()  # Guardar relaciones many-to-many
            
        return instance

#Asistencia Form
class AsistenciaForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['miembro', 'date', 'present']

# Define un formset utilizando el form anterior
AsistenciaFormSet = modelformset_factory(Attendance, form=AsistenciaForm, extra=0)

#Tareas Form
class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['nombre', 'descripcion', 'fecha']
        widgets = {
            'nombre': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el título de la actividad'
                }
            ),
            'descripcion': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la descripción',
                    'rows': '4'
                }
            ),
            'fecha': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local'
                }
            ),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha is None:
            raise forms.ValidationError("La fecha es requerida")
        return fecha
 

#Notas Form       
class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['titulo', 'contenido']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título'}),
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ingrese el contenido'}),
        }
        

class EstadoForm(forms.ModelForm):
    class Meta:
        model = Estado
        fields = '__all__'
    
class CargoForm(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = ['nombre',  'es_cargo_principal', 'orden_jerarquico']

        required = {
            'orden_jerarquico': False,
        }

    def __init__(self, *args, **kwargs):
        super(CargoForm, self).__init__(*args, **kwargs)
        
        # Obtener una instancia válida de SeccionIglesia para el valor por defecto
        
        self.fields['es_cargo_principal'].initial = False  # Valor por defecto para 'es_cargo_principal'
        self.fields['orden_jerarquico'].initial = 0  # Valor por defecto para 'orden_jerarquico'
        
        # Hacer que 'nombre' sea el único campo requerido
        self.fields['nombre'].required = True
        self.fields['es_cargo_principal'].required = False
        self.fields['orden_jerarquico'].required = False


#form cambio de directiva
class ProcesoTransicionForm(forms.ModelForm):
    seccion = forms.ChoiceField(
        choices=secciones_choices,
        label="Sección",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'cargarPeriodos(this.value)'
        })
    )

    periodo_anterior = forms.ModelChoiceField(
        queryset=PeriodoDirectiva.objects.all(),
        label="Período Anterior",
        empty_label="Seleccione período anterior",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    periodo_nuevo = forms.ModelChoiceField(
        queryset=PeriodoDirectiva.objects.all(),
        label="Período Nuevo",
        empty_label="Seleccione período nuevo",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = ProcesoTransicion
        fields = [
            'seccion',
            'periodo_anterior',
            'periodo_nuevo',
            'fecha_inicio',
            'fecha_fin_planeada',
            'observaciones'
        ]
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin_planeada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        data = kwargs.get('data', None)
        
        if data and 'seccion' in data:
            seccion = data.get('seccion')
            if seccion:
                self.fields['periodo_anterior'].queryset = PeriodoDirectiva.objects.filter(
                    seccion=seccion,
                    estado='ACTIVO'
                )
                self.fields['periodo_nuevo'].queryset = PeriodoDirectiva.objects.filter(
                    seccion=seccion,
                    estado='PLANEANDO'
                )
            else:
                self.fields['periodo_anterior'].queryset = PeriodoDirectiva.objects.none()
                self.fields['periodo_nuevo'].queryset = PeriodoDirectiva.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        seccion = cleaned_data.get('seccion')
        periodo_anterior = cleaned_data.get('periodo_anterior')
        periodo_nuevo = cleaned_data.get('periodo_nuevo')

        if seccion:
            if periodo_anterior and periodo_anterior.seccion != seccion:
                self.add_error('periodo_anterior', 'El período anterior debe pertenecer a la sección seleccionada')

            if periodo_nuevo and periodo_nuevo.seccion != seccion:
                self.add_error('periodo_nuevo', 'El período nuevo debe pertenecer a la sección seleccionada')

            if periodo_anterior and periodo_anterior.estado != 'ACTIVO':
                self.add_error('periodo_anterior', 'El período anterior debe estar en estado ACTIVO')

            if periodo_nuevo and periodo_nuevo.estado != 'PLANEANDO':
                self.add_error('periodo_nuevo', 'El período nuevo debe estar en estado PLANEANDO')

        return cleaned_data

class CandidatoTransicionForm(forms.ModelForm):
    class Meta:
        model = CandidatoTransicion
        fields = ['miembro', 'cargo_postulado']
        widgets = {
            'miembro': forms.Select(attrs={'class': 'form-control'}),
            'cargo_postulado': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        proceso_transicion = kwargs.pop('proceso_transicion', None)
        super().__init__(*args, **kwargs)
        
        if proceso_transicion:
            # Filtrar miembros y cargos basados en el proceso de transición
            self.fields['miembro'].queryset = Miembro.objects.filter(
                state__nombre='ACTIVO',
                category=proceso_transicion.seccion.nombre
            )
            
            self.fields['cargo_postulado'].queryset = Cargo.objects.filter(
                seccion=proceso_transicion.seccion
            )
    class Meta:
        model = CandidatoTransicion
        fields = ['miembro', 'cargo_postulado']


class PeriodoDirectivaForm(forms.ModelForm):
    class Meta:
        model = PeriodoDirectiva
        fields = '__all__'  # Esto incluirá todos los campos del modelo

        widgets = {
            'seccion': forms.Select(attrs={'class': 'form-control'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }

#Presentacion de Niño
class PresentacionNinoForm(forms.ModelForm):
    class Meta:
        model = PresentacionNino
        fields = '__all__'
        exclude = ['fecha_registro']
        widgets = {
            'nombre_nino': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre completo'
            }),
            'fecha_nacimiento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'lugar_nacimiento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Lugar de nacimiento'
            }),
            'nombre_padre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo del padre'
            }),
            'nombre_madre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre completo de la madre'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección completa'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número de teléfono'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
            'fecha_presentacion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'pastor_oficiante': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del pastor'
            }),
            'testigos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Nombres de los testigos'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observaciones adicionales'
            }),
            'acta_nacimiento': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,.jpg,.jpeg,.png'
            }),
        }

#Estudio Biblico
class EstudioBiblicoForm(forms.ModelForm):
    class Meta:
        model = EstudioBiblico
        fields = ['fecha', 'tema', 'maestro', 'descripcion', 'versiculo_clave', 'duracion']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }

#Registro Financiero
class RegistroFinancieroForm(forms.ModelForm):
    class Meta:
        model = RegistroFinanciero
        fields = ['fecha', 'diezmo', 'ofrenda', 'notas']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'diezmo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'ofrenda': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }