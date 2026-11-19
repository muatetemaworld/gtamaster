#!/usr/bin/env python3
"""Genera la web estática de GTA MASTER (home, páginas de vídeo, sitemap, robots, llms.txt).
Cambia SITE por tu dominio definitivo y vuelve a ejecutar: python3 build.py
"""
import unicodedata, json, os, random, html, re
from datetime import datetime
from zoneinfo import ZoneInfo

SITE = "https://gtamaster.es"          # <-- dominio definitivo
CHANNEL = "https://www.youtube.com/@GtaMaster2027"
CHANNEL_ID = "UCqBGUFmTDtnCzhu-uYCf7SA"
SUB = CHANNEL + "?sub_confirmation=1"
BRAND = "GTA MASTER"
LAUNCH = "2026-11-19T00:00:00+01:00"
OUT = os.path.dirname(os.path.abspath(__file__))
MAD = ZoneInfo("Europe/Madrid")
MESES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]

V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "videos.json"), encoding="utf-8"))
EXCLUIDOS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "excluidos.json"), encoding="utf-8")) if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "excluidos.json")) else []
_EXC_IDS = {e["id"] for e in EXCLUIDOS}
V = [x for x in V if x["id"] not in _EXC_IDS]
V.sort(key=lambda v: v["up"], reverse=True)
BY = {v["id"]: v for v in V}
import hashlib
def _h(p): return hashlib.md5(open(os.path.join(OUT, p), "rb").read()).hexdigest()[:8]
ASSET_V = {"css": _h("assets/css/main.css"), "js": _h("assets/js/main.js"), "com": _h("assets/js/comentarios.js")}  # rompe la caché al cambiar

def cap(s): return s[:1].upper()+s[1:]
def esc(s): return html.escape(s, quote=True)
def iso_dur(s): return f"PT{s//60}M{s%60}S" if s else None
def mmss(s): return f"{s//60}:{s%60:02d}" if s else ""
def fecha(v):
    dt = datetime.fromisoformat(v["up"]).astimezone(MAD)
    return f"{dt.day} {MESES[dt.month-1]} {dt.year}"
def vurl(v): return f"{SITE}/videos/{v['slug']}/"

FAQ_EXTRA = [
 ("¿Quién presenta la radio latina de GTA 6?", "Cocoteo FM, la emisora de música latina contemporánea, la presentan Bad Bunny y RaiNao, en los papeles de El Martillo y La Gata."),
 ("¿Qué es GTA MASTER?", "Un canal de YouTube en español dedicado a GTA 6: detalles que no viste, personajes, mapa, curiosidades y análisis hechos con material oficial de Rockstar, sin filtraciones. Es un canal de fans, no oficial."),
]

REGIONS = [
 ("Vice City", "La gran ciudad de Leonida, inspirada en Miami: playa, neón y vida nocturna.", "sDK3RR6bInQ", "Vice City de día vs de noche"),
 ("Leonida Keys", "Los Cayos: islas, embarcaderos y personajes como Cal Hampton.", "INVN9F4vSH8", "Quién es Cal Hampton"),
 ("Grassrivers", "Los pantanos inspirados en los Everglades, con caimanes e hidrodeslizador.", "_rBw7Wa-IVs", "Los pantanos de GTA 6"),
 ("Port Gellhorn", "La zona portuaria de Leonida.", "n8qxCiLWi28", "Las 6 regiones"),
 ("Ambrosia", "El interior de Leonida, más tranquilo que la ciudad.", "n8qxCiLWi28", "Las 6 regiones"),
 ("Mount Kalaga", "El parque nacional: montaña, bosque y naturaleza.", "WeX9Ga2vuOI", "Todo lo que podrás hacer"),
]

CAST = [
    {"n": "Jason Duval", "big": "Jason", "slug": "jason-duval", "rol": "Protagonista", "v": "BdIQoWrnTQc", "bg": "boulevard-art-deco",
     "t": "Protagonista. Exmilitar que acaba de nuevo en el mundo del crimen, trabajando para traficantes en los Cayos de Leonida.",
     "bio": "Creció rodeado de estafadores y delincuentes, pasó por el ejército y, al volver, acabó haciendo trabajos para los traficantes de los Cayos. Allí conoce a Lucia, y su relación es el eje de la historia."},
    {"n": "Lucia Caminos", "big": "Lucia", "slug": "lucia-caminos", "rol": "Protagonista", "v": "q9amoxM3teA", "bg": "bahia-urbana",
     "t": "Protagonista. Dispuesta a cambiar de vida después de pasar por la Penitenciaría de Leonida.",
     "bio": "Su padre le enseñó a pelear. Tras su paso por la Penitenciaría de Leonida decidió tomar solo decisiones inteligentes y busca la vida cómoda con la que soñaba su madre en Liberty City."},
    {"n": "Raul Bautista", "big": "Raul", "slug": "raul-bautista", "rol": "Secundario", "v": None, "bg": "costa-urbana-pastel", "lema": "Atracador de bancos",
     "t": "Atracador de bancos veterano que siempre busca un golpe mayor.",
     "bio": "Confía en la experiencia, el carisma y la astucia. Busca socios con talento dispuestos a asumir trabajos de mucho riesgo a cambio de un gran botín."},
    {"n": "Brian Heder", "big": "Brian", "slug": "brian-heder", "rol": "Secundario", "v": "oKhgAiukzrw", "bg": "everglades-aerodeslizador", "lema": "Contrabandista retirado",
     "t": "Contrabandista de la vieja escuela de los Cayos que todavía conserva sus contactos.",
     "bio": "Parece un jubilado de playa, pero sigue moviendo mercancía desde su astillero junto a su tercera esposa, Lori, y deja que otros hagan el trabajo sucio. Jason vive en una de sus propiedades y trabaja para él."},
    {"n": "Boobie Ike", "big": "Boobie", "slug": "boobie-ike", "rol": "Secundario", "v": "j3dwEDoxv4k", "bg": "club-art-deco",
     "t": "Leyenda local de Vice City: de la calle a empresario de éxito.",
     "bio": "Convirtió su pasado en la calle en un imperio de negocios legales: inmobiliarias, un club de striptease y el estudio de grabación del sello Only Raw Records."},
    {"n": "Cal Hampton", "big": "Cal", "slug": "cal-hampton", "rol": "Secundario", "v": "INVN9F4vSH8", "bg": "lancha-tropical",
     "t": "Amigo de Jason y socio de Brian. Un teórico de la conspiración que desconfía de todo.",
     "bio": "Prefiere quedarse en casa espiando las comunicaciones de la Guardia Costera. Se conforma con la vida tranquila mientras Jason sueña con algo más grande."},
    {"n": "Dre'Quan Priest", "big": "Dre'Quan", "slug": "drequan-priest", "rol": "Secundario", "v": None, "bg": "horizonte-neon-noche", "lema": "Buscavidas del rap",
     "t": "Más buscavidas que gánster: quiere triunfar en la música.",
     "bio": "Vendía en la calle para salir adelante mientras perseguía su carrera musical. Ahora está ligado al sello Only Raw Records, donde ha fichado a Real Dimez."},
    {"n": "Real Dimez", "big": "Dimez", "slug": "real-dimez", "rol": "Secundario", "v": None, "bg": "atardecer-neon-mar", "lema": "Bae-Luxe y Roxy",
     "t": "Bae-Luxe y Roxy: de sus comienzos en la calle al éxito en las redes.",
     "bio": "Amigas desde el instituto, se hicieron un nombre con temas provocadores y mucha promoción en redes. Su primer éxito llegó con el rapero DWNPLY y ahora han fichado por Only Raw Records."},
    {"n": "Andrés de León", "big": "Andrés", "slug": "andres-de-leon", "rol": "Secundario", "v": None, "bg": "estadio-tropical", "lema": "VIP de Megamundo",
     "t": "Un VIP de Megamundo que necesita algo más que protección.",
     "bio": "Socio adinerado de Megamundo. Jason y Lucia son contratados, a través de Valentina, como su escolta en la inauguración de la primera sede de Megamundo en Estados Unidos, donde acaba tomado como rehén."},
    {"n": "Petra Navarro", "big": "Petra", "slug": "petra-navarro", "rol": "Secundario", "v": None, "bg": "bahia-urbana", "lema": "Directora de Megamundo",
     "t": "Directora de operaciones de Megamundo, figura clave del mundo empresarial de Vice City.",
     "bio": "Es la COO de Megamundo. Conoce a Jason y a Lucia a través de Valentina durante la inauguración del edificio de la compañía."},
]
CAST_SOURCES = [("Rockstar Games: personajes de GTA VI", "https://www.rockstargames.com/VI"),
                ("GTABase: guía de personajes de GTA 6", "https://www.gtabase.com/es/gta-6/personajes/"),
                ("PC Gamer: GTA 6 characters", "https://www.pcgamer.com/games/action/grand-theft-auto/gta6-characters"),
                ("Stevivor: GTA 6 characters", "https://stevivor.com/guides/gta-6-characters/")]

# Clave pública de IndexNow (Bing, Yandex…): el archivo <clave>.txt está en la raíz.
INDEXNOW = "8ca4c57fdd33e60aabbfda8bf2fbff7a"

# ---------- seguridad ----------
# GitHub Pages no deja enviar cabeceras HTTP, así que la política de seguridad
# va en una etiqueta <meta>. Solo se ejecutan scripts de la propia web (nada en
# línea ni de terceros) y solo se incrustan reproductores de YouTube.
CSP = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
       "font-src 'self'; connect-src 'self'; media-src 'self'; "
       "frame-src https://www.youtube-nocookie.com https://www.youtube.com; "
       "object-src 'none'; base-uri 'self'; form-action 'none'; upgrade-insecure-requests")

# Comentarios con Disqus (solo en las noticias del blog y solo si el lector los abre).
DISQUS = "gtamaster-es"
CSP_COMENTARIOS = ("default-src 'self'; script-src 'self' https://*.disqus.com https://*.disquscdn.com; "
       "style-src 'self' 'unsafe-inline' https://*.disquscdn.com; img-src 'self' data: https://*.disqus.com https://*.disquscdn.com; "
       "font-src 'self' https://*.disquscdn.com; connect-src 'self' https://*.disqus.com; media-src 'self'; "
       "frame-src https://www.youtube-nocookie.com https://www.youtube.com https://disqus.com https://*.disqus.com; "
       "object-src 'none'; base-uri 'self'; form-action 'none'; upgrade-insecure-requests")

