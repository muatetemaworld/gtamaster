#!/usr/bin/env python3
"""Añade a la web los vídeos nuevos del canal de YouTube de GTA MASTER.

Lee el feed público del canal, detecta los vídeos que aún no están en
data/videos.json, descarga sus miniaturas, genera sus textos a partir del
título y la descripción de YouTube y los guarda. Después hay que ejecutar
build.py para regenerar las páginas (el flujo de GitHub lo hace solo).

Uso: python3 scripts/actualizar_videos.py
"""
import json, os, re, sys, unicodedata, urllib.request, xml.etree.ElementTree as ET
from io import BytesIO

CHANNEL_ID = "UCqBGUFmTDtnCzhu-uYCf7SA"
FEED = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "videos.json")
THUMBS = os.path.join(ROOT, "assets", "thumbs")
UA = {"User-Agent": "Mozilla/5.0 (GTA MASTER web updater)", "Accept-Language": "es-ES,es;q=0.9"}
NS = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015", "media": "http://search.yahoo.com/mrss/"}

CATS = [  # primera coincidencia gana
    ("Personajes", ["jason", "lucia", "lucía", "cal hampton", "brian", "personaje", "protagonista", "boobie", "dre'quan", "real dimez"]),
    ("Leonida", ["vice city", "leonida", "mapa", "región", "regiones", "cayos", "keys", "pantano", "grassrivers", "ambrosia", "kalaga", "gellhorn", "everglades"]),
    ("Historia", ["historia", "misión", "mision", "atraco", "robo", "golpe", "trama"]),
    ("Mecánicas", ["policía", "policia", "armas", "coches", "vehículo", "mecánica", "actividad", "podrás hacer", "trucos", "dinero", "online"]),
    ("Curiosidades", ["curiosidad", "easter", "anuncio", "radio", "secreto", "sabías", "detalle"]),
]


def get(url, binary=False, timeout=30):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", "replace")


def clean_title(t):
    t = re.sub(r"#\S+", "", t)                                   # hashtags
    t = "".join(ch for ch in t if unicodedata.category(ch) not in ("So", "Sk", "Cs") and ch not in "️‍")
    t = re.sub(r"\s*\|\s*$", "", re.sub(r"\s+", " ", t)).strip(" |-·")
    return t


def slugify(t):
    t = unicodedata.normalize("NFKD", t.lower()).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    words = t.split("-")
    out = []
    for w in words:  # máx. ~60 caracteres
        if len("-".join(out + [w])) > 60: break
        out.append(w)
    return "-".join(out) or "video"


def sentence_cut(text, limit=155):
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit: return text
    cut = text[:limit]
    for sep in (". ", "? ", "! "):
        i = cut.rfind(sep)
        if i > 80: return cut[: i + 1]
    return cut[: cut.rfind(" ")].rstrip(",;:") + "…"


def category(text):
    low = text.lower()
    for cat, words in CATS:
        if any(w in low for w in words): return cat
    return "Análisis"


def duration(vid):
    try:
        h = get(f"https://www.youtube.com/watch?v={vid}&hl=es")
        m = re.search(r'"lengthSeconds":"(\d+)"', h)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def is_short(vid):
    try:
        req = urllib.request.Request(f"https://www.youtube.com/shorts/{vid}", headers=UA, method="HEAD")
        opener = urllib.request.build_opener(NoRedirect)
        r = opener.open(req, timeout=15)
        return r.status == 200
    except Exception:
        return False


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k): return None


def thumbs(vid):
    from PIL import Image
    raw = None
    for name in ("maxresdefault", "sddefault", "hqdefault"):
        try:
            raw = get(f"https://i.ytimg.com/vi/{vid}/{name}.jpg", binary=True)
            if len(raw) > 2000: break
        except Exception:
            continue
    if not raw: raise RuntimeError("sin miniatura")
    im = Image.open(BytesIO(raw)).convert("RGB")
    W, H = im.size
    if abs(W / H - 16 / 9) > 0.02:  # recorta bandas negras sin deformar
        h = round(W * 9 / 16); y = (H - h) // 2; im = im.crop((0, y, W, y + h))
    big = im.resize((1280, 720), Image.LANCZOS) if im.width < 1280 else im.resize((1280, 720), Image.LANCZOS)
    big.save(os.path.join(THUMBS, f"{vid}.jpg"), "JPEG", quality=82, optimize=True, progressive=True)
    big.save(os.path.join(THUMBS, f"{vid}.webp"), "WEBP", quality=78, method=6)
    big.resize((640, 360), Image.LANCZOS).save(os.path.join(THUMBS, f"{vid}-640.webp"), "WEBP", quality=76, method=6)
    cw = int(720 * 0.75)
    big.crop((1280 - cw, 0, 1280, 720)).save(os.path.join(THUMBS, f"{vid}-v.webp"), "WEBP", quality=80, method=6)


def main():
    videos = json.load(open(DATA, encoding="utf-8"))
    known = {v["id"] for v in videos}
    slugs = {v["slug"] for v in videos}
    root = ET.fromstring(get(FEED))
    nuevos = []
    for e in root.findall("a:entry", NS):
        vid = e.find("yt:videoId", NS).text
        if vid in known: continue
        raw_title = e.find("a:title", NS).text or ""
        desc = (e.find("media:group/media:description", NS).text or "").strip()
        title = clean_title(raw_title)
        if re.match(r"^gta\s*(vi|6)\b", title, re.I):
            h1 = re.sub(r"^gta\s*(vi|6)\s*[:\-|]?\s*", "GTA 6: ", title, count=1, flags=re.I)
        elif re.search(r"\bgta\s*(6|vi)\b", title, re.I):
            h1 = title
        else:
            h1 = f"GTA 6: {title}"
        body = re.split(r"\n\s*\n?\s*Suscr[ií]bete", desc, flags=re.I)[0]
        paras = [re.sub(r"\s+", " ", p).strip() for p in body.split("\n") if p.strip() and not p.strip().startswith("#")]
        short = is_short(vid)
        slug = base = slugify(h1)
        n = 2
        while slug in slugs: slug = f"{base}-{n}"; n += 1
        slugs.add(slug)
        title_seo = h1 if len(h1) <= 60 else h1[:57].rsplit(" ", 1)[0] + "…"
        cat = "Shorts" if short else category(raw_title + " " + desc[:300])
        v = {
            "id": vid, "up": e.find("a:published", NS).text, "len": duration(vid), "cat": cat, "slug": slug,
            "yt": raw_title.strip(), "h1": h1, "title": title_seo,
            "kw": [k for k in dict.fromkeys(["gta 6", "gta vi", cat.lower() if cat != "Análisis" else "gta 6 analisis"])],
            "desc": sentence_cut(paras[0] if paras else h1),
            "intro": paras[:3] if paras else [h1],
            "points": [], "auto": True,
        }
        try:
            thumbs(vid)
        except Exception as ex:
            print(f"! {vid}: sin miniatura ({ex}), se omite por ahora", file=sys.stderr)
            continue
        nuevos.append(v)
        print(f"+ {vid}  {h1}  [{cat}]")
    if nuevos:
        videos.extend(nuevos)
        json.dump(videos, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Vídeos nuevos: {len(nuevos)} · total: {len(videos)}")
    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f: f.write(f"nuevos={len(nuevos)}\n")


if __name__ == "__main__":
    main()
