$(function() {
    const detalleEmpleado = $('#detalle');
    const dataTable = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdata'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "name"}, 
            {"data": "lastname"},
            {"data": "dni"},
            {"data": "state.name",
            render: function(data, type, row) {
                if (data === 'Activo') {
                    return `<span class="badge bg-success">${data}</span>`;
                }else if (data ==='Disciplina'){
                    return `<span class="badge bg-danger">${data}</span>`;
                }else{
                    return `<span class="badge" style="background-color:rgb(241, 169, 79); color: white;">${data}</span>`;

                }
                
            }
        }, 
        {"data": "cargo.nombre"},
        {"data": "phone"}, 
        {"data": "opcion"}
        ],
        
        columnDefs: [{
            targets: [-2],
            class: 'text-center',
            orderable: false, 
        }, {
            targets: [-1],
            class: 'text-center',
            orderable: false,
            render: function(data, type, row) {
                var buttons = '<a href="/asys/persona/edit/' + row.id + '/" class="btn btn-sm btn-primary me-2"><i class="fas fa-pencil-alt"></i></a> ';     
                buttons += '<a href="/asys/persona/delete/' + row.id + '/" class="btn btn-sm btn-danger delete-btn"><i class="fas fa-trash-alt"></i></a>';   
                return buttons;
                    
            } 
        }],
		initComplete: function(settings, json) {
            // Añadir clase para estilos personalizados
            $('#data').addClass('table-hover');
        }
    });

    // Manejo de clic en fila para mostrar detalles
    $('#data tbody').on('click', 'tr', function(e) {
        // Evitar que se abra el modal si se hizo clic en los botones
        if ($(e.target).closest('.btn-group').length) {
            return;
        }

        const data = dataTable.row(this).data();
        showEmployeeDetails(data);
    });

    // Función para mostrar detalles del empleado
    function showEmployeeDetails(data) {
        detalleEmpleado.find('#perfil').attr('src', data.image);
        detalleEmpleado.find('#nombre-empleado').text(`${data.name} ${data.lastname}`);
        detalleEmpleado.find('#dni-empleado').text(`Cedula: ${data.dni}`);
        detalleEmpleado.find('#nacimiento-empleado').text(`Fecha de Nacimiento: ${data.date_joined}`);
        detalleEmpleado.find('#genero-mpleado').text(`Genero: ${data.gender}`);
        detalleEmpleado.find('#telefono-empleado').text(`Teléfono: ${data.phone}`);
        detalleEmpleado.find('#direccion-empleado').text(`Dirección: ${data.address}`);
        detalleEmpleado.find('#ingreso-empleado').text(`Fecha de Ingreso: ${data.fecha_ingreso}`);
        detalleEmpleado.find('#correo-empleado').text(`Correo: ${data.email}`);
        detalleEmpleado.find('#estado-empleado').text(`Estado: ${data.state.name}`);
        detalleEmpleado.find('#cargo-empleado').text(`Cargo: ${data.cargo.name}`);
        detalleEmpleado.find('#category-empleado').text(`Categoria: ${data.category}`);

        detalleEmpleado.fadeIn(300);
    }

    // Manejar el cierre del modal de detalles
    $(document).on('keydown', function(event) {
        if (event.key === 'Escape') {
            detalleEmpleado.fadeOut(300);
        }
    });

    detalleEmpleado.on('click', '.close-button', function() {
        detalleEmpleado.fadeOut(300);
    });

   
    
});