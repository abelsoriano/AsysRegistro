// Función para manejar la presentación secuencial de modales
let modales = document.querySelectorAll('.modal');
let indiceActual = -1; // Inicializamos a -1 para comenzar desde el primer modal

function manejarSiguienteModal() {
    indiceActual++; // Incrementamos para el próximo modal
    if (indiceActual < modales.length) {
        let modalBootstrap = new bootstrap.Modal(modales[indiceActual]);
        modalBootstrap.show();
    } else {
       if (indiceActual > 0) {  // Asegúrate de que haya al menos un modal mostrado anteriormente
           let ultimoModalElement = modales[indiceActual - 1];
           let ultimoModal = bootstrap.Modal.getInstance(ultimoModalElement);
           if (ultimoModal) {
                ultimoModal.hide(); // Cierra el último modal mostrado
           }
       }
    }
}





// Función para enviar datos del formulario con AJAX
function enviarFormulario(event, miembroId) {
    event.preventDefault();
    var form = event.target;
    var data = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: data,
        headers: {
            'X-CSRFToken': data.get('csrfmiddlewaretoken')
        }
    }).then(response => {
        if (!response.ok) {
            // Lanza un error con el estado para entender mejor el problema
            throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
    }).then(data => {
        console.log('Success:', data);
        $(form.closest('.modal')).modal('hide'); // Ocultamos el modal actual
        manejarSiguienteModal(); // Mostramos el siguiente modal
    }).catch(error => {
        console.error('Error:', error);
        alert('Hubo un error. Por favor, intenta de nuevo. ' + error.message);
    });

    return false;
}


document.addEventListener('DOMContentLoaded', function () {
    manejarSiguienteModal(); // Inicializamos el primer modal
});
