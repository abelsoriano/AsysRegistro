$(function () {
    // Funcionalidad para imprimir
    $('#printDetail').on('click', function() {
        window.print();
    });
    
    // Animación suave al cargar la página
    $('.info-group').each(function(index) {
        $(this).css('opacity', 0);
        $(this).animate({
            opacity: 1
        }, 300 + (index * 100));
    });
    
    // Formato de moneda para la ofrenda
    var ofrendaElement = $('.ofrenda-value');
    var ofrendaValue = ofrendaElement.text();
    if (ofrendaValue) {
        ofrendaValue = ofrendaValue.replace('$', '');
        // Formatea la ofrenda como moneda
        var formattedValue = '$ ' + parseFloat(ofrendaValue).toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
        ofrendaElement.text(formattedValue);
    }
});