/* Codice · interacciones mínimas (sin dependencias). Abrir/cerrar paneles y ventanas, menú en tablet,
   selector de sucursal, mostrar contraseña y botones +/− de cantidad. */
(function () {
  document.addEventListener("click", function (e) {
    var el;
    if ((el = e.target.closest("[data-open]"))) { e.preventDefault(); var o = document.querySelector(el.dataset.open); if (o) o.classList.add("is-open"); return; }
    if ((el = e.target.closest("[data-close]"))) { e.preventDefault(); var ov = el.closest(".overlay"); if (ov) ov.classList.remove("is-open"); return; }
    if (e.target.classList.contains("overlay")) { e.target.classList.remove("is-open"); return; }
    if ((el = e.target.closest("[data-toggle-nav]"))) { e.preventDefault(); document.querySelector(".app").classList.toggle("nav-open"); return; }
    if ((el = e.target.closest("[data-toggle-password]"))) {
      var inp = el.parentNode.querySelector("input");
      var show = inp.type === "password"; inp.type = show ? "text" : "password";
      el.setAttribute("aria-label", show ? "Ocultar contraseña" : "Mostrar contraseña");
      el.querySelector("use").setAttribute("href", el.querySelector("use").getAttribute("href").replace(show ? "#eye" : "#eye-off", show ? "#eye-off" : "#eye"));
      return;
    }
    if ((el = e.target.closest("[data-qty]"))) {
      var q = el.parentNode.querySelector("input");
      q.value = Math.max(1, (parseInt(q.value, 10) || 1) + (el.dataset.qty === "+" ? 1 : -1));
      return;
    }
    var trigger = e.target.closest(".dropdown__trigger");
    document.querySelectorAll(".dropdown.is-open").forEach(function (d) { if (!trigger || d !== trigger.parentNode) d.classList.remove("is-open"); });
    if (trigger) trigger.parentNode.classList.toggle("is-open");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    document.querySelectorAll(".overlay.is-open, .dropdown.is-open").forEach(function (o) { o.classList.remove("is-open"); });
    var app = document.querySelector(".app"); if (app) app.classList.remove("nav-open");
  });
})();
