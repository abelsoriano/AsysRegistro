

$(function () {
  $('#nuevaNota').on('click', function() {
    openSweetAlertForm('create');
  });


  window.openSweetAlertForm = function(action, id = null) {
    let title = (action === 'edit') ? "Editar Cargo" : "Crear nuevo Cargo";
    let url = (action === 'edit') ? `/asys/updateCargo/${id}/` : createUrl;
    let initialData = {};

    const processForm = () => {
        Swal.fire({
            title: title,
            html: `
                <form id="cargoForm">
                    <input type="text" id="id_nombre" nombre="nombre" class="swal2-input" value="${initialData.nombre || ''}" placeholder="Nombre del cargo" required>
                </form>
            `,
            showCancelButton: true,
            confirmButtonText: (action === 'edit') ? 'Actualizar' : 'Guardar',
            cancelButtonText: 'Cancelar',
            preConfirm: () => {
                const nombre = Swal.getPopup().querySelector('#id_nombre').value;
                if (!nombre) {
                    Swal.showValidationMessage('El nombre del cargo es obligatorio');
                    return false;
                }

                const formData = new FormData();
                formData.append('nombre', nombre);
                formData.append('action', action);

                console.log('Sending request to:', url);
                return fetch(url, {
                    method: "POST",
                    body: formData,
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest"
                    }
                }).then(response => {
                    console.log('Response received', response.status);
                    if (!response.ok) {
                        throw new Error("Error en el servidor");
                    }
                    return response.json();
                }).then(data => {
                    console.log('Response data:', data);
                    if (!data.success) {
                        throw new Error(data.error || "Error desconocido");
                    }
                    return data;
                }).catch(error => {
                    console.error('Fetch error:', error);
                    Swal.showValidationMessage(`Request failed: ${error}`);
                });
            }
        }).then((result) => {
            // console.log('Swal result:', result);
            if (result.value && result.value.success) {
                Swal.fire({
                    title: "Éxito",
                    text: (action === 'edit') ? "El cargo fue actualizado con éxito" : "El cargo fue creado con éxito",
                    icon: "success"
                }).then(() => {
                    // console.log('Reloading DataTable...');
                    if (typeof table !== 'undefined' && table.ajax && typeof table.ajax.reload === 'function') {
                        table.ajax.reload(function(json) {
                            // console.log('DataTable reloaded, new data:', json);
                        }, false);
                    } else {
                        // console.error('DataTable or its reload method is not available');
                        location.reload(); // Fallback to page reload if DataTable is not available
                    }
                });
            } else {
                // Swal.fire({
                //     title: "Error",
                //     text: "No se pudo procesar el estado",
                //     icon: "error"
                // });
            }
        });
    };

    if (action === 'edit') {
        // console.log('Fetching estado data for edit');
        fetch(`/asys/getCargo/${id}/`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(data => {
            // console.log('Estado data fetched:', data);
            initialData = data;
            processForm();
        })
        .catch(error => {
            // console.error('Error fetching estado:', error);
            Swal.fire('Error', 'No se pudo cargar el registro', 'error');
        });
    } else {
        processForm();
    }
  };
});