#!/usr/bin/env python3
"""Genera la web estática de GTA MASTER (home, páginas de vídeo, sitemap, robots, llms.txt).
Cambia SITE por tu dominio definitivo y vuelve a ejecutar: python3 build.py
"""
import json, os, random, html
from datetime import datetime
from zoneinfo import ZoneInfo

SITE = "https://www.gtamaster.es"          # <-- dominio definitivo
CHANNEL = "https://www.youtube.com/@GtaMaster2027"
CHANNEL_ID = "UCqBGUFmTDtnCzhu-uYCf7SA"
SUB = CHANNEL + "?sub_confirmation=1"
BRAND = "GTA MASTER"
LAUNCH = "2026-11-19T00:00:00+01:00"
OUT = os.path.dirname(os.path.abspath(__file__))
MAD = ZoneInfo("Europe/Madrid")
MESES = ["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]

V = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "videos.json"), encoding="utf-8"))
V.sort(key=lambda v: v["up"], reverse=True)
BY = {v["id"]: v for v in V}

def cap(s): return s[:1].upper()+s[1:]
def esc(s): return html.escape(s, quote=True)
def iso_dur(s): return f"PT{s//60}M{s%60}S" if s else None
def mmss(s): return f"{s//60}:{s%60:02d}" if s else ""
def fecha(v):
    dt = datetime.fromisoformat(v["up"]).astimezone(MAD)
    return f"{dt.day} {MESES[dt.month-1]} {dt.year}"
def vurl(v): return f"{SITE}/videos/{v['slug']}/"

FAQ = [
 ("¿Cuándo sale GTA 6?", "Grand Theft Auto VI sale el 19 de noviembre de 2026. Rockstar Games y Take-Two han confirmado esa fecha para PlayStation 5 y Xbox Series X|S."),
 ("¿GTA 6 sale en PC?", "No en el lanzamiento. Las plataformas anunciadas son PS5 y Xbox Series X|S; Rockstar no ha dado fecha para la versión de PC."),
 ("¿Quiénes son los protagonistas de GTA 6?", "Jason Duval y Lucia, una pareja que se mete en el mundo criminal de Leonida. En GTA MASTER tienes un vídeo dedicado a cada uno."),
 ("¿Dónde transcurre GTA 6?", "En Leonida, un estado ficticio inspirado en Florida. Su gran ciudad es Vice City, inspirada en Miami, y el mapa incluye zonas como los Cayos, los pantanos de Grassrivers, Port Gellhorn, Ambrosia y Mount Kalaga."),
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
 ("Jason Duval", "Protagonista. Exmilitar que acaba trabajando para traficantes en Leonida.", "BdIQoWrnTQc"),
 ("Lucia", "Protagonista. Su pasado incluye una etapa en prisión y una relación clave con Jason.", "q9amoxM3teA"),
 ("Cal Hampton", "Amigo de Jason en los Cayos y socio de Brian. Desconfía de todo.", "INVN9F4vSH8"),
]

# ---------- piezas comunes ----------
YT_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24 12a31 31 0 0 0-.5-5.8zM9.6 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M5 3l16 9-16 9z"/></svg>'

