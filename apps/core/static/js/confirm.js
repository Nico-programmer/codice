/*
  Confirmación antes de enviar un formulario, con SweetAlert2.
  Uso: <form ... data-confirm="¿Inactivar X?" data-confirm-text="Detalle" data-confirm-button="Sí, inactivar">
  Si SweetAlert no carga, usa la confirmación del navegador.
*/
document.addEventListener("submit", function (e) {
  var form = e.target;
  if (!form.dataset.confirm || form.dataset.confirmed === "true") return;
  e.preventDefault();
  var enviar = function () { form.dataset.confirmed = "true"; form.requestSubmit ? form.requestSubmit() : form.submit(); };
  if (!window.Swal) {
    if (window.confirm(form.dataset.confirm)) enviar();
    return;
  }
  Swal.fire({
    icon: "warning",
    title: form.dataset.confirm,
    text: form.dataset.confirmText || "",
    showCancelButton: true,
    confirmButtonText: form.dataset.confirmButton || "Sí, continuar",
    cancelButtonText: "Cancelar",
    reverseButtons: true,
    buttonsStyling: false,
    customClass: { popup: "swal-codice", confirmButton: "btn btn--danger-solid btn--lg", cancelButton: "btn btn--neutral btn--lg" }
  }).then(function (r) { if (r.isConfirmed) enviar(); });
});
