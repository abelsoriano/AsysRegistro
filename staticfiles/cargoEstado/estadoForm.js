
document.addEventListener("DOMContentLoaded", function () {
  // console.log("DOM fully loaded");

  const nuevoRegistroBtn = document.getElementById("nuevoRegistro");
  if (nuevoRegistroBtn) {
    nuevoRegistroBtn.addEventListener("click", function () {
      openSweetAlertForm("create");
    });
  } else {
    console.error("Nuevo registro button not found");
  }

  const editarRegistroBtns = document.querySelectorAll(".editarRegistro");
  // console.log("Edit buttons found:", editarRegistroBtns.length);
  editarRegistroBtns.forEach(function (button) {
    button.addEventListener("click", function () {
      const estadoId = this.getAttribute("data-id");
      // console.log("Editar registro clicked, ID:", estadoId);
      openSweetAlertForm("edit", estadoId);
    });
  });

  function openSweetAlertForm(action, estadoId = null) {
    // console.log("openSweetAlertForm called", action, estadoId);
    let title = action === "edit" ? "Editar Estado" : "Crear nuevo Estado";
    let url = action === "edit" ? `/asys/updateEstado/${estadoId}/` : createUrl;
    // console.log("Form URL:", url);

    showSweetAlertForm(action, url, "");
  }

  function showSweetAlertForm(action, url, inputNameValue) {
    // console.log("showSweetAlertForm called", action, url);
    Swal.fire({
      title: action === "edit" ? "Editar Estado" : "Crear nuevo Estado",
      html: `
                    <form id="estadoForm">
                        <input type="text" id="id_name" name="name" class="swal2-input" value="${inputNameValue}" required>
                    </form>
                `,
      showCancelButton: true,
      confirmButtonText: action === "edit" ? "Actualizar" : "Guardar",
      cancelButtonText: "Cancelar",
      preConfirm: () => {
        // console.log("preConfirm called");
        const name = Swal.getPopup().querySelector("#id_name").value;
        if (!name) {
          Swal.showValidationMessage("El nombre del estado es obligatorio");
          return;
        }

        const formData = new FormData();
        formData.append("name", name);
        formData.append("action", action);

        // console.log("Sending request to:", url);
        return fetch(url, {
          method: "POST",
          body: formData,
          headers: {
            "X-CSRFToken": csrfToken,
            "X-Requested-With": "XMLHttpRequest",
          },
        })
          .then((response) => {
            // console.log("Response received", response.status);
            if (!response.ok) {
              throw new Error("Error en el servidor");
            }
            return response.json();
          })
          .then((data) => {
            // console.log("Response data:", data);
            return data;
          })
          .catch((error) => {
            // console.error("Fetch error:", error);
            Swal.showValidationMessage(`Request failed: ${error}`);
          });
      },
    }).then((result) => {
      // console.log("Swal result:", result);
      if (result.isConfirmed) {
        if (result.value && result.value.success) {
          Swal.fire({
            title: "Estado guardado",
            text:
              action === "edit"
                ? "El estado fue actualizado con éxito"
                : "El estado fue creado con éxito",
            icon: "success",
          }).then(() => {
            window.location.reload(true);
          });
        } else {
          Swal.fire({
            title: "Error",
            text: "No se pudo guardar el estado",
            icon: "error",
          });
          // console.error("Error details:", result.value);
        }
      }
    });
  }
});
