/* GTA MASTER · comentarios con Disqus.
   No se carga nada de Disqus hasta que el lector pulsa el botón (privacidad y velocidad).
   Si llega desde un enlace a un comentario (#comment-…), se abre solo. */
(function () {
  var gate = document.querySelector('.comments__gate');
  if (!gate) return;
  var cargado = false;
  function cargar() {
    if (cargado) return; cargado = true;
    var short = gate.getAttribute('data-disqus');
    if (!/^[a-z0-9-]+$/.test(short)) return;
    var url = gate.getAttribute('data-url'), id = gate.getAttribute('data-id'), title = gate.getAttribute('data-title');
    window.disqus_config = function () {
      this.page.url = url; this.page.identifier = id; this.page.title = title; this.language = 'es_ES';
    };
    var s = document.createElement('script');
    s.src = 'https://' + short + '.disqus.com/embed.js';
    s.setAttribute('data-timestamp', String(+new Date()));
    s.async = true;
    document.body.appendChild(s);
    gate.classList.add('is-loading');
    gate.querySelector('.comments__btn span').textContent = 'Cargando comentarios…';
    setTimeout(function () { gate.hidden = true; }, 1200);
  }
  gate.querySelector('.comments__btn').addEventListener('click', cargar);
  if (/^#(comment-|comentarios|disqus)/.test(location.hash)) cargar();
})();
