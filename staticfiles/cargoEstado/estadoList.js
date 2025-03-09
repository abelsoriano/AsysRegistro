    $(function () {
        var table = $('#data').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: function(d) {
                    d.action = 'searchdata';
                    return d;
                },
                dataSrc: function(json) {
                    return json;
                }
            },
            columns: [
                {"data": "id"},
                {"data": "name"},
                {"data": "desc"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a href="javascript:void(0);" class="btn btn-warning btn-xs btn-flat" onclick="openSweetAlertForm(\'edit\', ' + row.id + ')"><i class="fas fa-edit"></i></a> ' +
                            '<a href="javascript:void(0);" class="btn btn-danger btn-xs btn-flat" onclick="deleteItem(' + row.id + ')"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
            ],
            initComplete: function(settings, json) {
            }
        });

        $('#nuevoRegistro').on('click', function() {
            openSweetAlertForm('create');
        });

        window.openSweetAlertForm = function(action, id = null) {
            let title = (action === 'edit') ? "Editar Estado" : "Crear nuevo Estado";
            let url = (action === 'edit') ? `/asys/updateEstado/${id}/` : createUrl;
            let initialData = {};
        
            const processForm = () => {
                Swal.fire({
                    title: title,
                    html: `
                        <form id="estadoForm">
                            <input type="text" id="id_name" name="name" class="swal2-input" value="${initialData.name || ''}" placeholder="Nombre del estado" required>
                        </form>
                    `,
                    showCancelButton: true,
                    confirmButtonText: (action === 'edit') ? 'Actualizar' : 'Guardar',
                    cancelButtonText: 'Cancelar',
                    preConfirm: () => {
                        const name = Swal.getPopup().querySelector('#id_name').value;
                        if (!name) {
                            Swal.showValidationMessage('El nombre del estado es obligatorio');
                            return false;
                        }
        
                        const formData = new FormData();
                        formData.append('name', name);
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
                            text: (action === 'edit') ? "El estado fue actualizado con éxito" : "El estado fue creado con éxito",
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
                fetch(`/asys/getEstado/${id}/`, {
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

        window.deleteItem = function(id) {
            Swal.fire({
                title: '¿Estás seguro?',
                text: "Esta acción no se puede deshacer",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, eliminar',
                cancelButtonText: 'Cancelar'
            }).then((result) => {
                if (result.value) {
                    // console.log('Attempting to delete item with ID:', id);
        
                    // Enviar la solicitud POST para eliminar
                    fetch(`/asys/deleteEstado/${id}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': csrfToken,
                            'X-Requested-With': 'XMLHttpRequest',
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            action: 'delete'
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            Swal.fire(
                                'Eliminado!',
                                'El registro ha sido eliminado.',
                                'success'
                            ).then(() => {
                                location.reload(); // Recargar la página o DataTable
                            });
                        } else {
                            Swal.fire(
                                'Error!',
                                'Ocurrió un error al eliminar el registro: ' + (data.error || 'Error desconocido'),
                                'error'
                            );
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        Swal.fire(
                            'Error!',
                            'Ocurrió un error al eliminar el registro.',
                            'error'
                        );
                    });
                } 
            });
        };       
        
        
    });

    