$(function() {
    $('#data').DataTable({
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
        language: {
            "decimal": "",
            "emptyTable": "No hay datos disponibles en la tabla",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "infoEmpty": "Mostrando 0 a 0 de 0 entradas",
            "infoFiltered": "(filtradas de _MAX_ entradas totales)",
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
        columns: [
            {"data": "id"},
            {"data": "fecha"},
            {"data": "direccion"},
            {"data": "lectura"},
            {"data": "devocional"},
            {"data": "cultural_1.nombre"},
           {
                "data": "participantes",
                "render": function(data, type, row) {
                    return data.join(', ');  // Combina los nombres de los participantes en una cadena
                }
            },
            {
                "data": null,
                "render": function(data, type, row) {
                    var buttons = '<a href="/asys/service/edit/' + row.id + '/" class="pencil-icon"><i class="fas fa-pencil-alt"></i></a> ';
                    buttons += '<a href="/asys/service/delete/' + row.id + '/" class="delete-icon"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                },
                "className": "text-center",
                "orderable": false
            }
        ],
        initComplete: function(settings, json) {
            // Opcional: código para ejecutar cuando la tabla se ha inicializado completamente
        }
    });
});
