window.deleteServicio = function(id) {
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
            // Enviar la solicitud POST para eliminar
            fetch(`/asys/servicio/delete/${id}/`, {
                method: 'POST',
                headers: {
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

$(function () {
    var datatable = $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        processing: true,
        serverSide: false,
        language: {
            url: window.location.pathname,
        },
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: function (d) {
                d.action = 'searchdata';
                d.start_date = $('input[name="date_range"]').data('daterangepicker').startDate.format('YYYY-MM-DD');
                d.end_date = $('input[name="date_range"]').data('daterangepicker').endDate.format('YYYY-MM-DD');
                d.tipo = $('select[name="tipo_servicio"]').val();
                d.term = $('input[name="search"]').val();
            },
            dataSrc: ""
        },
        columns: [
            {"data": "fecha"},
            {"data": "tipo_servicio"},
            {"data": "direccion"},
            {"data": "director_cultural"},
            {"data": "participantes"},
            {
                "data": "ofrenda",
                render: function(data) {
                    return '$ ' + parseFloat(data).toFixed(2);
                }
            },
            {"data": "mensaje"},
            {
                "data": null,
                render: function(data, type, row) {
                    var buttons = '<a href="/asys/servicio/detail/' + row.id + '/" class="btn btn-info btn-xs mr-1"><i class="fas fa-eye"></i></a> ';
                    buttons += '<a href="/asys/servicio/update/' + row.id + '/" class="btn btn-warning btn-xs mr-1"><i class="fas fa-edit"></i></a> ';
                    buttons += '<a href="javascript:void(0);" onclick="deleteServicio(' + row.id + ')" class="btn btn-danger btn-xs"><i class="fas fa-trash"></i></a>';
                    return buttons;
                }
            }
        ],
        initComplete: function(settings, json) {
        }
    });

    $('input[name="date_range"]').daterangepicker({
        locale: {
            format: 'YYYY-MM-DD',
            applyLabel: 'Aplicar',
            cancelButtonText: 'Cancelar'
        }
    });

    $('select[name="tipo_servicio"], input[name="search"]').on('change keyup', function() {
        datatable.ajax.reload();
    });

    $('input[name="date_range"]').on('apply.daterangepicker', function(ev, picker) {
        datatable.ajax.reload();
    });
});