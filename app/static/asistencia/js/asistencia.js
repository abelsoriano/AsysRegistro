let indiceActual = 0;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Mensajes de inasistencia:', mensajesInasistencia);
    if (mensajesInasistencia.length > 0) {
        mostrarSiguienteAlerta();
    }
});

const mostrarSiguienteAlerta = () => {
    if (indiceActual < mensajesInasistencia.length) {
      const mensaje = mensajesInasistencia[indiceActual];
      Swal.fire({
        title: 'Notificación de Inasistencia',
        html: `
            <div style="font-size: 18px; color: #444;">
                ${mensaje.mensaje}
            </div><br>
            <div class="form-check" style="margin-bottom: 10px;">
                <input class="form-check-input" type="radio" name="status" value="enfermo" id="statusEnfermo">
                <label class="form-check-label" for="statusEnfermo">
                    Miembro se encuentra enfermo
                </label>
            </div>
            <div class="form-check" style="margin-bottom: 10px;">
                <input class="form-check-input" type="radio" name="status" value="visitar" id="statusVisitar">
                <label class="form-check-label" for="statusVisitar">
                    Miembro necesita ser visitado
                </label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="status" value="permiso" id="statusPermiso">
                <label class="form-check-label" for="statusPermiso">
                    Miembro tiene permiso o excusa
                </label>
            </div>
        `,
        showCancelButton: true,
        confirmButtonText: 'Guardar',
        cancelButtonText: 'Siguiente',
        customClass: {
            popup: 'styled-swal-popup',
            confirmButton: 'styled-swal-confirm-btn',
            cancelButton: 'styled-swal-cancel-btn'
        },
        buttonsStyling: false, 
        allowOutsideClick: false,
        preConfirm: () => {
            const selectedStatus = document.querySelector('input[name="status"]:checked');
            if (!selectedStatus) {
                Swal.showValidationMessage('Por favor seleccione un estado');
                return false;
            }
            return selectedStatus.value;
        }
    }).then((result) => {
        if (result.value) {
            guardarStatus(mensaje.miembroId, result.value);
        } else {
            indiceActual++;
            mostrarSiguienteAlerta();
        }
    });
    
    }
  }

function guardarStatus(miembroId, status) {
    console.log('Iniciando guardado de estado:', { miembroId, status });
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (!csrftoken) {
        console.error('No se encontró el token CSRF');
        return;
    }

    const requestData = {
        id: miembroId,
        status: status
    };
    
    console.log('Enviando datos:', requestData);

    fetch('/asys/guardar-status/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        console.log('Respuesta del servidor:', response.status);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text();
    })
    .then(text => {
        console.log('Texto de respuesta:', text);
        try {
            return JSON.parse(text);
        } catch (error) {
            console.error('Error al parsear respuesta:', text);
            throw new Error('Error al parsear respuesta del servidor');
        }
    })
    .then(data => {
        console.log('Datos procesados:', data);
        if (data.success) {
            Swal.fire({
                icon: 'success',
                title: 'Guardado',
                text: 'El estado se ha guardado correctamente',
                timer: 1500
            }).then(() => {
                indiceActual++;
                mostrarSiguienteAlerta();
            });
        } else {
            throw new Error(data.error || 'Error desconocido');
        }
    })
    .catch(error => {
        console.error('Error en la petición:', error);
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'Hubo un error al guardar el estado: ' + error.message
        }).then(() => {
            // Opcional: decidir si quieres pasar al siguiente en caso de error
            // indiceActual++;
            // mostrarSiguienteAlerta();
        });
    });
}