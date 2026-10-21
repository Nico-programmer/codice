/*
  Listas con buscador (Tom Select) para los <select data-searchable>.
  El filtro |styled se lo pone solo a los campos que eligen algo de la base de datos
  (empresa, encargado, sucursal...). Si Tom Select no carga, queda la lista normal.
*/
document.addEventListener("DOMContentLoaded", function () {
  if (!window.TomSelect) return;
  document.querySelectorAll("select[data-searchable]").forEach(function (el) {
    new TomSelect(el, {
      create: false,
      maxOptions: null,
      allowEmptyOption: !el.required,
      placeholder: "Escribe para buscar…",
      render: {
        no_results: function () { return '<div class="no-results">No hay resultados</div>'; }
      }
    });
  });
});
