$(document).ready(function() {
    // Variables globales
    let modal = null;
    let currentMode = '';

    // Inicializamos el modal después de que el DOM esté listo
    const modalElement = document.getElementById('modalPersona');
    if (modalElement) {
        modal = new bootstrap.Modal(modalElement);
        
    }

    $(document).ready(function() {
        $('#id_director_cultural').select2();
        $('#id_participantes').select2();
    });

    // Inicializar Select2 para director cultural y participantes
    function configureSelect2(selector, url, placeholder) {
        $(selector).select2({
            theme: 'bootstrap-5',
            width: '100%',
            placeholder: placeholder,
            allowClear: true,
            ajax: {
                url: url,
                type: 'GET',
                data: params => ({ term: params.term }),
                processResults: function (data) {
                    // Asegúrate de que los datos estén en el formato correcto
                    const results = data.map(item => ({
                        id: item.id,
                        text: item.text
                    }));
                    return { results: results };
                }
            }
        });
    }

    configureSelect2('#id_participantes', '/get_personas/', 'Seleccione participantes');
    configureSelect2('#id_director_cultural', '/get_personas/', 'Seleccione director');

    // Inicializar AutoNumeric para el campo de ofrenda
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
        $('#nombrePersona').val('');
        $('#apellidoPersona').val('');
        modal.show();
    });

    $('#btnAddDirector').click(function() {
        currentMode = 'director';
        $('.modal-title').text('Agregar Nuevo Director');
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

        // Detectar la acción basada en el contexto del formulario
        let action = form.find('input[name="action"]').val() || 'add';
        data.append('action', action);

        $.ajax({
            url: form.attr('action'),
            type: 'POST',
            data: data,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log("Respuesta del servidor:", response);

                if (response.success) {
                    let message = action === 'edit' ? 
                        'Servicio actualizado correctamente' : 
                        'Servicio registrado correctamente';

                    // Verificar que la URL de redirección comienza con /
                    let redirectUrl = response.redirect_url;
                    if (redirectUrl && !redirectUrl.startsWith('/')) {
                        redirectUrl = '/' + redirectUrl;
                    }

                    // Intentar redirección directa primero
                    try {
                        console.log("Intentando redirección directa a:", redirectUrl);
                        window.location.href = redirectUrl;
                    } catch (e) {
                        console.error("Error en redirección directa:", e);

                        Swal.fire({
                            title: '¡Éxito!',
                            text: message,
                            icon: 'success',
                            confirmButtonText: 'OK',
                            allowOutsideClick: false
                        }).then((result) => {
                            if (result.isConfirmed && redirectUrl) {
                                console.log("Intentando redirección a:", redirectUrl);
                                window.location.href = redirectUrl;
                            }
                        });
                    }
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
                console.error("Error en la petición AJAX:", xhr);
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

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Configurar el token CSRF en las solicitudes AJAX
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    });

    // Función para guardar una persona
    function guardarPersona() {
        let nombre = $('#nombrePersona').val();
        let apellido = $('#apellidoPersona').val();

        if (!nombre || !apellido) {
            Swal.fire('Error', 'Por favor complete todos los campos', 'error');
            return;
        }

        $.ajax({
            url: '/asys/add_persona/',
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
});