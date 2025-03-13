function message_error(obj) {
    var html = '';
    if (typeof (obj) === 'object') {
        html = '<ul style="text-align: left;">';
        $.each(obj, function (key, value) {
            html += '<li>' + key + ': ' + value + '</li>';
        });
        html += '</ul>';
    } else {
        html = '<p>' + obj + '</p>';
    }
    Swal.fire({
        title: 'Error!',
        html: html,
        icon: 'error'
    });
}

function submit_with_ajax(url, title, content, parameters, callback) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    $.ajax({
                        url: url, //window.location.pathname
                        type: 'POST',
                        data: parameters,
                        dataType: 'json',
                        processData: false,
                        contentType: false,
                    }).done(function (data) {
                        console.log(data);
                        if (!data.hasOwnProperty('error')) {
                            callback(data);
                            return false;
                        }
                        message_error(data.error);
                    }).fail(function (jqXHR, textStatus, errorThrown) {
                        alert(textStatus + ': ' + errorThrown);
                    }).always(function (data) {

                    });
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {

                }
            },
        }
    })
}

function alert_action(title, content, callback, cancel) {
    $.confirm({
        theme: 'material',
        title: title,
        icon: 'fa fa-info',
        content: content,
        columnClass: 'small',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {
                    callback();
                }
            },
            danger: {
                text: "No",
                btnClass: 'btn-red',
                action: function () {
                    cancel();
                }
            },
        }
    })
}



// Capturar clics en enlaces con la clase "ajax-link"
// document.addEventListener('click', function(e) {
//     if (e.target.classList.contains('ajax-link') || e.target.parentElement.classList.contains('ajax-link')) {
//         e.preventDefault();
//         const link = e.target.classList.contains('ajax-link') ? e.target : e.target.parentElement;
        
//         console.log("Haciendo clic en:", link.href);
        
//         fetch(link.href, {
//             method: 'GET',
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => {
//             console.log("Código de estado:", response.status);
//             console.log("Headers:", response.headers);
//             return response.text();
//         })
//         .then(text => {
//             console.log("Respuesta:", text);
//             try {
//                 // Intenta analizar como JSON
//                 const json = JSON.parse(text);
//                 console.log("JSON parseado:", json);
                
//                 // Si hay un error, muéstralo
//                 if (json.error) {
//                     alert("Error: " + json.error);
//                 }
//             } catch (e) {
//                 // Si no es JSON, es probablemente HTML
//                 console.log("No es JSON, probablemente HTML");
//                 document.getElementById('content').innerHTML = text;
//             }
//         })
//         .catch(error => {
//             console.error('Error en fetch:', error);
//             alert("Error al cargar: " + error);
//         });
//     }
// });

// Capturar envíos de formularios con la clase "ajax-form"
// document.addEventListener('submit', function(e) {
//     if (e.target.classList.contains('ajax-form')) {
//         e.preventDefault();
//         fetch(e.target.action, {
//             method: e.target.method,
//             body: new FormData(e.target),
//             headers: {
//                 'X-Requested-With': 'XMLHttpRequest'
//             }
//         })
//         .then(response => {
//             if (!response.ok) {
//                 handleAccessDenied(response);
//             }
//         })
//         .catch(error => console.error('Error:', error));
//     }
// });