def comentarios(p, canon, rel):
    if not DISQUS: return ""
    return f'''<section class="comments" id="comentarios" aria-labelledby="t-com">
  <div class="comments__head"><span class="eyebrow px">Comunidad</span><h2 id="t-com">Comentarios</h2></div>
  <ul class="comments__rules">
    <li><b>Sin spoilers sin avisar.</b> Si cuentas algo de la historia, avísalo al principio o usa la etiqueta de spoiler.</li>
    <li><b>Respeto.</b> Nada de insultos, odio ni acoso. Se debate el juego, no a las personas.</li>
    <li><b>Sin enlaces a filtraciones, piratería ni estafas.</b> Los mensajes con enlaces sospechosos se borran.</li>
  </ul>
  <div class="comments__gate" data-disqus="{DISQUS}" data-url="{canon}" data-id="blog-{p["slug"]}" data-title="{esc(p["title"])}">
    <button type="button" class="pill comments__btn"><span>Ver y escribir comentarios</span>{ARROW}</button>
    <p class="comments__note">Los comentarios funcionan con Disqus: puedes entrar con Google, Facebook, X o tu email. Al pulsar el botón se conecta con Disqus, que usa sus propias cookies. Más información en nuestra <a href="{rel}privacidad/">política de privacidad</a>.</p>
  </div>
  <div id="disqus_thread"></div>
</section>'''

def ld_json(obj):
    """JSON-LD seguro dentro de <script>: un texto con «</script>» no puede cerrar la etiqueta."""
    return (json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))

# ---------- piezas comunes ----------
YT_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5 3l16 9-16 9z"/></svg>'

def head(title, desc, canon, img, rel, schema, extra="", csp=None):
    return f'''<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="{csp or CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="es" href="{canon}">
<link rel="alternate" hreflang="x-default" href="{canon}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#0D0A2C">
<meta name="author" content="{BRAND}">
<meta property="og:type" content="{'video.other' if '/videos/' in canon and canon.rstrip('/').split('/')[-1] != 'videos' else 'website'}">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="1280">
<meta property="og:image:alt" content="{esc(title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<link rel="icon" href="{rel}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{rel}assets/img/icon-32.png">
<link rel="apple-touch-icon" href="{rel}assets/img/icon-180.png">
<link rel="manifest" href="{rel}site.webmanifest">
<link rel="stylesheet" href="{rel}assets/css/fonts.css">
<link rel="stylesheet" href="{rel}assets/css/main.css?v={ASSET_V["css"]}">
{extra}<script type="application/ld+json">{ld_json(schema)}</script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<div class="progress" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
<header class="nav">
  <a class="nav__brand" href="{rel or './'}" aria-label="GTA MASTER, inicio"><img src="{rel}assets/img/icon-192.png" width="46" height="46" alt=""><span>GTA MASTER</span></a>
  <nav aria-label="Principal"><ul class="nav__links">
    <li><a href="{rel}gta-6/">Guía GTA 6</a></li><li><a href="{rel}#videos">Vídeos</a></li><li><a href="{rel}personajes/">Personajes</a></li><li><a href="{rel}#leonida">Leonida</a></li><li><a href="{rel}blog/">Blog</a></li><li><a href="{rel}#faq">Preguntas</a></li>
  </ul></nav>
  <a class="btn btn--yt" href="{SUB}" target="_blank" rel="noopener">{YT_ICON}<span>Suscríbete</span></a>
</header>
'''

def footer(rel):
    vids = "".join(f'<li><a href="{rel}videos/{v["slug"]}/">{esc(cap(v["h1"].replace("GTA 6: ","")))}</a></li>' for v in V[:6])
    vids2 = "".join(f'<li><a href="{rel}videos/{v["slug"]}/">{esc(cap(v["h1"].replace("GTA 6: ","")))}</a></li>' for v in V[6:])
    return f'''<footer class="footer">
  <div class="footer__grid">
    <div><h2>GTA MASTER</h2><p>GTA 6 en español: detalles que no viste, personajes, mapa de Leonida y curiosidades, con material oficial de Rockstar Games.</p>
    <p><a class="btn btn--yt" href="{SUB}" target="_blank" rel="noopener">{YT_ICON}<span>Canal de YouTube</span></a></p></div>
    <div><h2>Últimos vídeos</h2><ul>{vids}</ul></div>
    <div><h2>Más análisis</h2><ul>{vids2}<li><a href="{rel}videos/">Todos los vídeos</a></li><li><a href="{rel}blog/">Blog de noticias</a></li><li><a href="{rel}privacidad/">Privacidad y cookies</a></li></ul></div>
  </div>
  <small>© <span data-year>2026</span> GTA MASTER · Web de fans, no oficial. Grand Theft Auto, GTA y Grand Theft Auto VI son marcas de Take-Two Interactive. Esta web no está afiliada a Rockstar Games ni a Take-Two. Las imágenes de los vídeos son miniaturas del canal GTA MASTER.</small>
</footer>
<script src="{rel}assets/js/vendor/gsap.min.js" defer></script>
<script src="{rel}assets/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="{rel}assets/js/main.js?v={ASSET_V["js"]}" defer></script>
<script src="{rel}assets/js/comentarios.js?v={ASSET_V["com"]}" defer></script>
</body>
</html>
'''

def video_obj(v, with_id=True):
    o = {"@type": "VideoObject", "name": v["h1"], "description": v["desc"],
         "thumbnailUrl": [f"{SITE}/assets/thumbs/{v['id']}.jpg", f"https://i.ytimg.com/vi/{v['id']}/maxresdefault.jpg"],
         "uploadDate": v["up"], "duration": iso_dur(v.get("len")),
         "embedUrl": f"https://www.youtube.com/embed/{v['id']}", "url": vurl(v), "inLanguage": "es",
         "keywords": ", ".join(v["kw"]), "publisher": {"@id": SITE + "/#org"},
         "potentialAction": {"@type": "WatchAction", "target": f"https://www.youtube.com/watch?v={v['id']}"}}
    if with_id: o["@id"] = vurl(v) + "#video"
    return {k: x for k, x in o.items() if x is not None}

LOADATTR = {True: 'fetchpriority="high"', False: 'loading="lazy"'}
def img(v, cls="", sizes="(max-width:760px) 82vw, 440px", eager=False):
    return (f'<img src="{{rel}}assets/thumbs/{v["id"]}-640.webp" srcset="{{rel}}assets/thumbs/{v["id"]}-640.webp 640w, {{rel}}assets/thumbs/{v["id"]}.webp 1280w" '
            f'sizes="{sizes}" width="1280" height="720" alt="Miniatura del vídeo: {esc(v["h1"])}" {LOADATTR[eager]} decoding="async"{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>')

def card(v, rel):
    return (f'<a class="card" href="{rel}videos/{v["slug"]}/"><div class="card__img">{img(v).replace("{rel}", rel)}<span class="card__dur">{mmss(v.get("len"))}</span></div>'
            f'<div class="card__body"><span class="tag tag--{v["cat"]} px">{v["cat"]}</span><h3>{esc(v["h1"])}</h3><time datetime="{v["up"]}">{fecha(v)}</time></div></a>')

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "url": SITE + "/",
       "logo": {"@type": "ImageObject", "url": SITE + "/assets/img/icon-512.png", "width": 512, "height": 512},
       "sameAs": [CHANNEL, f"https://www.youtube.com/channel/{CHANNEL_ID}"]}

# ---------- HOME ----------
BG = {  # fondo -> (alt, object-position)
 "costa-urbana-pastel": ("Ilustración de una avenida costera de Vice City al atardecer", "50% 60%"),
 "horizonte-neon-noche": ("Ilustración del horizonte de Vice City de noche con luna", "50% 50%"),
 "atardecer-neon-mar": ("", "60% 50%"), "club-art-deco": ("", "65% 50%"), "boulevard-art-deco": ("", "50% 50%"),
 "bahia-urbana": ("", "60% 50%"), "lancha-tropical": ("", "70% 50%"), "everglades-aerodeslizador": ("", "50% 50%"),
 "estadio-tropical": ("", "60% 50%"), "humedales-tropicales": ("", "50% 50%"), "paseo-tropical": ("", "75% 40%"),
}
CAT_BG = {"Leonida": "everglades-aerodeslizador", "Personajes": "bahia-urbana", "Mecánicas": "atardecer-neon-mar",
          "Curiosidades": "club-art-deco", "Música": "club-art-deco", "Historia": "boulevard-art-deco", "Análisis": "costa-urbana-pastel", "Shorts": "paseo-tropical"}

def bgimg(key, rel="", cls="bgpar__img", eager=False, idattr=""):
    alt, pos = BG[key]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img{(" id=" + chr(34) + idattr + chr(34)) if idattr else ""} class="{cls}" src="{rel}assets/bg/{key}-1600.webp" '
            f'srcset="{rel}assets/bg/{key}-900.webp 900w, {rel}assets/bg/{key}-1600.webp 1600w" sizes="100vw" '
            f'width="1600" height="900" alt="{esc(alt)}" {load} decoding="async" style="object-position:{pos}">')

PLAY_IC = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6 4l15 8-15 8z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" d="M4 12h15M13 6l6 6-6 6"/></svg>'


def yt(i): return f"https://www.youtube.com/watch?v={i}"

def vcard(v, rel):
    return (f'<article class="vcard" data-cat="{v["cat"]}">'
            f'<a class="vcard__link" href="{rel}videos/{v["slug"]}/">'
            f'<img src="{rel}assets/thumbs/{v["id"]}-v.webp" width="540" height="720" alt="Miniatura del vídeo: {esc(v["h1"])}" loading="lazy" decoding="async">'
            f'<span class="vcard__shade" aria-hidden="true"></span>'
            f'<span class="tag tag--{v["cat"]} px vcard__tag">{v["cat"]}</span>'
            + (f'<span class="vcard__dur">{mmss(v.get("len"))}</span>' if v.get("len") else "") +
            f'<span class="vcard__text"><span class="vcard__eyebrow">Ver ahora</span><h3>{esc(v.get("card") or v["h1"].replace("GTA 6: ", ""))}</h3><time datetime="{v["up"]}">{fecha(v)}</time></span></a>'
            f'<a class="vcard__play" href="{yt(v["id"])}" target="_blank" rel="noopener" data-yt-out aria-label="Ver en YouTube: {esc(v["h1"])}">{PLAY_IC}</a>'
            f'</article>')

