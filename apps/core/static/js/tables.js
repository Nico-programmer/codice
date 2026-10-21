/*
  Tablas con DataTables: buscador, orden por columna y paginación en el navegador.
  Uso en la plantilla:
    <table class="table table--stack" data-datatable>
      <th data-filter>Estado</th>   → agrega una lista para filtrar por los valores de esa columna
      <th data-no-sort>Acciones</th> → esa columna no se ordena ni se busca
      <td data-search="Al día" data-order="2026-11-18"> → valor para filtrar/buscar y para ordenar,
                                                          cuando el texto visible trae más cosas
  Sirve para listados de cientos de filas (empresas, sucursales, usuarios). Para miles (productos,
  facturas) hay que paginar desde el servidor.
*/
(function () {
  var ES = {
    search: "",
    searchPlaceholder: "Buscar…",
    lengthMenu: "_MENU_ por página",
    info: "Mostrando _START_ a _END_ de _TOTAL_",
    infoEmpty: "Sin resultados",
    infoFiltered: "(de _MAX_ en total)",
    zeroRecords: "No hay resultados para esa búsqueda",
    emptyTable: "No hay datos",
    paginate: { first: "«", previous: "‹", next: "›", last: "»" },
    aria: { orderable: "Ordenar por esta columna", orderableReverse: "Invertir el orden" }
  };

  function filtroPorColumna(tabla, indice, titulo, contenedor) {
    var valores = [];
    tabla.column(indice).nodes().each(function (celda) {
      var texto = (celda.getAttribute("data-search") || celda.textContent).trim();
      if (texto && valores.indexOf(texto) === -1) valores.push(texto);
    });
    valores.sort();
    var select = document.createElement("select");
    select.className = "select dt-filter";
    select.setAttribute("aria-label", "Filtrar por " + titulo.toLowerCase());
    select.innerHTML = '<option value="">' + titulo + ": todos</option>" +
      valores.map(function (v) { return '<option value="' + v.replace(/"/g, "&quot;") + '">' + v.replace(/</g, "&lt;") + "</option>"; }).join("");
    select.addEventListener("change", function () {
      var valor = select.value ? "^" + DataTable.util.escapeRegex(select.value) + "$" : "";
      tabla.column(indice).search(valor, true, false).draw();
    });
    contenedor.insertBefore(select, contenedor.firstChild);
  }

  document.addEventListener("DOMContentLoaded", function () {
    if (!window.DataTable) return;  // sin DataTables la tabla se ve igual, solo sin buscador ni páginas
    document.querySelectorAll("table[data-datatable]").forEach(function (el) {
      var sinOrden = [], conFiltro = [];
      el.querySelectorAll("thead th").forEach(function (th, i) {
        if (th.hasAttribute("data-no-sort")) sinOrden.push(i);
        if (th.hasAttribute("data-filter")) conFiltro.push([i, th.textContent.trim()]);
      });
      var tabla = new DataTable(el, {
        language: ES,
        order: [],
        pageLength: 10,
        lengthMenu: [10, 25, 50, 100],
        autoWidth: false,
        columnDefs: [{ targets: sinOrden, orderable: false, searchable: false }]
      });
      var busqueda = tabla.table().container().querySelector(".dt-search");
      conFiltro.forEach(function (f) { filtroPorColumna(tabla, f[0], f[1], busqueda); });
    });
  });
})();