def head(title, desc, canon, img, rel, schema, extra=""):
    return f'''<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Barlow+Condensed:wght@600;700&family=Barlow:wght@400;600&family=Press+Start+2P&display=swap">
<link rel="stylesheet" href="{rel}assets/css/main.css">
{extra}<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>
<div class="progress" aria-hidden="true"></div>
<div class="grain" aria-hidden="true"></div>
<header class="nav">
  <a class="nav__brand" href="{rel or './'}" aria-label="GTA MASTER, inicio"><img src="{rel}assets/img/icon-192.png" width="46" height="46" alt=""><span>GTA MASTER</span></a>
  <nav aria-label="Principal"><ul class="nav__links">
    <li><a href="{rel}#videos">Vídeos</a></li><li><a href="{rel}#personajes">Personajes</a></li><li><a href="{rel}#leonida">Leonida</a></li><li><a href="{rel}#faq">Preguntas</a></li>
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
    <div><h2>Más análisis</h2><ul>{vids2}<li><a href="{rel}videos/">Todos los vídeos</a></li></ul></div>
  </div>
  <small>© <span data-year>2026</span> GTA MASTER · Web de fans, no oficial. Grand Theft Auto, GTA y Grand Theft Auto VI son marcas de Take-Two Interactive. Esta web no está afiliada a Rockstar Games ni a Take-Two. Las imágenes de los vídeos son miniaturas del canal GTA MASTER.</small>
</footer>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
<script src="{rel}assets/js/main.js" defer></script>
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
          "Curiosidades": "club-art-deco", "Historia": "boulevard-art-deco", "Análisis": "costa-urbana-pastel", "Shorts": "paseo-tropical"}

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
    title = "GTA 6 en Español: Secretos, Detalles y Análisis | GTA MASTER"
    desc = "GTA 6 en español: detalles que no viste, Jason y Lucia, el mapa de Leonida y Vice City, curiosidades y análisis de cada tráiler. Vídeos de GTA MASTER."
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
    cats = ["Todos"] + [c for c in ["Personajes", "Leonida", "Mecánicas", "Historia", "Curiosidades", "Análisis", "Shorts"] if any(v["cat"] == c for v in V)]
    chips = "".join(f'<button type="button" class="chip{" is-on" if c == "Todos" else ""}" data-filter="{c}" aria-pressed="{"true" if c == "Todos" else "false"}">{c}</button>' for c in cats)
    char_bg = {"BdIQoWrnTQc": "boulevard-art-deco", "q9amoxM3teA": "bahia-urbana", "INVN9F4vSH8": "lancha-tropical"}
    cast = "".join(f'''<article class="char">{bgimg(char_bg[i], cls="char__bg bgpar__img")}<span class="char__veil" aria-hidden="true"></span>
  <div class="char__inner wrap"><span class="char__name" aria-hidden="true">{esc(n.split()[0])}</span>
  <div class="char__media"><a href="videos/{BY[i]["slug"]}/">{img(BY[i], sizes="(max-width:820px) 92vw, 46vw").replace("{rel}", "")}</a></div>
  <div class="char__copy reveal"><span class="eyebrow px">Personaje 0{k+1}</span><h3>{esc(n)}</h3><p>{esc(t)}</p>
  <a class="pill pill--ghost" href="videos/{BY[i]["slug"]}/"><span>Ver el análisis</span>{ARROW}</a></div></div></article>''' for k, (n, t, i) in enumerate(CAST))
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
    <div class="hero__cta"><a class="btn btn--yt" href="{SUB}" target="_blank" rel="noopener">{YT_ICON}<span>Suscríbete gratis</span></a><a class="btn btn--ghost" href="#videos">Ver los vídeos</a></div>
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

<div class="stats" role="list">
  <div class="stat" role="listitem"><b data-count="{len(V)}">{len(V)}</b><span>Análisis publicados</span></div>
  <div class="stat" role="listitem"><b data-count="6">6</b><span>Regiones de Leonida</span></div>
  <div class="stat" role="listitem"><b data-count="2">2</b><span>Protagonistas</span></div>
  <div class="stat" role="listitem"><b>0</b><span>Filtraciones: solo material oficial</span></div>
</div>

<section class="banners wrap" aria-label="Destacados">
  {banner("club-art-deco", "Música · Cocoteo FM", "La radio latina de GTA&nbsp;6", "Bad Bunny y RaiNao presentan Cocoteo FM: bachata, merengue, dembow y reguetón para las noches de Vice City. Diez curiosidades en el vídeo.", "videos/" + coco["slug"] + "/", "Descubre más", side="left", eclass="is-cian")}
</section>

<section class="cast sec" id="personajes" aria-labelledby="t-cast">
  <div class="wrap"><span class="eyebrow px reveal">Quién es quién</span><h2 class="h2 reveal" id="t-cast">Personajes de <span class="grad-text">GTA 6</span></h2>
  <p class="lead reveal">Jason y Lucia llevan la historia, pero Leonida está llena de secundarios. Estos son los que ya hemos analizado.</p></div>
  {cast}
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
  </article>
  <aside aria-label="Vídeos relacionados"><h2>Sigue viendo</h2>{rels}
    <p style="margin-top:1.4rem"><a class="link-arrow" href="{rel}videos/">Todos los vídeos de GTA 6 →</a></p></aside>
</div>
</main>
'''
    d = os.path.join(OUT, "videos", v["slug"]); os.makedirs(d, exist_ok=True)
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
    for c in ["Personajes", "Leonida", "Mecánicas", "Historia", "Curiosidades", "Análisis", "Shorts"]:
        vs = [v for v in V if v["cat"] == c]
        if vs: cats.append(f'<h2 class="h2" style="font-size:clamp(2rem,1.4rem + 2.5vw,3.6rem);margin:3.5rem 0 1.5rem">GTA 6: {c.lower()}</h2><div class="vgrid">{"".join(vcard(v, rel) for v in vs)}</div>')
    body = f'''<main id="main"><section class="vhero bgpar">{bgimg("horizonte-neon-noche", rel=rel, eager=True)}<span class="bgpar__veil bgpar__veil--vhero" aria-hidden="true"></span><nav class="crumbs" aria-label="Migas de pan"><ol><li><a href="{rel}">Inicio</a></li><li aria-current="page">Vídeos</li></ol></nav>
<h1>Vídeos de GTA 6 en español</h1><p class="lead">{len(V)} análisis de Grand Theft Auto VI ordenados por tema. Todos hechos con material oficial.</p></section>
<div class="wrap" style="padding-bottom:5rem">{"".join(cats)}</div></main>
'''
    d = os.path.join(OUT, "videos"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(h + body + footer(rel))

def build_meta():
    today = datetime.now(MAD).strftime("%Y-%m-%d")
    urls = [(SITE + "/", today, "daily", "1.0"), (SITE + "/videos/", today, "daily", "0.9")]
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
    llms += ["", "## Páginas", f"- [Inicio]({SITE}/): resumen del canal, personajes, regiones de Leonida y preguntas frecuentes", f"- [Todos los vídeos]({SITE}/videos/)"]
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(llms) + "\n")
    open(os.path.join(OUT, "site.webmanifest"), "w").write(json.dumps({"name": "GTA MASTER · GTA 6 en español", "short_name": "GTA MASTER", "lang": "es", "start_url": "/", "display": "standalone",
        "background_color": "#0D0A2C", "theme_color": "#0D0A2C", "icons": [{"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png"}, {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=1))
    open(os.path.join(OUT, "404.html"), "w").write(head("Página no encontrada | GTA MASTER", "Esta página no existe.", SITE + "/404.html", SITE + "/assets/img/og-gta-master.jpg", "/", {"@context": "https://schema.org", "@type": "WebPage", "name": "404"}).replace('content="index, follow', 'content="noindex, follow') +
        '<main id="main"><section class="vhero" style="min-height:70vh"><h1>Wasted. Esta página no existe.</h1><p class="lead">Vuelve a <a href="/">la portada</a> o mira <a href="/videos/">todos los vídeos de GTA 6</a>.</p></section></main>' + footer("/"))

if __name__ == "__main__":
    build_home()
    for v in V: build_video(v)
    build_index(); build_meta()
    print("OK:", len(V), "vídeos")
