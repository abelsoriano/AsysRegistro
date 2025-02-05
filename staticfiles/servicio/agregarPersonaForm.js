$(document).ready(function() {
    // Variables globales
    let modal = null;
    let currentMode = '';

    // Inicializamos el modal después de que el DOM esté listo
    const modalElement = document.getElementById('modalPersona');
    if (modalElement) {
        modal = new bootstrap.Modal(modalElement);
    }

    $(document).ready(function () {
        // Forzar la inicialización de los campos select2
        $('#id_director_cultural').djangoSelect2();
        $('#id_participantes').djangoSelect2();
    });

    $(document).ready(function () {
        // Opciones específicas si necesitas algo diferente a lo global
        $('#id_participantes').select2({
            theme: 'bootstrap-5',
            placeholder: 'Seleccione participantes',
            allowClear: true,
            width: '100%',
            ajax: {
                url: '/get_personas/', // Asegúrate de que coincida con la ruta definida en urls.py
                type: 'GET',           // La vista utiliza GET para obtener los datos
                data: function (params) {
                    return {
                        term: params.term // Envía el término de búsqueda al backend
                    };
                },
                processResults: function (data) {
                    return {
                        results: data // El formato esperado es un array de objetos {id, text}
                    };
                }
            }
        });
        

        $('#id_director_cultural').select2({
            ajax: {
                url: '/url/a/obtener/directores/',
                type: 'POST',
                data: function (params) {
                    return { term: params.term };
                },
                processResults: function (data) {
                    return {
                        results: data.results
                    };
                }
            }
        });
    });



            new AutoNumeric('#id_ofrenda', {
                decimalPlaces: 2,
                digitGroupSeparator: ',',
                decimalCharacter: '.',
                currencySymbol: '$ '
            });

        // Event Listeners
        $('#btnAddParticipante').click(function() {
            currentMode = 'participante';
            $('.modal-title').text('Agregar Nuevo Participante');
            // Limpiar campos antes de mostrar el modal
            $('#nombrePersona').val('');
            $('#apellidoPersona').val('');
            modal.show();
        });

        $('#btnAddDirector').click(function() {
            currentMode = 'director';
            $('.modal-title').text('Agregar Nuevo Director');
            // Limpiar campos antes de mostrar el modal
            $('#nombrePersona').val('');
            $('#apellidoPersona').val('');
            modal.show();
        });

        $('#btnGuardarPersona').click(function() {
            guardarPersona();
        });

        // Manejo del formulario principal
        $('form').on('submit', function (e) {
            e.preventDefault();
            let form = $(this);
            let data = new FormData(this);
            data.append('action', 'add');
            
            $.ajax({
                url: form.attr('action'),
                type: 'POST',
                data: data,
                processData: false,
                contentType: false,
                success: function (response) {
                    if (response.success) {
                        Swal.fire({
                            title: '¡Éxito!',
                            text: 'Servicio registrado correctamente',
                            icon: 'success',
                            confirmButtonText: 'OK'
                        }).then((result) => {
                            if (result.isConfirmed) {
                                window.location.href = '{{list_url}}';
                            }
                        });
                    } else {
                        let errorMessage = response.error_message || 'Hubo errores en el formulario:';
                        Swal.fire({
                            title: 'Error',
                            html: errorMessage.replace(/\n/g, '<br>'),
                            icon: 'error',
                            confirmButtonText: 'OK'
                        });
                    }
                },
                error: function (xhr) {
                    let errorMessage = 'Ha ocurrido un error inesperado';
                    try {
                        const response = JSON.parse(xhr.responseText);
                        if (response.error_message) {
                            errorMessage = response.error_message;
                        }
                    } catch(e) {
                        console.error('Error parsing response:', e);
                    }
                    Swal.fire('Error', errorMessage, 'error');
                }
            });
        });

        $.ajaxSetup({
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });


});



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) { // Línea corregida
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function guardarPersona() {
    let nombre = $('#nombrePersona').val();
    let apellido = $('#apellidoPersona').val();

    if (!nombre || !apellido) {
        Swal.fire('Error', 'Por favor complete todos los campos', 'error');
        return;
    }

    $.ajax({
        url: '{% url "asys:add_persona" %}',
        type: 'POST',
        data: JSON.stringify({
            nombre: nombre,
            apellido: apellido
        }),
        contentType: 'application/json',
        success: function (response) {
            if (response.id) {
                // Creamos la nueva opción
                const newOption = new Option(response.text, response.id, true, true);
                
                // Verificamos si la opción ya existe
                const targetSelect = currentMode === 'participante' ? 
                    $('#id_participantes') : 
                    $('#id_director_cultural');
                
                // Verificamos si ya existe la opción
                if (!targetSelect.find(`option[value="${response.id}"]`).length) {
                    targetSelect.append(newOption).trigger('change');
                }
                
                // Limpiamos los campos del formulario
                $('#nombrePersona').val('');
                $('#apellidoPersona').val('');
                
                // Cerramos el modal
                modal.hide();
                
                Swal.fire('¡Éxito!', 'Persona agregada correctamente', 'success');
            }
        },
        error: function (xhr, status, error) {
            let errorMessage = 'No se pudo agregar la persona';
            try {
                const response = JSON.parse(xhr.responseText);
                if (response.error && response.error.includes('already exists')) {
                    errorMessage = 'Esta persona ya existe en el sistema';
                }
            } catch(e) {
                console.error('Error parsing response:', e);
            }
            Swal.fire('Error', errorMessage, 'error');
        }
    });
}

