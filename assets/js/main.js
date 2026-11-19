/* Seguridad: la web no se puede mostrar dentro de un marco ajeno (clickjacking).
   GitHub Pages no permite la cabecera X-Frame-Options, así que se hace aquí. */
(function () {
  /* Respaldo: si alguien entra por http, pasa a https (GitHub ya lo fuerza al activar «Enforce HTTPS»). */
  if (location.protocol === 'http:' && /(^|\.)gtamaster\.es$/.test(location.hostname)) { location.replace('https://' + location.host + location.pathname + location.search + location.hash); return; }
  if (window.top !== window.self) {
    try { window.top.location.replace(window.self.location.href); }
    catch (e) { document.documentElement.style.display = 'none'; }
  }
})();
/* GTA MASTER · interacciones y scroll */
(function () {
  var d = document, w = window, root = d.documentElement;
  root.classList.remove('no-js');
  var RM = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (RM) root.classList.add('rm');

  /* Enlaces limpios (/videos/slug/) también en vistas previas sin servidor */
  if (location.protocol === 'file:' || /claude|artifact|usercontent/.test(location.hostname)) {
    d.querySelectorAll('a[href$="/"]').forEach(function (a) {
      var h = a.getAttribute('href');
      if (!/^(https?:|mailto:|#)/.test(h)) a.setAttribute('href', h + 'index.html');
    });
  }

  /* Barra de progreso y nav */
  var bar = d.querySelector('.progress'), nav = d.querySelector('.nav');
  function onScroll() {
    var h = root.scrollHeight - innerHeight, p = h > 0 ? scrollY / h : 0;
    if (bar) bar.style.transform = 'scaleX(' + p + ')';
    if (nav) nav.classList.toggle('is-solid', scrollY > 40);
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* Vídeos: cada clic abre el vídeo en YouTube (pestaña nueva, reproducción automática).
     Así la visualización cuenta en el canal y no depende del reproductor incrustado. */
  d.querySelectorAll('[data-yt-out]').forEach(function (a) {
    a.addEventListener('click', function () {
      try { if (w.gtag) w.gtag('event', 'ver_en_youtube', { video_url: a.href }); } catch (e) {}
    });
  });

  /* Filtro de vídeos por tema */
  var chips = d.querySelectorAll('.chip[data-filter]');
  chips.forEach(function (c) {
    c.addEventListener('click', function () {
      var f = c.getAttribute('data-filter');
      chips.forEach(function (x) { var on = x === c; x.classList.toggle('is-on', on); x.setAttribute('aria-pressed', on); });
      d.querySelectorAll('.vgrid .vcard').forEach(function (v) { v.hidden = !(f === 'Todos' || v.getAttribute('data-cat') === f); });
      if (w.ScrollTrigger) w.ScrollTrigger.refresh();
    });
  });

  /* Cuenta atrás al lanzamiento (19 nov 2026, 00:00 hora peninsular) */
  var cd = d.querySelector('[data-countdown]');
  if (cd) {
    var target = Date.parse(cd.getAttribute('data-countdown'));
    var tick = function () {
      var s = Math.max(0, Math.floor((target - Date.now()) / 1000));
      if (s === 0) { cd.innerHTML = '<div style="min-width:auto;padding:1rem 2rem"><b>YA A LA VENTA</b><span>PS5 · Xbox Series X|S</span></div>'; return; }
      var u = { d: Math.floor(s / 86400), h: Math.floor(s % 86400 / 3600), m: Math.floor(s % 3600 / 60), s: s % 60 };
      for (var k in u) { var el = cd.querySelector('[data-u="' + k + '"]'); if (el) el.textContent = String(u[k]).padStart(2, '0'); }
      setTimeout(tick, 1000);
    };
    tick();
  }

  /* Año del pie */
  d.querySelectorAll('[data-year]').forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* Sin GSAP o con movimiento reducido: mostrar todo */
  function plainReveal() {
    var els = d.querySelectorAll('.reveal');
    if (!('IntersectionObserver' in w) || RM) { els.forEach(function (e) { e.style.opacity = 1; e.style.transform = 'none'; }); return; }
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) { if (x.isIntersecting) { x.target.style.transition = 'opacity .9s cubic-bezier(.22,1,.36,1), transform .9s cubic-bezier(.22,1,.36,1)'; x.target.style.opacity = 1; x.target.style.transform = 'none'; io.unobserve(x.target); } });
    }, { rootMargin: '0px 0px -10% 0px' });
    els.forEach(function (e) { io.observe(e); });
  }

  function init() {
    if (RM || !w.gsap || !w.ScrollTrigger) { plainReveal(); return; }
    var gsap = w.gsap; gsap.registerPlugin(w.ScrollTrigger);

    /* HERO: del atardecer a la noche en Vice City */
    var hero = d.querySelector('.hero');
    if (hero) {
      gsap.set('#bg-day', { scale: 1.12 });
      gsap.set('#bg-night', { scale: 1.18 });
      var tl = gsap.timeline({ scrollTrigger: { trigger: hero, start: 'top top', end: '+=160%', scrub: 1, pin: true, anticipatePin: 1 } });
      tl.to('#bg-day', { scale: 1, yPercent: 4, ease: 'none' }, 0)
        .to('#bg-night', { opacity: 1, scale: 1.04, ease: 'none' }, .25)
        .to('#night-tint', { opacity: 1, ease: 'none' }, .3)
        .to('.hero__copy', { yPercent: -18, opacity: 0, ease: 'power1.in' }, 0)
        .to('.hero__scroll', { opacity: 0 }, 0)
        .fromTo('.hero__night', { opacity: 0, scale: .92 }, { opacity: 1, scale: 1, ease: 'power2.out' }, .5)
        .fromTo('.hero__night .big span', { yPercent: 40 }, { yPercent: 0, stagger: .06, ease: 'power3.out' }, .5);
    }

    /* Parallax suave en los fondos */
    gsap.utils.toArray('.bgpar__img, .hero-card__img, .banner__img').forEach(function (img) {
      var box = img.parentElement;
      gsap.fromTo(img, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: box, start: 'top bottom', end: 'bottom top', scrub: true } });
    });

    /* Tarjetas de vídeo en cascada */
    w.ScrollTrigger.batch('.vcard', { start: 'top 90%', once: true,
      onEnter: function (els) { gsap.fromTo(els, { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: .9, ease: 'expo.out', stagger: .08 }); } });

    /* Revelados al entrar */
    gsap.utils.toArray('.reveal').forEach(function (el) {
      gsap.to(el, { opacity: 1, y: 0, duration: 1, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 88%' } });
    });

    /* Contadores */
    gsap.utils.toArray('[data-count]').forEach(function (el) {
      var n = { v: 0 }, end = +el.getAttribute('data-count');
      gsap.to(n, { v: end, duration: 1.6, ease: 'power2.out', scrollTrigger: { trigger: el, start: 'top 90%' }, onUpdate: function () { el.textContent = Math.round(n.v); } });
    });

    /* Nombres gigantes de personajes */
    gsap.utils.toArray('.char').forEach(function (c, i) {
      var name = c.querySelector('.char__name'), img = c.querySelector('.char__media a');
      if (name) gsap.fromTo(name, { xPercent: i % 2 ? -12 : 12 }, { xPercent: i % 2 ? 6 : -6, ease: 'none', scrollTrigger: { trigger: c, start: 'top bottom', end: 'bottom top', scrub: true } });
      if (img) gsap.fromTo(img, { clipPath: 'inset(12% 12% 12% 12% round 18px)' }, { clipPath: 'inset(0% 0% 0% 0% round 18px)', ease: 'none', scrollTrigger: { trigger: c, start: 'top 85%', end: 'top 35%', scrub: true } });
    });

    addEventListener('load', function () { w.ScrollTrigger.refresh(); });
  }


  /* Slider de radios */
  function radiosSlider() {
    var t = d.getElementById('radios-track'); if (!t) return;
    var btns = d.querySelectorAll('.radios__btn');
    function step() { var c = t.querySelector('.radio'); return c ? c.getBoundingClientRect().width + parseFloat(getComputedStyle(t).columnGap || 16) : 300; }
    function upd() { var max = t.scrollWidth - t.clientWidth - 2; btns[0].disabled = t.scrollLeft <= 2; btns[1].disabled = t.scrollLeft >= max; }
    btns.forEach(function (b) { b.addEventListener('click', function () { t.scrollBy({ left: step() * +b.getAttribute('data-dir'), behavior: 'smooth' }); }); });
    t.addEventListener('keydown', function (e) { if (e.key === 'ArrowRight' || e.key === 'ArrowLeft') { e.preventDefault(); t.scrollBy({ left: step() * (e.key === 'ArrowRight' ? 1 : -1), behavior: 'smooth' }); } });
    t.addEventListener('scroll', upd, { passive: true }); addEventListener('resize', upd); upd();
  }

  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', radiosSlider); else radiosSlider();
  if (d.readyState === 'loading') d.addEventListener('DOMContentLoaded', init); else init();
})();