# ---------- RADIOS (confirmadas por Rockstar el 8 oct 2026) ----------
RADIOS = [
    {"n": "Cocoteo FM", "slug": "cocoteo-fm", "g": "Latino moderno", "d": "Reguetón, bachata, merengue y dembow.", "h": "El Martillo y La Gata", "voz": "Bad Bunny y RaiNao", "v": "P1LpnlrMHhg", "c1": "#ff4fa3", "c2": "#ffb347"},
    {"n": "AfroBank FM", "slug": "afrobank-fm", "g": "Afro y amapiano", "d": "Amapiano, clásicos africanos y 3-step.", "h": "Burna y Palmsy", "voz": "Burna Boy y Palms Trax", "v": "V4_fmyQfsd0", "c1": "#1fbf6b", "c2": "#ffc83e"},
    {"n": "Flash FM", "slug": "flash-fm", "g": "Pop", "d": "La emisora de Vice City vuelve con el pop de hoy.", "h": "Robyn y Alex", "voz": "Robyn y Alex Consani", "v": None, "c1": "#3cd0e2", "c2": "#e82c7a"},
    {"n": "Back Country Radio", "slug": "back-country-radio", "g": "Country", "d": "Country rebelde para las carreteras de Leonida.", "h": "MW y Delta Dawne", "voz": "Morgan Wallen y Lana Del Rey", "v": None, "c1": "#c8743a", "c2": "#ffd28a"},
    {"n": "The Chamber 106.6", "slug": "the-chamber", "g": "Metal", "d": "Heavy metal clásico, sin concesiones.", "h": "DJ Kerry y DJ Tom", "voz": "Kerry King y Tom Araya (Slayer)", "v": None, "c1": "#8b1d2c", "c2": "#2a1240", "fq": "106.6"},
    {"n": "Dirty South Classics", "slug": "dirty-south-classics", "g": "Rap del sur", "d": "Clásicos del rap y el hip-hop del sur.", "h": "Trick y Trina", "voz": "Trick Daddy y Trina", "v": None, "c1": "#7a3cff", "c2": "#ff7a59"},
]
EQ = '<span class="radio__eq" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i></span>'

def radio_card(r, rel=""):
    img = os.path.exists(os.path.join(OUT, "assets", "radios", r["slug"] + ".webp"))
    vid = BY.get(r["v"]) if r.get("v") else None
    media = (f'<img src="{rel}assets/radios/{r["slug"]}-360.webp" srcset="{rel}assets/radios/{r["slug"]}-360.webp 360w, {rel}assets/radios/{r["slug"]}.webp 540w" sizes="(max-width:760px) 72vw, 320px" alt="{esc(r["n"])}, emisora de GTA 6" width="540" height="720" loading="lazy" decoding="async">'
             if img else f'<span class="radio__poster{" radio__poster--long" if len(r["n"]) > 12 else ""}" aria-hidden="true"><b>{esc(r["n"])}</b></span>')
    cta = (f'<a class="radio__cta" href="{rel}videos/{vid["slug"]}/">Ver vídeo {ARROW}</a>' if vid
           else f'<a class="radio__cta radio__cta--ghost" href="{rel}gta-6/#musica">Más sobre la música {ARROW}</a>')
    return (f'<li class="radio{" radio--img" if img else ""}" style="--c1:{r["c1"]};--c2:{r["c2"]}">'
            f'<div class="radio__media">{media}<span class="radio__shade" aria-hidden="true"></span>'
            f'<span class="radio__badge px">{esc(r.get("fq") or r["g"])}</span>{EQ}</div>'
            f'<div class="radio__body"><h3>{esc(r["n"])}</h3><p class="radio__g">{esc(r["g"])} · {esc(r["d"])}</p>'
            f'<p class="radio__h">Presentan <strong>{esc(r["h"])}</strong><span> (voces de {esc(r["voz"])})</span></p>{cta}</div></li>')

def radios_slider(rel=""):
    cards = "".join(radio_card(r, rel) for r in RADIOS)
    cards += ('<li class="radio radio--more" style="--c1:#3a1a6e;--c2:#0d0a2c"><div class="radio__media"><span class="radio__poster" aria-hidden="true"><b>+</b></span></div>'
              '<div class="radio__body"><h3>Más emisoras</h3><p class="radio__g">Rockstar ha confirmado 6 de momento. Añadiremos el resto en cuanto se publique la lista completa.</p>'
              f'<a class="radio__cta radio__cta--ghost" href="{rel}videos/#musica">Vídeos de música {ARROW}</a></div></li>')
    return f'''<section class="radios wrap" id="radios" aria-labelledby="t-radios">
  <div class="radios__head"><div><span class="eyebrow px reveal">Sintoniza Leonida</span><h2 class="h2 reveal" id="t-radios">Radios de <span class="grad-text">GTA 6</span></h2></div>
  <div class="radios__nav"><button type="button" class="radios__btn" data-dir="-1" aria-label="Emisora anterior" aria-controls="radios-track">←</button><button type="button" class="radios__btn" data-dir="1" aria-label="Emisora siguiente" aria-controls="radios-track">→</button></div></div>
  <ul class="radios__track" id="radios-track" tabindex="0" aria-label="Emisoras de radio de GTA 6">{cards}</ul>
  <p class="radios__src">Emisoras y presentadores confirmados por Rockstar Games el 8 de octubre de 2026.</p>
</section>'''

def banner(key, eyebrow, title, text, href, cta, side="left", ext=False, eclass=""):
    tgt = ' target="_blank" rel="noopener"' if ext else ""
    return (f'<article class="banner banner--{side} reveal">{bgimg(key, cls="banner__img")}<span class="banner__shade" aria-hidden="true"></span>'
            f'<div class="banner__copy"><span class="banner__eyebrow {eclass}">{eyebrow}</span><h2 class="banner__title">{title}</h2>'
            f'<p>{text}</p><a class="pill" href="{href}"{tgt}><span>{cta}</span>{ARROW}</a></div></article>')

MODAL = '''<dialog class="modal" id="modal" aria-label="Reproductor de vídeo">
  <div class="modal__box"><button class="modal__close" type="button" aria-label="Cerrar">✕</button>
  <div class="modal__frame"></div><p class="modal__title"></p></div>
</dialog>'''

def build_home():
    feat = next(v for v in V if v["id"] == "pgMlP92hjTY")
    coco = BY["P1LpnlrMHhg"]
    title = "GTA 6 en español: noticias, guía y trucos | GTA MASTER"
    desc = "GTA 6 en español: noticias cada día, guía con fecha, precio y PC, personajes, mapa de Leonida, trucos y vídeos con los detalles que no viste."
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebSite", "@id": SITE + "/#web", "url": SITE + "/", "name": BRAND, "alternateName": ["GTA MASTER VI", "GTA Master 6"], "inLanguage": "es", "publisher": {"@id": SITE + "/#org"}},
        ORG,
        {"@type": "WebPage", "@id": SITE + "/#page", "url": SITE + "/", "name": title, "description": desc, "isPartOf": {"@id": SITE + "/#web"},
         "about": {"@type": "VideoGame", "name": "Grand Theft Auto VI", "alternateName": ["GTA 6", "GTA VI"], "gamePlatform": ["PlayStation 5", "Xbox Series X|S"], "datePublished": "2026-11-19",
                   "publisher": {"@type": "Organization", "name": "Rockstar Games"}},
         "primaryImageOfPage": SITE + "/assets/img/og-gta-master.jpg", "inLanguage": "es"},
        {"@type": "ItemList", "@id": SITE + "/#videos", "name": "Vídeos de GTA 6 en español", "numberOfItems": len(V),
         "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": vurl(v)} for i, v in enumerate(V)]},
        {"@type": "FAQPage", "@id": SITE + "/#faq", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
    ]}
    rel = ""
    extra = ('<link rel="preload" as="image" href="assets/bg/costa-urbana-pastel-1600.webp" imagesrcset="assets/bg/costa-urbana-pastel-900.webp 900w, assets/bg/costa-urbana-pastel-1600.webp 1600w" imagesizes="100vw" fetchpriority="high">\n')
    h = head(title, desc, SITE + "/", SITE + "/assets/img/og-gta-master.jpg", rel, schema, extra)
    grid = "".join(vcard(v, rel) for v in V)
    cats = ["Todos"] + [c for c in ["Personajes", "Leonida", "Música", "Mecánicas", "Historia", "Curiosidades", "Análisis", "Shorts"] if any(v["cat"] == c for v in V)]
    chips = "".join(f'<button type="button" class="chip{" is-on" if c == "Todos" else ""}" data-filter="{c}" aria-pressed="{"true" if c == "Todos" else "false"}">{c}</button>' for c in cats)
    cast = "".join(char_section(c, k, "") for k, c in enumerate(CAST))
    regions = "".join(f'<article class="region reveal"><h3>{esc(n)}</h3><p>{esc(t)}</p><a href="videos/{BY[i]["slug"]}/">Vídeo: {esc(l)} →</a></article>' for n, t, i, l in REGIONS)
    faq = "".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in FAQ)
    body = f'''<main id="main">
<section class="hero" aria-labelledby="h1">
  <div class="hero__scene">
    {bgimg("costa-urbana-pastel", cls="hero__img", eager=True, idattr="bg-day")}
    {bgimg("horizonte-neon-noche", cls="hero__img hero__img--night", idattr="bg-night")}
    <span id="night-tint" aria-hidden="true"></span>
  </div>
  <div class="hero__vignette"></div>
  <div class="hero__copy">
    <img class="hero__logo" src="assets/img/logo-gta-master-520.webp" srcset="assets/img/logo-gta-master-520.webp 520w, assets/img/logo-gta-master-900.webp 900w" sizes="(max-width:760px) 74vw, 540px" width="1166" height="968" alt="Logo de GTA MASTER, canal de GTA 6 en español">
    <p class="hero__kicker px">Canal de GTA VI en español</p>
    <h1 id="h1">GTA 6 en español: secretos, detalles y análisis de Grand Theft Auto VI</h1>
    <div class="hero__cta"><a class="btn btn--yt" href="{SUB}" target="_blank" rel="noopener">{YT_ICON}<span>Suscríbete gratis</span></a><a class="btn btn--ghost" href="gta-6/">Guía de GTA 6</a></div>
  </div>
  <div class="hero__night" aria-hidden="true"><p class="big"><span class="grad-text">Cae la noche</span><span class="stroke">en Vice City</span></p></div>
  <div class="hero__scroll" aria-hidden="true"><span class="px">Desliza</span><i></i></div>
</section>

<section class="videos sec" id="videos" aria-labelledby="t-videos">
  <div class="wrap">
    <div class="videos__head"><div><span class="eyebrow px reveal">Vídeos</span><h2 class="h2 reveal" id="t-videos">Vídeos de <span class="grad-text">GTA 6</span></h2></div>
      <a class="pill pill--ghost reveal" href="videos/"><span>Ver todos</span>{ARROW}</a></div>

    <article class="hero-card reveal">
      {bgimg("atardecer-neon-mar", cls="hero-card__img bgpar__img")}
      <span class="hero-card__shade" aria-hidden="true"></span>
      <div class="hero-card__copy">
        <span class="banner__eyebrow">Ver ahora · El más visto</span>
        <h3 class="hero-card__title">10 detalles que no viste en la mirada extendida</h3>
        <p>{esc(feat["intro"][0])}</p>
        <div class="hero-card__actions">
          <a class="pill pill--light" href="{yt(feat["id"])}" target="_blank" rel="noopener" data-yt-out>{PLAY_IC}<span>Reproducir en YouTube</span></a>
          <a class="pill pill--ghost" href="videos/{feat["slug"]}/"><span>Leer el análisis</span>{ARROW}</a>
        </div>
        <div class="meta-row"><span>{mmss(feat["len"])} min</span><span>{fecha(feat)}</span><span>Material oficial</span></div>
      </div>
      <img class="hero-card__thumb" src="assets/thumbs/{feat["id"]}-640.webp" width="640" height="360" alt="Miniatura del vídeo: {esc(feat["h1"])}" loading="lazy" decoding="async">
    </article>

    <div class="chips" role="group" aria-label="Filtrar vídeos por tema">{chips}</div>
    <div class="vgrid">{grid}</div>
  </div>
</section>

{home_news()}
<div class="stats" role="list">
  <div class="stat" role="listitem"><b data-count="{len(V)}">{len(V)}</b><span>Análisis publicados</span></div>
  <div class="stat" role="listitem"><b data-count="6">6</b><span>Regiones de Leonida</span></div>
  <div class="stat" role="listitem"><b data-count="2">2</b><span>Protagonistas</span></div>
  <div class="stat" role="listitem"><b>0</b><span>Filtraciones: solo material oficial</span></div>
</div>

<section class="banners wrap" aria-label="Destacados">
  {banner("club-art-deco", "Música · Cocoteo FM", "La radio latina de GTA&nbsp;6", "Bad Bunny y RaiNao presentan Cocoteo FM: bachata, merengue, dembow y reguetón para las noches de Vice City. Diez curiosidades en el vídeo.", "videos/" + coco["slug"] + "/", "Descubre más", side="left", eclass="is-cian")}
</section>
{radios_slider("")}

<section class="cast sec" id="personajes" aria-labelledby="t-cast">
  <div class="wrap"><span class="eyebrow px reveal">Quién es quién</span><h2 class="h2 reveal" id="t-cast">Personajes de <span class="grad-text">GTA 6</span></h2>
  <p class="lead reveal">Jason y Lucia llevan la historia, pero Leonida está llena de secundarios. Este es todo el reparto confirmado hasta hoy.</p></div>
  {cast}
  <div class="wrap" style="text-align:center;padding-top:2rem"><a class="pill" href="personajes/"><span>Todos los personajes, explicados</span>{ARROW}</a></div>
</section>

<section class="leonida sec bgpar" id="leonida" aria-labelledby="t-leo">
  {bgimg("everglades-aerodeslizador")}<span class="bgpar__veil" aria-hidden="true"></span>
  <div class="wrap"><span class="eyebrow px reveal">El mapa</span><h2 class="h2 reveal" id="t-leo">Leonida, <span class="grad-text">zona a zona</span></h2>
  <p class="lead reveal">El estado ficticio de GTA 6, inspirado en Florida, se divide en seis regiones. De los rascacielos de Vice City a los pantanos de Grassrivers.</p>
  <div class="regions">{regions}</div></div>
</section>

<section class="launch sec bgpar" aria-labelledby="t-launch">
  {bgimg("estadio-tropical")}<span class="bgpar__veil bgpar__veil--launch" aria-hidden="true"></span>
  <div class="wrap"><span class="eyebrow px">Lanzamiento</span><h2 class="h2" id="t-launch">GTA 6 sale el <span class="grad-text">19 de noviembre</span></h2>
  <p class="lead">PlayStation 5 y Xbox Series X|S. Cuenta atrás hasta las 00:00 del 19 de noviembre, hora peninsular española.</p>
  <div class="countdown" data-countdown="{LAUNCH}" aria-live="off">
    <div><b data-u="d">00</b><span class="px">Días</span></div><div><b data-u="h">00</b><span class="px">Horas</span></div><div><b data-u="m">00</b><span class="px">Min</span></div><div><b data-u="s">00</b><span class="px">Seg</span></div>
  </div></div>
</section>

<section class="faq sec bgpar" id="faq" aria-labelledby="t-faq">
  {bgimg("humedales-tropicales")}<span class="bgpar__veil bgpar__veil--deep" aria-hidden="true"></span>
  <div class="wrap"><span class="eyebrow px reveal">Dudas rápidas</span><h2 class="h2 reveal" id="t-faq">Preguntas sobre <span class="grad-text">GTA 6</span></h2>
  <div class="faq__list">{faq}</div></div>
</section>

<section class="cta" aria-label="Suscríbete a GTA MASTER">
  <div class="marquee" aria-hidden="true"><div class="marquee__inner"><span>Suscríbete</span><span>GTA Master</span><span>Suscríbete</span><span>GTA Master</span></div><div class="marquee__inner"><span>Suscríbete</span><span>GTA Master</span><span>Suscríbete</span><span>GTA Master</span></div></div>
  <div class="wrap">
  {banner("paseo-tropical", "Únete a la banda", "Suscríbete a GTA MASTER", "Un vídeo nuevo de GTA 6 casi cada día. Activa la campana y no te pierdas nada de Leonida.", SUB, "Suscribirme en YouTube", side="left", ext=True, eclass="is-oro")}
  </div>
</section>
</main>
'''
    open(os.path.join(OUT, "index.html"), "w").write(h + body + footer(rel))

