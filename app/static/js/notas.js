document.addEventListener('DOMContentLoaded', function () {
  const getCSRFToken = () => {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
  };

  const csrfToken = getCSRFToken();

  // Función para eliminar una nota
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

            // Enviar la solicitud POST para eliminar
            fetch(`/asys/notas/delete/${id}/`, {
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


  // Función para manejar la confirmación y eliminación
  document.addEventListener("DOMContentLoaded", function () {
    const csrfToken = getCSRFToken(); // Ahora usa la función para obtenerlo dinámicamente

    // Manejo del envío del formulario (Crear / Editar)
    document.getElementById("notaForm").addEventListener("submit", function (event) {
      event.preventDefault();
      const formData = new FormData(this);
      const actionUrl = this.getAttribute("action");

      fetch(actionUrl, {
          method: "POST",
          body: formData,
          headers: {
              "X-CSRFToken": csrfToken,
              "X-Requested-With": "XMLHttpRequest",
          },
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              Swal.fire("Éxito", "Nota guardada correctamente", "success").then(() => location.reload());
          } else {
              Swal.fire("Error", "No se pudo guardar la nota", "error");
          }
      })
      .catch(error => {
          console.error("Error:", error);
          Swal.fire("Error", "Ocurrió un error al guardar la nota", "error");
      });
  });
});



  // Agregar event listeners a los botones de eliminar
  function addDeleteListeners() {
    document.querySelectorAll('.delete-link').forEach(button => {
      button.addEventListener('click', async function(e) {
        e.preventDefault();
        const noteId = this.getAttribute('data-id');
        await deleteItem(noteId);
      });
    });
  }

  // Inicializar los event listeners de eliminación
  addDeleteListeners();

  // Manejo de "Ver más"
  const verMasButton = document.getElementById('ver-mas');
  
  if (verMasButton) {
    verMasButton.addEventListener('click', async function(event) {
      event.preventDefault();
      
      try {
        const button = event.target;
        const offset = parseInt(button.getAttribute('data-offset'));
        const url = button.getAttribute('data-url');

        const response = await fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify({ offset: offset })
        });

        const data = await response.json();
        const notas = JSON.parse(data);

        if (notas.length === 0) {
          button.textContent = 'No hay más notas';
          button.disabled = true;
          return;
        }

        const container = document.getElementById('nota-container');
        
        notas.forEach(nota => {
          const colDiv = document.createElement('div');
          colDiv.className = 'col-md-4 mb-4';
          
          colDiv.innerHTML = `
  <div class="card h-100 shadow-sm" data-id="${nota.pk}">
    <div class="card-header d-flex justify-content-between align-items-center">
      <strong>${nota.fields.titulo.toUpperCase()}</strong>
      <small class="text-muted">${nota.fields.fecha_creacion}</small>
    </div>
    <div class="card-body">
      <p class="card-text">${nota.fields.contenido}</p>
    </div>
    <div class="card-footer d-flex justify-content-between">
      <button class="btn btn-primary btn-sm edit-btn" data-id="${nota.pk}">
        <i class="fas fa-edit"></i> Editar
      </button>
      <button class="btn btn-danger btn-sm delete-link" data-id="${nota.pk}">
        <i class="fas fa-trash-alt"></i> Eliminar
      </button>
    </div>
  </div>
`;

          
          container.appendChild(colDiv);
        });

        button.setAttribute('data-offset', offset + 3);
        
        // Actualizar los event listeners para los nuevos botones
        addDeleteListeners();

      } catch (error) {
        console.error('Error:', error);
        await Swal.fire({
          title: 'Error',
          text: 'No se pudieron cargar más notas',
          icon: 'error'
        });
      }
    });
  }
});