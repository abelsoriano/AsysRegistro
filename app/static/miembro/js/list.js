$(function() {
	$('#data').DataTable({
		responsive: true,
//		pageLength: 8,
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
		language: {
			"decimal": "",
			"emptyTable": "No hay datos disponibles en la tabla",
			"info": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
			"infoEmpty": "Mostrando 0 a 0 de 0 entradas",
			"infoFiltered": "(filtradas de _MAX_ entradas totales)",
			"infoPostFix": "",
			"thousands": ",",
			"lengthMenu": "Mostrar _MENU_ entradas",
			"loadingRecords": "Cargando...",
			"processing": "Procesando...",
			"search": "Buscar:",
			"zeroRecords": "No se encontraron registros coincidentes",
			"paginate": {
				"first": "Primero",
				"last": "Último",
				"next": "Siguiente",
				"previous": "Anterior"
			},
			"aria": {
				"sortAscending": ": activar para ordenar de manera ascendente",
				"sortDescending": ": activar para ordenar de manera descendente"
			}
		},
		columns: [{
			"data": "id"
		}, {
			"data": "name"
		}, {
			"data": "lastname"
		}, {
			"data": "dni"
		}, {
			"data": "state.name"
		}, {
			"data": "cargo.name"
		}, {
			"data": "phone"
		}, {
			"data": "opcion"
		}],
		columnDefs: [{
			targets: [-2],
			class: 'text-center',
			orderable: false,
		}, {
			targets: [-1],
			class: 'text-center',
			orderable: false,
			render: function(data, type, row) {
			var buttons = '<a href="/asys/persona/edit/' + row.id + '/" class="pencil-icon"><i class="fas fa-pencil-alt"></i></a> ';
             buttons += '<a href="/asys/persona/delete/' + row.id + '/" class="delete-icon"><i class="fas fa-trash-alt"></i></a>';
				return buttons;
			}
		}, ],
		initComplete: function(settings, json) {

		}
	});
});



$(function() {
    const detalleEmpleado = $('#detalle');

    $(document).on('keydown', function(event) {
        if (event.key === 'Escape') {
            detalleEmpleado.hide();
        }
    });

    $('#data tbody').on('click', 'tr', function() {
        const table = $('#data').DataTable();
        const data = table.row(this).data();
        const name = data.name;
        const lastname = data.lastname;
        const dni = data.dni;
        const state = data.state.name;
        const phone = data.phone;
        const email = data.email;
        const address = data.address;
        const image = data.image;

        detalleEmpleado.find('#perfil').attr('src', image);
        detalleEmpleado.find('#nombre-empleado').text(`${name} ${lastname}`);
        detalleEmpleado.find('#dni-empleado').text(`Cedula: ${dni}`);
        detalleEmpleado.find('#nacimiento-empleado').text(`Fecha de Nacimiento: ${data.date_joined}`);
        detalleEmpleado.find('#genero-mpleado').text(`Genero: ${data.gender}`);
        detalleEmpleado.find('#telefono-empleado').text(`Teléfono: ${phone}`);
        detalleEmpleado.find('#direccion-empleado').text(`Dirección: ${address}`);
        detalleEmpleado.find('#ingreso-empleado').text(`Fecha de Ingreso: ${data.fecha_ingreso}`);
        detalleEmpleado.find('#correo-empleado').text(`Correo: ${email}`);
        detalleEmpleado.find('#estado-empleado').text(`Estado: ${state}`);
        detalleEmpleado.find('#cargo-empleado').text(`Cargo: ${data.cargo.name}`);

        detalleEmpleado.show();
    });

    detalleEmpleado.on('click', '.close-button', function() {
        detalleEmpleado.hide();
    });
});