# ---------- PÁGINA DE VÍDEO ----------
GUIA_ANCLA = {"Personajes": ("historia", "Historia y personajes de GTA 6"), "Leonida": ("mapa", "El mapa de GTA 6: Leonida y Vice City"),
              "Mecánicas": ("rendimiento", "Fps, tamaño y cómo funciona GTA 6"), "Historia": ("historia", "La historia de GTA 6"),
              "Música": ("musica", "Música y radios de GTA 6"), "Curiosidades": ("notas", "Curiosidades y detalles de GTA 6"), "Análisis": ("notas", "Notas y análisis de GTA 6"),
              "Shorts": ("fecha", "Fecha, precio y todo sobre GTA 6")}
def _palabras(t):
    return {w for w in re.findall(r"[a-záéíóúñ0-9]{4,}", t.lower())} - {"gta", "grand", "theft", "auto", "rockstar", "sobre", "como", "todo", "para", "este", "esta"}
def related_posts(text, n=2, excluir=None):
    q = _palabras(text)
    cands = [p for p in POSTS if p["slug"] != excluir]
    cands.sort(key=lambda p: (len(q & _palabras(p["title"] + " " + " ".join(p.get("tags", [])))), p["date"]), reverse=True)
    return cands[:n]
def sigue_leyendo(rel, cat, text, excluir=None):
    a, t = GUIA_ANCLA.get(cat, ("fecha", "Todo sobre GTA 6"))
    items = [f'<li><a href="{rel}gta-6/#{a}">{esc(t)}</a> <span>· Guía GTA 6</span></li>']
    if cat in ("Personajes", "Historia"): items.append(f'<li><a href="{rel}personajes/">Todos los personajes de GTA 6</a> <span>· Fichas</span></li>')
    items += [f'<li><a href="{rel}blog/{p["slug"]}/">{esc(p["title"])}</a> <span>· Noticia</span></li>' for p in related_posts(text, 2, excluir)]
    return f'<nav class="readmore" aria-label="Sigue leyendo"><h2>Sigue leyendo</h2><ul>{"".join(items)}</ul></nav>'

