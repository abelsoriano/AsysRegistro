$(function () {
    var $detailsTable = $('#detailsTable').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        columns: [
            { "data": "id" },
            { "data": "miembro_nombre_completo" },
            { "data": "date" },
            {
                "data": "present",
                "render": function (data, type, row, meta) {
                    if (type === 'display') {
                        if (data) {
                           return '<span class="badge badge-success" style="background-color: green;">Presente</span>';
                        } else {
                            return '<span class="badge badge-danger" style="background-color: red;">Ausente</span>';
                        }
                    }
                    return data;  // Para otros tipos de renderización, como 'sort' o 'filter'
                }
            }
        ]
    });

    $('#data').DataTable({
        responsive: true,
        autoWidth: false,
    });

    // Código para manejar click en .show-details
    $('.show-details').on('click', function () {
        var date = $(this).data('date');
        var url = '/asys/details/?date=' + date;
        $.ajax({
            url: url,
            type: 'GET',
            success: function (data) {
                $detailsTable.clear().rows.add(data.details).draw();
                $('#detailsModal').modal('show');
            }
        });

    });

});

