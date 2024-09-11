// Este bloque de codigo es para eliminar las notas
document.addEventListener('DOMContentLoaded', function () {
  let deleteButtons = document.querySelectorAll('.delete-link');
  let confirmDeleteButton = document.getElementById('confirm-delete');
  let currentNoteId;

  deleteButtons.forEach((button) => {
    button.addEventListener('click', function () {
      currentNoteId = this.getAttribute('data-id');
    });
  });

  confirmDeleteButton.addEventListener('click', function () {
    const getCSRFToken = () => {
      return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    };

    fetch(`/asys/notas/delete/${currentNoteId}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCSRFToken(),
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          document.querySelector(`.card[data-id="${currentNoteId}"]`).remove();
          let modalElement = document.getElementById('deleteModal');
          let modalInstance = bootstrap.Modal.getInstance(modalElement);
          modalInstance.hide();
        
          
        } else {
          console.error('Error al eliminar la nota');
        }
      })
      .catch((error) => console.error('Error:', error));
  });
});



// En este bloque esta la accion del boton ver mas y la organizacion de la lista de notas
document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('ver-mas').addEventListener('click', function (event) {
    event.preventDefault()

    let button = event.target
    let offset = parseInt(button.getAttribute('data-offset'))
    let url = button.getAttribute('data-url')

    const getCSRFToken = () => {
      return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
    }

    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken(),
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ offset: offset })
    })
      .then((response) => response.json())
      .then((data) => {
        let notas = JSON.parse(data)
        if (notas.length === 0) {
          button.textContent = 'No hay más notas'
          button.disabled = true
          return
        }

        let container = document.getElementById('nota-container')
        let newDeck = document.createElement('div')
        newDeck.className = 'card-deck'

        notas.forEach((nota) => {
          let card = document.createElement('div')
          card.className = 'card text-white bg-warning mb-3'
          card.innerHTML = `
                  <div class="card-header d-flex justify-content-between align-items-center">
                    <strong>${nota.fields.titulo.toUpperCase()}</strong>
                    <cite class="blockquote-footer text-muted">${nota.fields.fecha_creacion}</cite>
                  </div>
                  <div class="card-body">
                    <p>${nota.fields.contenido}</p>
                  </div>
                  <div class="card-footer d-flex justify-content-between">
                    <a class="btn btn-primary update-link" href="#">
                      <i class="fas fa-edit"></i> Editar
                    </a>
                    <button class="btn btn-danger delete-link" data-id="{{ nota.id }}" data-bs-toggle="modal" data-bs-target="#deleteModal"><i class="fas fa-trash-alt"></i> Eliminar</button>
                  </div>
                `
          newDeck.appendChild(card)
        })

        container.appendChild(newDeck)
        button.setAttribute('data-offset', offset + 3)
      })
      .catch((error) => console.error('Error:', error))
  })
})