def build_video(v):
    rel = "../../"
    canon = vurl(v)
    related = [x for x in V if x["id"] != v["id"] and x["cat"] == v["cat"]][:3]
    related += [x for x in V if x["id"] != v["id"] and x not in related][: 5 - len(related)]
    schema = {"@context": "https://schema.org", "@graph": [
        ORG, video_obj(v),
        {"@type": "WebPage", "@id": canon, "url": canon, "name": v["title"], "description": v["desc"], "inLanguage": "es",
         "isPartOf": {"@id": SITE + "/#web"}, "primaryImageOfPage": f"{SITE}/assets/thumbs/{v['id']}.jpg", "mainEntity": {"@id": canon + "#video"},
         "breadcrumb": {"@id": canon + "#bc"}},
        {"@type": "BreadcrumbList", "@id": canon + "#bc", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Vídeos de GTA 6", "item": SITE + "/videos/"},
            {"@type": "ListItem", "position": 3, "name": v["h1"], "item": canon}]},
    ]}
    title = f'{v["title"]}'
    if len(title) + len(" | GTA MASTER") <= 60: title += " | GTA MASTER"
    h = head(title, v["desc"], canon, f"{SITE}/assets/thumbs/{v['id']}.jpg", rel, schema,
             f'<link rel="preload" as="image" href="{rel}assets/bg/{CAT_BG[v["cat"]]}-1600.webp" imagesrcset="{rel}assets/bg/{CAT_BG[v["cat"]]}-900.webp 900w, {rel}assets/bg/{CAT_BG[v["cat"]]}-1600.webp 1600w" imagesizes="100vw">\n')
    pts = "".join(f"<li>{esc(p)}</li>" for p in v["points"])
    rels = "".join(f'<a class="mini" href="{rel}videos/{x["slug"]}/">{img(x, sizes="140px").replace("{rel}", rel)}<span>{esc(x["h1"])}</span></a>' for x in related)
    body = f'''<main id="main">
<section class="vhero bgpar">{bgimg(CAT_BG[v["cat"]], rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span>
  <nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li><a href="{rel}videos/">Vídeos</a></li><li aria-current="page">{esc(v["cat"])}</li></ol></nav>
  <span class="tag tag--{v["cat"]} px">{v["cat"]}</span>
  <h1>{esc(v["h1"])}</h1>
  <div class="meta-row">{f"<span>{mmss(v.get(chr(108)+chr(101)+chr(110)))} min</span>" if v.get("len") else ""}<time datetime="{v["up"]}">{fecha(v)}</time><span>Español</span></div>
</section>
<div class="vbody">
  <article>
    <div class="player">{img(v, sizes="(max-width:900px) 92vw, 60vw", eager=False).replace("{rel}", rel)}
      <a class="player__btn" href="{yt(v["id"])}" target="_blank" rel="noopener" data-yt-out aria-label="Ver en YouTube: {esc(v["h1"])}"><span>{PLAY}</span><em class="player__yt">{YT_ICON}Se abre en YouTube</em></a></div>
    <h2>De qué trata el vídeo</h2>
    {"".join(f"<p>{esc(p)}</p>" for p in v["intro"])}
    {f'<h2>Puntos clave</h2><ul class="points">{pts}</ul>' if pts else ""}
    <p><a class="btn btn--yt" href="https://www.youtube.com/watch?v={v["id"]}" target="_blank" rel="noopener">{YT_ICON}<span>Verlo en YouTube</span></a></p>
    <p style="font-size:.9rem">Título en YouTube: «{esc(v["yt"])}». Análisis hecho con material oficial de Rockstar Games, sin filtraciones.</p>
    {sigue_leyendo(rel, v["cat"], v["h1"] + " " + " ".join(v.get("kw", [])))}
  </article>
  <aside aria-label="Vídeos relacionados"><h2>Sigue viendo</h2>{rels}
    <p style="margin-top:1.4rem"><a class="link-arrow" href="{rel}videos/">Todos los vídeos de GTA 6 →</a></p></aside>
</div>
</main>
'''
    d = os.path.join(OUT, "videos", v["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

# ---------- BLOG ----------
POSTS_PATH = os.path.join(OUT, "data", "posts.json")
POSTS = json.load(open(POSTS_PATH, encoding="utf-8")) if os.path.exists(POSTS_PATH) else []
POSTS.sort(key=lambda p: p["date"], reverse=True)

def purl(p): return f"{SITE}/blog/{p['slug']}/"
def pfecha(p):
    dt = datetime.fromisoformat(p["date"]).astimezone(MAD)
    return f"{dt.day} {MESES[dt.month-1]} {dt.year}"
def read_min(p): return max(2, round(len(re.sub(r"<[^>]+>", " ", p["body"]).split()) / 200))

def _inline(s, rel):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    def link(m):
        t, u = m.group(1), m.group(2).replace("&amp;", "&")
        if u.startswith("/") and not u.startswith("//"):
            return f'<a href="{rel}{esc(u.lstrip("/"))}">{t}</a>'
        if re.match(r"^https?://[\w.-]+(/|$)", u, re.I):
            return f'<a href="{esc(u)}" target="_blank" rel="noopener noreferrer">{t}</a>'
        return t  # cualquier otro esquema (javascript:, data:…) se queda en texto plano
    return re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)

def yt_embed(vid, title):
    return (f'<figure class="yt"><div class="yt__frame"><iframe src="https://www.youtube-nocookie.com/embed/{vid}?rel=0" '
            f'title="{esc(title)}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" '
            f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>'
            f'<figcaption>{esc(title)} · <a href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">Ver en YouTube</a></figcaption></figure>')

def md(text, rel):
    out = []
    for block in [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]:
        m = re.match(r"^\{\{youtube:([\w-]{11})\s*\|\s*(.+?)\}\}$", block)
        if m: out.append(yt_embed(m.group(1), m.group(2))); continue
        if block.startswith("### "): out.append(f"<h3>{_inline(block[4:], rel)}</h3>"); continue
        if block.startswith("## "): out.append(f"<h2>{_inline(block[3:], rel)}</h2>"); continue
        lines = block.split("\n")
        if all(l.startswith("- ") for l in lines):
            out.append("<ul>" + "".join(f"<li>{_inline(l[2:], rel)}</li>" for l in lines) + "</ul>"); continue
        if all(l.strip().startswith("|") for l in lines) and len(lines) >= 3:
            rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines if not re.match(r"^\|?\s*:?-{2,}", l.strip())]
            th = "".join(f"<th>{_inline(c, rel)}</th>" for c in rows[0])
            tb = "".join("<tr>" + "".join(f"<td>{_inline(c, rel)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="table"><table><thead><tr>{th}</tr></thead><tbody>{tb}</tbody></table></div>'); continue
        if block.startswith("> "): out.append(f"<blockquote>{_inline(block[2:], rel)}</blockquote>"); continue
        out.append(f"<p>{_inline(' '.join(lines), rel)}</p>")
    return "\n".join(out)

def pcard(p, rel):
    return (f'<a class="pcard" href="{rel}blog/{p["slug"]}/"><div class="pcard__img">'
            f'<img src="{rel}assets/blog/{p["slug"]}-640.webp" srcset="{rel}assets/blog/{p["slug"]}-640.webp 640w, {rel}assets/blog/{p["slug"]}.webp 1280w" sizes="(max-width:760px) 92vw, 420px" width="1280" height="720" alt="{esc(p.get("cover_alt") or p["title"])}" loading="lazy" decoding="async"></div>'
            f'<div class="pcard__body"><span class="tag px">{esc(p["cat"])}</span><h3>{esc(p["title"])}</h3><p>{esc(p["desc"])}</p>'
            f'<time datetime="{p["date"]}">{pfecha(p)}</time></div></a>')

def build_posts():
    for i, p in enumerate(POSTS):
        rel = "../../"; canon = purl(p); img = f"{SITE}/assets/blog/{p['slug']}.jpg"
        title = p.get("seo_title") or p["title"]
        if len(title) + 15 <= 62: title += " | GTA MASTER"
        schema = {"@context": "https://schema.org", "@graph": [ORG,
            {"@type": "NewsArticle", "@id": canon + "#article", "headline": p["title"][:110], "description": p["desc"],
             "image": [img], "datePublished": p["date"], "dateModified": p.get("updated", p["date"]), "inLanguage": "es",
             "articleSection": p["cat"], "keywords": ", ".join(p.get("tags", [])),
             "author": {"@type": "Organization", "name": "Redacción GTA MASTER", "url": SITE + "/"},
             "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": canon,
             "citation": [s["url"] for s in p.get("sources", [])],
             "about": {"@type": "VideoGame", "name": "Grand Theft Auto VI"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": canon}]}]}
        h = head(title, p["desc"], canon, img, rel, schema,
                 f'<meta property="article:published_time" content="{p["date"]}">\n<link rel="alternate" type="application/rss+xml" title="Blog GTA MASTER" href="{SITE}/blog/feed.xml">\n', csp=CSP_COMENTARIOS)
        h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
        src = "".join(f'<li><a href="{esc(s["url"])}" target="_blank" rel="noopener">{esc(s["name"])}</a>{(" · " + esc(s["note"])) if s.get("note") else ""}</li>' for s in p.get("sources", []))
        others = [x for x in POSTS if x["slug"] != p["slug"]][:3]
        more = f'<section class="wrap post__more"><h2 class="h2" style="font-size:clamp(2rem,1.4rem + 2.4vw,3.4rem)">Más noticias</h2><div class="bgrid">{"".join(pcard(x, rel) for x in others)}</div></section>' if others else ""
        body = f'''<main id="main">
<article class="post">
  <header class="vhero bgpar">{bgimg(p.get("fondo", "horizonte-neon-noche"), rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span>
    <nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li><a href="{rel}blog/">Blog</a></li><li aria-current="page">{esc(p["cat"])}</li></ol></nav>
    <span class="tag px">{esc(p["cat"])}</span>
    <h1>{esc(p["title"])}</h1>
    <div class="meta-row"><time datetime="{p["date"]}">{pfecha(p)}</time><span>Redacción GTA MASTER</span><span>{read_min(p)} min de lectura</span></div>
  </header>
  <div class="post__wrap">
    <figure class="post__cover"><img src="{rel}assets/blog/{p["slug"]}.webp" width="1280" height="720" alt="{esc(p.get("cover_alt") or p["title"])}" fetchpriority="high"><figcaption>Portada: GTA MASTER</figcaption></figure>
    <p class="post__lead">{_inline(p["desc"], rel)}</p>
    <div class="post__body">{md(p["body"], rel)}</div>
    <aside class="sources" aria-label="Fuentes"><h2>Fuentes</h2><ul>{src}</ul>
      <p>Las noticias de GTA MASTER se basan en las fuentes citadas. Si algo es un rumor, lo indicamos.</p></aside>
    <p><a class="btn btn--yt" href="{SUB}" target="_blank" rel="noopener">{YT_ICON}<span>Más GTA 6 en YouTube</span></a></p>
    {sigue_leyendo(rel, p["cat"], p["title"] + " " + " ".join(p.get("tags", [])), p["slug"])}
    {comentarios(p, canon, rel)}
  </div>
</article>
{more}
</main>
'''
        d = os.path.join(OUT, "blog", p["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

def build_blog_index():
    rel = "../"; canon = SITE + "/blog/"
    title = "Noticias de GTA 6 en español: blog diario | GTA MASTER"
    desc = "Noticias de GTA 6 cada día: lanzamiento, personajes, trucos y curiosidades de Grand Theft Auto VI, con fuentes y vídeos. Blog de GTA MASTER."
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "CollectionPage", "@id": canon, "url": canon, "name": title, "description": desc, "inLanguage": "es", "isPartOf": {"@id": SITE + "/#web"}},
        {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": purl(p)} for i, p in enumerate(POSTS)]}]}
    h = head(title, desc, canon, SITE + "/assets/img/og-gta-master.jpg", rel, schema,
             f'<link rel="alternate" type="application/rss+xml" title="Blog GTA MASTER" href="{SITE}/blog/feed.xml">\n')
    cards = "".join(pcard(p, rel) for p in POSTS) or '<p class="lead">Pronto, las primeras noticias.</p>'
    body = f'''<main id="main"><section class="vhero bgpar">{bgimg("horizonte-neon-noche", rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span>
<nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li aria-current="page">Blog</li></ol></nav>
<span class="eyebrow px">Cada día</span><h1>Noticias de GTA 6</h1><p class="lead">Lanzamiento, personajes, trucos y curiosidades de Grand Theft Auto VI. Siempre con la fuente y, cuando lo hay, con el vídeo.</p></section>
<div class="wrap" style="padding-bottom:5rem"><div class="bgrid">{cards}</div></div></main>
'''
    d = os.path.join(OUT, "blog"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))
    # RSS
    items = "".join(f'<item><title>{esc(p["title"])}</title><link>{purl(p)}</link><guid>{purl(p)}</guid>'
                    f'<pubDate>{datetime.fromisoformat(p["date"]).strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate>'
                    f'<description>{esc(p["desc"])}</description><enclosure url="{SITE}/assets/blog/{p["slug"]}.jpg" type="image/jpeg" length="0"/></item>' for p in POSTS[:30])
    open(os.path.join(d, "feed.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>GTA MASTER · Noticias de GTA 6</title>'
        f'<link>{SITE}/blog/</link><description>{esc(desc)}</description><language>es</language>{items}</channel></rss>')

def home_news(rel=""):
    if not POSTS: return ""
    return f'''<section class="news sec" id="noticias" aria-labelledby="t-news">
  <div class="wrap"><div class="videos__head"><div><span class="eyebrow px reveal">Blog diario</span><h2 class="h2 reveal" id="t-news">Lo último de <span class="grad-text">GTA 6</span></h2></div>
  <a class="pill pill--ghost reveal" href="{rel}blog/"><span>Todas las noticias</span>{ARROW}</a></div>
  <div class="bgrid" style="margin-top:2.4rem">{"".join(pcard(p, rel) for p in POSTS[:3])}</div></div>
</section>
'''

def char_img(c, rel, sizes="(max-width:820px) 92vw, 46vw"):
    p = f"{rel}assets/personajes/{c['slug']}"
    return (f'<img src="{p}.webp" srcset="{p}-640.webp 640w, {p}.webp 1280w" sizes="{sizes}" width="1280" height="720" '
            f'alt="{esc(c["n"])}, personaje de GTA 6: portada de GTA MASTER" loading="lazy" decoding="async">')

def char_section(c, k, rel, full=False):
    """Bloque de personaje con el mismo diseño en la portada y en /personajes/."""
    v = BY.get(c["v"]) if c["v"] else None
    if v:
        href = f'{rel}videos/{v["slug"]}/'; media = char_img(c, rel); cta = "Ver el análisis"
    else:
        href = f'{rel}personajes/#{c["slug"]}'; media = char_img(c, rel); cta = "Ver la ficha"
    if full and not v:
        href = f'{rel}personajes/#{c["slug"]}'
    text = f'<p>{esc(c["t"])}</p>' + (f'<p>{esc(c["bio"])}</p>' if full else "")
    btn = (f'<a class="pill pill--ghost" href="{href}"><span>{cta}</span>{ARROW}</a>' if (v or not full) else "")
    return f'''<article class="char" id="{c["slug"]}">{bgimg(c["bg"], rel=rel, cls="char__bg bgpar__img")}<span class="char__veil" aria-hidden="true"></span>
  <div class="char__inner wrap"><span class="char__name" aria-hidden="true">{esc(c["big"])}</span>
  <div class="char__media"><a href="{href}" aria-label="{esc(c["n"])}">{media}</a></div>
  <div class="char__copy reveal"><span class="eyebrow px">Personaje {k+1:02d} · {c["rol"]}</span><{"h2" if full else "h3"} class="char__h">{esc(c["n"])}</{"h2" if full else "h3"}>{text}
  {btn}</div></div></article>'''

def build_personajes():
    rel = "../"; canon = SITE + "/personajes/"
    title = "Personajes de GTA 6: todo el reparto, explicado | GTA MASTER"
    desc = "Todos los personajes de GTA 6: Jason Duval, Lucia Caminos, Raul Bautista, Brian Heder, Boobie Ike, Cal Hampton, Dre'Quan Priest, Real Dimez, Andrés de León y Petra Navarro."
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "CollectionPage", "@id": canon, "url": canon, "name": title, "description": desc, "inLanguage": "es", "isPartOf": {"@id": SITE + "/#web"},
         "about": {"@type": "VideoGame", "name": "Grand Theft Auto VI"}, "citation": [u for _, u in CAST_SOURCES]},
        {"@type": "ItemList", "name": "Personajes de GTA 6", "numberOfItems": len(CAST), "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": c["n"], "url": f"{canon}#{c['slug']}",
             "image": f"{SITE}/assets/personajes/{c['slug']}.jpg"} for i, c in enumerate(CAST)]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Personajes de GTA 6", "item": canon}]}]}
    h = head(title, desc, canon, SITE + "/assets/personajes/raul-bautista.jpg", rel, schema)
    idx = "".join(f'<a class="chip" href="#{c["slug"]}">{esc(c["n"])}</a>' for c in CAST)
    secs = "".join(char_section(c, k, rel, full=True) for k, c in enumerate(CAST))
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in CAST_SOURCES)
    body = f'''<main id="main"><section class="vhero bgpar">{bgimg("club-art-deco", rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span>
<nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li aria-current="page">Personajes</li></ol></nav>
<span class="eyebrow px">Quién es quién</span><h1>Personajes de GTA 6</h1><p class="lead">Los dos protagonistas y el reparto secundario confirmado de Grand Theft Auto VI, con lo que se sabe de cada uno.</p>
<div class="chips" style="margin-top:1.6rem">{idx}</div></section>
<section class="cast">{secs}</section>
<div class="wrap" style="padding-block:3rem 5rem"><aside class="sources"><h2>Fuentes</h2><ul>{src}</ul>
<p>Las portadas de los personajes son ilustraciones originales de GTA MASTER, creadas con IA a partir de escenas de su mundo. No reproducen arte oficial de Rockstar ni dibujan a los personajes.</p></aside></div></main>
'''
    d = os.path.join(OUT, "personajes"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

# ---------- GUÍA PILAR /gta-6/ ----------
GUIA_FAQ = [
 ("¿Cuándo sale GTA 6?", "GTA 6 sale el jueves 19 de noviembre de 2026 en PlayStation 5 y Xbox Series X|S. En España se desbloquea a las 00:00 del 19 de noviembre, hora peninsular."),
 ("¿Cuánto cuesta GTA 6?", "En España, la edición estándar cuesta 79,99 € y la Ultimate Edition 99,99 €. En Estados Unidos, 79,99 y 99,99 dólares."),
 ("¿GTA 6 sale en PC?", "No en el lanzamiento. Rockstar solo ha anunciado PS5 y Xbox Series X|S y no hay fecha para PC. Take-Two ha dicho que los jugadores de consola son su público principal."),
 ("¿Cuánto ocupa GTA 6?", "Hasta 212 GB, según la consola. La precarga para las reservas digitales empezó el 10 de noviembre."),
 ("¿La edición física de GTA 6 trae disco?", "No. La caja incluye un código de descarga, así que hace falta el mismo espacio y conexión a Internet que en digital."),
 ("¿A cuántos fps va GTA 6?", "A 30 fps en todas las consolas, incluida PS5 Pro. Rockstar no ha confirmado un modo a 60 fps."),
 ("¿Cuánto dura GTA 6?", "Unas 80 horas la historia con algunos objetivos opcionales, según Rob Nelson, de Rockstar North. Completarlo todo lleva bastante más."),
 ("¿Qué nota tiene GTA 6?", "Un 99 en Metacritic con 146 reseñas y un 99 en OpenCritic el día antes del lanzamiento, con dieces en IGN, GameSpot y Game Informer."),
 ("¿Quiénes son los protagonistas de GTA 6?", "Jason Duval y Lucia Caminos, una pareja que se mete en el crimen de Leonida. Es la primera vez que un GTA principal tiene una protagonista."),
 ("¿Dónde transcurre GTA 6?", "En Leonida, un estado ficticio inspirado en Florida, con Vice City (inspirada en Miami) como gran ciudad. Según Rockstar North, Vice City es el doble de grande que Los Santos de GTA V."),
 ("¿GTA 6 tiene trucos?", "Sí: 61, pero solo se desbloquean al terminar la historia y cada uno pide además un reto. Se introducen con el móvil del juego (arriba en la cruceta, L1 + R1 o LB + RB y la combinación) y desactivan trofeos, logros y guardado durante esa sesión."),
]
GUIA_FUENTES = [
 ("Rockstar Games: Grand Theft Auto VI", "https://www.rockstargames.com/VI"),
 ("Vandal: guía de reserva, precio y ediciones de GTA 6", "https://vandal.elespanol.com/noticia/1350791112/guia-de-reserva-de-gta-6-precio-hora-ediciones-y-todas-las-novedades-confirmadas-por-rockstar/"),
 ("God is a Geek: Take-Two y la versión de PC", "https://godisageek.com/?p=308419"),
 ("GamesRadar+: GTA 6 ocupa 212 GB", "https://gamesradar.com/games/grand-theft-auto/rockstar-confirms-gta-6-is-212gb-pre-loading-opens-earlier-than-previously-announced-for-digital-orders"),
 ("Notebookcheck: 30 fps en consolas", "https://notebookcheck.net/Rockstar-reveals-GTA-6-console-performance-targets-and-PS5-Pro-upgrades.1447121.0.html"),
 ("Tom's Guide: resumen de reseñas", "https://www.tomsguide.com/news/live/gta-6-review-roundup-live-updates"),
 ("GamesRadar+: GTA 6 dura unas 80 horas", "https://www.gamesradar.com/games/grand-theft-auto/how-long-is-gta-6-about-80-hours-according-to-one-rockstar-devs-playthrough/"),
 ("Insider Gaming: Vice City es el doble que Los Santos", "https://insider-gaming.com/gta-6-vice-city-twice-size-los-santos-map/"),
 ("TweakTown: GTA Online seguirá tras GTA 6", "https://tweaktown.com/news/113044/gta-online-will-continue-after-gta-6s-release-take-two-reiterates/index.html"),
]

FAQ = GUIA_FAQ + FAQ_EXTRA  # todas las preguntas viven en el apartado «Preguntas» de la portada

def build_guia():
    rel = "../"; canon = SITE + "/gta-6/"
    title = "GTA 6: fecha, precio, PC, mapa y todo lo que sabemos"
    desc = "Guía de GTA 6 en español: fecha y hora de lanzamiento, precio y ediciones, si sale en PC, cuánto ocupa, 30 fps, duración, mapa, personajes y trucos."
    def vl(slug_part, text):
        v = next((x for x in V if slug_part in x["slug"]), None)
        return f'<a href="{rel}videos/{v["slug"]}/">{esc(text)}</a>' if v else esc(text)
    def pl(slug, text):
        return f'<a href="{rel}blog/{slug}/">{esc(text)}</a>' if any(p["slug"] == slug for p in POSTS) else esc(text)
    toc = [("fecha", "Fecha y hora"), ("precio", "Precio y ediciones"), ("plataformas", "PS5, Xbox y PC"), ("tamano", "Cuánto ocupa"),
           ("rendimiento", "Fps y resolución"), ("notas", "Notas"), ("duracion", "Duración"), ("historia", "Historia y personajes"),
           ("mapa", "Mapa de Leonida"), ("musica", "Música y radios"), ("trucos", "Trucos"), ("online", "GTA Online")]
    ficha = [("Lanzamiento", "19 de noviembre de 2026"), ("Hora en España", "00:00 (peninsular)"), ("Plataformas", "PS5, PS5 Pro, Xbox Series X|S"),
             ("PC", "Sin fecha anunciada"), ("Precio", "79,99 € estándar · 99,99 € Ultimate"), ("Tamaño", "Hasta 212 GB"),
             ("Fps", "30 en todas las consolas"), ("Duración", "Unas 80 h la historia"), ("Metacritic", "99"), ("Desarrolla", "Rockstar Games")]
    tabla = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in ficha)
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener noreferrer">{esc(n)}</a></li>' for n, u in GUIA_FUENTES)
    chips = "".join(f'<a class="chip" href="#{i}">{esc(t)}</a>' for i, t in toc)
    pjs = ", ".join(f'<a href="{rel}personajes/#{c["slug"]}">{esc(c["n"])}</a>' for c in CAST[2:])
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "Article", "@id": canon + "#article", "headline": title, "description": desc, "inLanguage": "es",
         "datePublished": "2026-11-18T20:30:00+01:00", "dateModified": "2026-11-18T20:30:00+01:00", "mainEntityOfPage": canon,
         "image": [SITE + "/assets/img/og-gta-master.jpg"], "author": {"@type": "Organization", "name": "Redacción GTA MASTER", "url": SITE + "/"},
         "publisher": {"@id": SITE + "/#org"}, "about": {"@id": canon + "#game"}, "citation": [u for _, u in GUIA_FUENTES]},
        {"@type": "VideoGame", "@id": canon + "#game", "name": "Grand Theft Auto VI", "alternateName": ["GTA 6", "GTA VI"],
         "genre": ["Acción", "Mundo abierto"], "gamePlatform": ["PlayStation 5", "Xbox Series X|S"], "datePublished": "2026-11-19",
         "publisher": {"@type": "Organization", "name": "Rockstar Games"}, "author": {"@type": "Organization", "name": "Rockstar Games"},
         "offers": [{"@type": "Offer", "name": "Edición estándar", "price": "79.99", "priceCurrency": "EUR"},
                    {"@type": "Offer", "name": "Ultimate Edition", "price": "99.99", "priceCurrency": "EUR"}]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                                                        {"@type": "ListItem", "position": 2, "name": "Guía de GTA 6", "item": canon}]}]}
    h = head(title + " | GTA MASTER", desc, canon, SITE + "/assets/img/og-gta-master.jpg", rel, schema)
    h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">')
    body = f"""<main id="main"><section class="vhero bgpar">{bgimg("costa-urbana-pastel", rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span>
<nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li aria-current="page">Guía de GTA 6</li></ol></nav>
<span class="eyebrow px">Guía completa · actualizada el 18 nov 2026</span><h1>GTA 6: todo lo que sabemos</h1>
<p class="lead">Fecha y hora de lanzamiento, precio, plataformas, cuánto ocupa, rendimiento, duración, mapa, personajes, música y trucos de Grand Theft Auto VI. Solo datos confirmados, con su fuente.</p>
<div class="chips" style="margin-top:1.4rem">{chips}</div></section>
<div class="post__wrap guia">
<div class="table"><table class="ficha"><caption>Ficha de GTA 6</caption><tbody>{tabla}</tbody></table></div>
<div class="post__body">
<h2 id="fecha">Fecha y hora de lanzamiento de GTA 6</h2>
<p>Grand Theft Auto VI sale el <strong>jueves 19 de noviembre de 2026</strong>. Llega tras dos retrasos: primero estaba previsto para otoño de 2025 y después para el 26 de mayo de 2026. El juego se desbloquea a medianoche, hora local de cada país. En España es a las <strong>00:00 del 19 de noviembre</strong> y en Nueva Zelanda ya se juega desde las 12:00 del día 18, hora peninsular. Tienes todas las horas por país en {pl("gta-6-hora-lanzamiento-espana-nueva-zelanda", "nuestra noticia sobre la hora de lanzamiento")}.</p>
<h2 id="precio">Precio y ediciones de GTA 6</h2>
<p>Rockstar vende dos ediciones. En España, la <strong>estándar cuesta 79,99 €</strong> y la <strong>Ultimate Edition, 99,99 €</strong>, según la guía de reserva de Vandal. En Estados Unidos los precios son 79,99 y 99,99 dólares. Las reservas abrieron el 25 de junio de 2026.</p>
<p>La edición física no incluye disco, sino un código de descarga. Te lo contamos en {vl("caja-vacia", "nuestro vídeo sobre la caja sin disco")}.</p>
<h2 id="plataformas">¿GTA 6 sale en PS5, Xbox y PC?</h2>
<p>GTA 6 sale en <strong>PlayStation 5, PS5 Pro y Xbox Series X|S</strong>. No hay versión de PC en el lanzamiento ni fecha anunciada: el consejero delegado de Take-Two, Strauss Zelnick, explicó en mayo que el público principal de la saga está en consola. Con GTA V, la versión de PC llegó un año y medio después que la de consola.</p>
<h2 id="tamano">Cuánto ocupa GTA 6</h2>
<p>Rockstar ha confirmado que GTA 6 necesita <strong>hasta 212 GB</strong>, según la consola. En una Xbox Series S de 512 GB cabe, pero ocupa más de la mitad del disco. Si tienes PS5, recuerda instalar la actualización del sistema que Sony ha publicado para el lanzamiento. Lo explicamos en {pl("gta-6-212-gb-precarga-espacio", "cómo hacer sitio para GTA 6")} y en {pl("gta-6-actualizacion-ps5-obligatoria", "la actualización obligatoria de PS5")}.</p>
<h2 id="rendimiento">Fps y resolución de GTA 6</h2>
<p>GTA 6 funciona a <strong>30 fps en todas las consolas</strong>, incluida PS5 Pro, sin modo rendimiento en el lanzamiento. Según un informe de Wccftech, la base es 1440p en PS5, PS5 Pro y Xbox Series X y 720p en Series S. Tienes la tabla completa en {pl("gta-6-30-fps-resolucion-consolas", "30 fps en todas las consolas")}.</p>
<h2 id="notas">Notas de GTA 6: 99 en Metacritic</h2>
<p>Las reseñas se publicaron el 18 de noviembre. GTA 6 marcaba un <strong>99 en Metacritic con 146 críticas</strong> y un 99 en OpenCritic, con dieces en IGN, GameSpot y Game Informer. Lo resumimos en {pl("gta-6-resenas-metacritic-99", "las reseñas de GTA 6")}.</p>
<h2 id="duracion">Cuánto dura GTA 6</h2>
<p>Rob Nelson, de Rockstar North, tardó <strong>unas 80 horas</strong> en terminar la historia con algunos objetivos opcionales. Completarlo todo lleva bastante más, y el juego no se acaba con los créditos. Lo explicamos en {pl("gta-6-cuanto-dura-80-horas", "cuánto dura GTA 6")}.</p>
<h2 id="historia">Historia y personajes de GTA 6</h2>
<p>Los protagonistas son {vl("jason-duval", "Jason Duval")}, un exmilitar que acaba trabajando para traficantes en los Cayos, y {vl("gta-6-lucia", "Lucia Caminos")}, recién salida de la Penitenciaría de Leonida. Es la primera vez que un GTA principal tiene protagonista femenina. El reparto confirmado incluye a {pjs}. Tienes sus fichas en la página de <a href="{rel}personajes/">personajes de GTA 6</a> y la trama de Megamundo en {pl("gta-6-megamundo-andres-de-leon-petra-navarro", "quién es quién en Megamundo")}.</p>
<h2 id="mapa">El mapa de GTA 6: Leonida y Vice City</h2>
<p>GTA 6 transcurre en <strong>Leonida</strong>, un estado ficticio inspirado en Florida. Su gran ciudad es Vice City, inspirada en Miami, que según Rob Nelson es el <strong>doble de grande que Los Santos</strong> de GTA V. Alrededor hay zonas como los Cayos, los pantanos de Grassrivers, Port Gellhorn, Ambrosia y Mount Kalaga. Míralo en {vl("mapa-leonida", "las 6 regiones de Leonida")}, {vl("grassrivers", "los pantanos de Grassrivers")} y {vl("vice-city-dia-noche", "Vice City de día y de noche")}.</p>
<h2 id="musica">Música y radios de GTA 6</h2>
<p>La banda sonora original es del dúo francés <strong>Justice</strong>, que estrenó «Flower in a Hurricane» con el tráiler de lanzamiento. Entre las emisoras destacan {vl("cocoteo-fm", "Cocoteo FM, la radio latina con Bad Bunny")} y {vl("por-que-afrobank", "AfroBank FM, la de música africana")}, y por primera vez la radio y los podcasts te siguen también a pie. Más en {pl("gta-6-banda-sonora-justice", "la banda sonora de Justice")}.</p>
<h2 id="trucos">Trucos de GTA 6</h2>
<p>GTA 6 tiene <strong>61 trucos</strong>, pero no funcionan hasta que terminas la historia: entonces aparece el apartado Trucos en el menú de Progreso, y cada código pide además un reto propio (medallas en campos de tiro, entrenamientos, desafíos…). Se introducen con el móvil del juego: arriba en la cruceta, mantén L1 + R1 (LB + RB en Xbox) y mete la combinación. Al usarlos se bloquean trofeos, logros y guardado durante esa sesión. Muchos códigos aún están por descubrir; tienes los confirmados en {pl("gta-6-trucos-como-desbloquear", "cómo desbloquear los trucos de GTA 6")} y, por nostalgia, {vl("35-trucos", "los 35 trucos de GTA V que podían volver")}.</p>
<h2 id="online">¿Y GTA Online?</h2>
<p>Rockstar no ha detallado el modo online de GTA 6. Take-Two ha confirmado que seguirá actualizando GTA Online después del lanzamiento.</p>
</div>
<p class="guia__faqlink">¿Tienes una duda concreta? Tienes todas las <a href="{rel}#faq">preguntas frecuentes sobre GTA 6</a> en la portada.</p>
<aside class="sources" aria-label="Fuentes"><h2>Fuentes</h2><ul>{src}</ul><p>Guía de fans, no oficial. La actualizamos cuando Rockstar confirma algo nuevo.</p></aside>
<p><a class="btn btn--yt" href="{SUB}" target="_blank" rel="noopener">{YT_ICON}<span>Más GTA 6 en YouTube</span></a></p>
</div></main>
"""
    d = os.path.join(OUT, "gta-6"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

def build_privacidad():
    rel = "../"; canon = SITE + "/privacidad/"
    title = "Política de privacidad y cookies | GTA MASTER"
    desc = "Qué datos trata GTA MASTER, qué servicios externos usa (YouTube y Disqus) y cómo funcionan sus cookies."
    schema = {"@context": "https://schema.org", "@graph": [ORG, {"@type": "WebPage", "@id": canon, "url": canon, "name": title, "inLanguage": "es"}]}
    h = head(title, desc, canon, SITE + "/assets/img/og-gta-master.jpg", rel, schema).replace(
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">', '<meta name="robots" content="noindex, follow">')
    body = f'''<main id="main"><section class="vhero bgpar">{bgimg("bahia-urbana", rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span>
<nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li aria-current="page">Privacidad</li></ol></nav>
<span class="eyebrow px">Transparencia</span><h1>Privacidad y cookies</h1><p class="lead">Última actualización: 18 de noviembre de 2026.</p></section>
<div class="post__wrap"><div class="post__body">
<h2>Quién está detrás</h2><p>GTA MASTER es una web de fans, no oficial, del canal de YouTube <a href="{CHANNEL}" target="_blank" rel="noopener">@GtaMaster2027</a>. Para cualquier consulta sobre tus datos puedes escribirnos a través del canal.</p>
<h2>Qué datos tratamos</h2><p>Esta web no tiene formularios, no pide registro y no usa cookies propias ni herramientas de analítica. Está alojada en GitHub Pages, que registra datos técnicos de cada visita (como la dirección IP) por seguridad, según su propia política de privacidad.</p>
<h2>Vídeos de YouTube</h2><p>Los vídeos de las noticias se muestran con el modo de privacidad mejorada de YouTube (youtube-nocookie.com). YouTube solo guarda información cuando le das al play. Los botones «Ver en YouTube» te llevan a youtube.com, que tiene su propia política de privacidad y cookies.</p>
<h2>Comentarios (Disqus)</h2><p>Los comentarios del blog funcionan con Disqus. No se carga nada de Disqus hasta que pulsas «Ver y escribir comentarios»: al hacerlo, aceptas conectar con Disqus, que puede usar cookies y tratar tus datos según su <a href="https://help.disqus.com/en/articles/1717103-disqus-privacy-policy" target="_blank" rel="noopener">política de privacidad</a>. Si comentas, lo que publiques (nombre, foto de perfil y mensaje) es público. Puedes borrar tus comentarios y tu cuenta desde Disqus.</p>
<h2>Normas de la comunidad</h2><ul><li>Sin spoilers sin avisar.</li><li>Respeto: nada de insultos, odio ni acoso.</li><li>Sin enlaces a filtraciones, piratería ni estafas.</li></ul><p>Podemos borrar los comentarios que no las cumplan y bloquear a quien las incumpla de forma repetida.</p>
<h2>Tus derechos</h2><p>Puedes pedir acceso, rectificación o supresión de tus datos escribiéndonos a través del canal o directamente a Disqus en lo que se refiere a los comentarios. También puedes reclamar ante la Agencia Española de Protección de Datos (aepd.es).</p>
</div></div></main>
'''
    d = os.path.join(OUT, "privacidad"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

def build_index():
    rel = "../"; canon = SITE + "/videos/"
    title = "Vídeos de GTA 6 en español | GTA MASTER"
    desc = "Todos los vídeos de GTA 6 de GTA MASTER: personajes, mapa de Leonida, Vice City, policía, curiosidades y detalles que no viste de GTA VI."
    schema = {"@context": "https://schema.org", "@graph": [ORG,
        {"@type": "CollectionPage", "@id": canon, "url": canon, "name": title, "description": desc, "inLanguage": "es", "isPartOf": {"@id": SITE + "/#web"}},
        {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": vurl(v)} for i, v in enumerate(V)]},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Vídeos de GTA 6", "item": canon}]}]}
    h = head(title, desc, canon, SITE + "/assets/img/og-gta-master.jpg", rel, schema)
    cats = []
    for c in ["Personajes", "Leonida", "Música", "Mecánicas", "Historia", "Curiosidades", "Análisis", "Shorts"]:
        vs = [v for v in V if v["cat"] == c]
        if vs: cats.append(f'<h2 class="h2" id="{unicodedata.normalize("NFKD", c).encode("ascii","ignore").decode().lower()}" style="font-size:clamp(2rem,1.4rem + 2.5vw,3.6rem);margin:3.5rem 0 1.5rem">GTA 6: {c.lower()}</h2><div class="vgrid">{"".join(vcard(v, rel) for v in vs)}</div>')
    body = f'''<main id="main"><section class="vhero bgpar">{bgimg("horizonte-neon-noche", rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span><nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li aria-current="page">Vídeos</li></ol></nav>
<h1>Vídeos de GTA 6 en español</h1><p class="lead">{len(V)} análisis de Grand Theft Auto VI ordenados por tema. Todos hechos con material oficial.</p></section>
<div class="wrap" style="padding-bottom:5rem">{"".join(cats)}</div></main>
'''
    d = os.path.join(OUT, "videos"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

def build_meta():
    today = datetime.now(MAD).strftime("%Y-%m-%d")
    urls = [(SITE + "/", today, "daily", "1.0"), (SITE + "/videos/", today, "daily", "0.9"), (SITE + "/blog/", today, "daily", "0.9"), (SITE + "/personajes/", today, "weekly", "0.9"), (SITE + "/gta-6/", today, "daily", "1.0")]
    urls += [(purl(p), p.get("updated", p["date"])[:10], "weekly", "0.8") for p in POSTS]
    vids = []
    for v in V:
        urls.append((vurl(v), v["up"][:10], "weekly", "0.8"))
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, lm, cf, pr in urls:
        v = next((x for x in V if vurl(x) == u), None)
        extra = ""
        if v:
            extra = (f'<image:image><image:loc>{SITE}/assets/thumbs/{v["id"]}.jpg</image:loc></image:image>'
                     f'<video:video><video:thumbnail_loc>{SITE}/assets/thumbs/{v["id"]}.jpg</video:thumbnail_loc><video:title>{esc(v["h1"])}</video:title>'
                     f'<video:description>{esc(v["desc"])}</video:description><video:player_loc>https://www.youtube.com/embed/{v["id"]}</video:player_loc>'
                     + (f'<video:duration>{v.get("len")}</video:duration>' if v.get("len") else '') + f'<video:publication_date>{v["up"]}</video:publication_date><video:family_friendly>yes</video:family_friendly></video:video>')
        xml.append(f"<url><loc>{u}</loc><lastmod>{lm}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority>{extra}</url>")
    xml.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(xml))
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /build.py\n\n# Buscadores de IA bienvenidos\nUser-agent: GPTBot\nAllow: /\nUser-agent: OAI-SearchBot\nAllow: /\nUser-agent: ChatGPT-User\nAllow: /\nUser-agent: ClaudeBot\nAllow: /\nUser-agent: Claude-SearchBot\nAllow: /\nUser-agent: PerplexityBot\nAllow: /\nUser-agent: Google-Extended\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
    llms = [f"# GTA MASTER", "", "> Web y canal de YouTube en español sobre Grand Theft Auto VI (GTA 6): detalles que no viste, personajes, mapa de Leonida, Vice City y curiosidades, analizados con material oficial de Rockstar Games. Web de fans, no oficial.", "",
            f"- Canal de YouTube: {CHANNEL}", f"- Lanzamiento de GTA 6: 19 de noviembre de 2026, PS5 y Xbox Series X|S", "", "## Vídeos"]
    llms += [f"- [{v['h1']}]({vurl(v)}): {v['desc']}" for v in V]
    llms += ["", "## Guía de GTA 6", f"- [GTA 6: todo lo que sabemos]({SITE}/gta-6/): fecha y hora de lanzamiento, precio y ediciones, PC, tamaño, fps, duración, mapa, personajes, música y trucos."]
    llms += ["", "## Personajes de GTA 6", f"- [Todos los personajes]({SITE}/personajes/): " + ", ".join(c["n"] for c in CAST)]
    llms += ["", "## Noticias (blog)"] + [f"- [{p['title']}]({purl(p)}): {p['desc']}" for p in POSTS[:20]]
    llms += ["", "## Páginas", f"- [Inicio]({SITE}/): resumen del canal, personajes, regiones de Leonida y preguntas frecuentes", f"- [Todos los vídeos]({SITE}/videos/)"]
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({"name": "GTA MASTER · GTA 6 en español", "short_name": "GTA MASTER", "lang": "es", "start_url": "/", "display": "standalone",
        "background_color": "#0D0A2C", "theme_color": "#0D0A2C", "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=1))
    open(os.path.join(OUT, "404.html"), "w").write(head("Página no encontrada | GTA MASTER", "Esta página no existe.", SITE + "/404.html", SITE + "/assets/img/og-gta-master.jpg", "/", {"@context": "https://schema.org", "@type": "WebPage", "name": "404"}).replace('content="index, follow', 'content="noindex, follow') +
        '<main id="main"><section class="vhero" style="min-height:70vh"><h1>Wasted. Esta página no existe.</h1><p class="lead">Vuelve a <a href="/">la portada</a> o mira <a href="/videos/">todos los vídeos de GTA 6</a>.</p></section></main>' + footer("/"))

# ---------- validación de datos (barrera contra contenido malicioso) ----------
# Las tareas automáticas escriben en data/videos.json y data/posts.json a partir
# de contenido de Internet. Si algo no cumple estas reglas, la web NO se genera.
def build_excluidos():
    """Vídeos retirados: su antigua URL redirige (noindex) para no dejar 404."""
    import shutil
    for e in EXCLUIDOS:
        if not re.fullmatch(r"[a-z0-9-]+", e.get("slug", "")): continue
        d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos", e["slug"])
        if os.path.isdir(d): shutil.rmtree(d)
        os.makedirs(d, exist_ok=True)
        dest = "/" + e.get("redirige", "videos/").lstrip("/")
        if not re.fullmatch(r"/[a-z0-9/-]*", dest): dest = "/videos/"
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(
            f'<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="robots" content="noindex">'
            f'<link rel="canonical" href="https://gtamaster.es{dest}"><meta http-equiv="refresh" content="0;url={dest}">'
            f'<title>Redirigiendo…</title></head><body><a href="{dest}">Ir a GTA MASTER</a></body></html>')


def validar():
    errores = []
    rx_slug = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    rx_id = re.compile(r"^[A-Za-z0-9_-]{11}$")
    rx_url = re.compile(r"^https?://[A-Za-z0-9.-]+(?:[/?#][^\s<>\"']*)?$")
    peligroso = re.compile(r"<\s*/?\s*(script|iframe|object|embed|style|form|meta|link|svg|base)\b|javascript\s*:|data\s*:\s*text/html|vbscript\s*:|\son[a-z]+\s*=", re.I)
    def texto(origen, campo, valor):
        if isinstance(valor, str) and peligroso.search(valor):
            errores.append(f"{origen}: contenido peligroso en «{campo}»")
        elif isinstance(valor, list):
            for x in valor: texto(origen, campo, x)
        elif isinstance(valor, dict):
            for k, x in valor.items(): texto(origen, f"{campo}.{k}", x)
    vistos = set()
    for v in V:
        o = f"vídeo {v.get('id')}"
        if not rx_id.match(str(v.get("id", ""))): errores.append(f"{o}: id de YouTube no válido")
        if not rx_slug.match(str(v.get("slug", ""))): errores.append(f"{o}: slug no válido")
        if v.get("slug") in vistos: errores.append(f"{o}: slug repetido")
        vistos.add(v.get("slug"))
        try: datetime.fromisoformat(v["up"])
        except Exception: errores.append(f"{o}: fecha no válida")
        for k, x in v.items(): texto(o, k, x)
    vistos = set()
    for p in POSTS:
        o = f"noticia {p.get('slug')}"
        if not rx_slug.match(str(p.get("slug", ""))): errores.append(f"{o}: slug no válido")
        if p.get("slug") in vistos: errores.append(f"{o}: slug repetido")
        vistos.add(p.get("slug"))
        try: datetime.fromisoformat(p["date"])
        except Exception: errores.append(f"{o}: fecha no válida")
        if p.get("fondo", "horizonte-neon-noche") not in BG: errores.append(f"{o}: fondo desconocido")
        for s_ in p.get("sources", []):
            if not rx_url.match(s_.get("url", "")): errores.append(f"{o}: URL de fuente no válida")
        for vid in re.findall(r"\{\{youtube:([^|}]+)", p.get("body", "")):
            if not rx_id.match(vid.strip()): errores.append(f"{o}: id de YouTube no válido en el texto")
        for k, x in p.items(): texto(o, k, x)
    if errores:
        raise SystemExit("VALIDACIÓN DE SEGURIDAD FALLIDA. La web no se ha generado:\n- " + "\n- ".join(errores))

if __name__ == "__main__":
    validar()
    build_home()
    for v in V: build_video(v)
    build_index(); build_posts(); build_blog_index(); build_personajes(); build_privacidad(); build_guia(); build_meta(); build_excluidos()
    print("OK:", len(V), "vídeos")
