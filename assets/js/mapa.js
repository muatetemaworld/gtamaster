/* GTA MASTER · mapa interactivo de MapGenie (código de inserción oficial).
   No se conecta con MapGenie hasta que el lector pulsa el botón (privacidad y velocidad). */
(function () {
  var gate = document.querySelector('.mapa__gate');
  if (!gate) return;
  var SRC = 'https://mapgenie.io/grand-theft-auto-6/maps/leonida?embed=light';
  function cargar() {
    if (gate.getAttribute('data-on')) return; gate.setAttribute('data-on', '1');
    var f = document.createElement('iframe');
    f.src = SRC; f.title = 'Mapa interactivo de GTA 6 (Leonida) de MapGenie';
    f.className = 'mapa__frame'; f.loading = 'eager';
    f.setAttribute('allow', 'fullscreen'); f.setAttribute('allowfullscreen', '');
    f.setAttribute('referrerpolicy', 'strict-origin-when-cross-origin');
    gate.parentNode.insertBefore(f, gate);
    gate.hidden = true;
  }
  gate.querySelector('.mapa__btn').addEventListener('click', cargar);
  if (/^#(cargar|mapa-interactivo)$/.test(location.hash)) cargar();
})();
