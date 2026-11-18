#!/usr/bin/env python3
"""Genera la portada de una noticia del blog con el estilo de GTA MASTER.

Usa los fondos ilustrados de la web (mismo estilo de dibujo que las miniaturas
del canal), los recorta a 16:9 sin deformarlos y les añade el titular con la
tipografía y los colores de la marca.

Uso:
  python3 scripts/portada.py --slug mi-noticia --titulo "Titular" \
      --etiqueta "Noticias" --fondo estadio-tropical [--imagen ruta.png]

--imagen permite usar una ilustración propia (por ejemplo, generada con IA)
en lugar de un fondo de la web; también se recorta sin deformar.
Salida: assets/blog/<slug>.jpg (1280x720), <slug>.webp y <slug>-640.webp
"""
import argparse, os, textwrap
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
W, H = 1280, 720
FONDOS = ["costa-urbana-pastel", "horizonte-neon-noche", "atardecer-neon-mar", "club-art-deco",
          "boulevard-art-deco", "bahia-urbana", "lancha-tropical", "everglades-aerodeslizador",
          "estadio-tropical", "humedales-tropicales", "paseo-tropical"]


def cover_crop(im, w, h, fx=0.5, fy=0.5):
    """Escala para cubrir y recorta: nunca estira ni deforma."""
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def fit_title(draw, text, font_path, max_w, max_lines, start=118, min_size=54):
    text = text.upper()
    for size in range(start, min_size - 1, -4):
        f = ImageFont.truetype(font_path, size)
        avg = f.getlength("ABCDEFGHIJKLMNOPQRSTUVWXYZ") / 26
        width_chars = max(8, int(max_w / avg))
        lines = textwrap.wrap(text, width=width_chars)
        if len(lines) <= max_lines and all(draw.textlength(l, font=f) <= max_w for l in lines):
            return f, lines
    f = ImageFont.truetype(font_path, min_size)
    return f, textwrap.wrap(text, width=int(max_w / (f.getlength("M") * .8)))[:max_lines]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--titulo", required=True)
    ap.add_argument("--etiqueta", default="Noticias")
    ap.add_argument("--fondo", default="horizonte-neon-noche", choices=FONDOS)
    ap.add_argument("--imagen", help="ilustración propia opcional")
    ap.add_argument("--fx", type=float, default=0.62)
    a = ap.parse_args()

    src = a.imagen or os.path.join(ROOT, "assets", "bg", f"{a.fondo}-1600.webp")
    base = cover_crop(Image.open(src).convert("RGB"), W, H, fx=a.fx).convert("RGBA")

    # Velado para que el titular se lea: oscuro a la izquierda y abajo
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(shade)
    for x in range(W):
        d.line([(x, 0), (x, H)], fill=(13, 10, 44, int(215 * max(0, 1 - x / 860) ** 1.2)))
    for y in range(H):
        a_ = int(170 * max(0, (y - H * 0.45) / (H * 0.55)) ** 1.5)
        d.line([(0, y), (W, y)], fill=(13, 10, 44, a_))
    base.alpha_composite(shade)

    draw = ImageDraw.Draw(base)
    # Franja de marca (degradado cian > magenta > oro)
    stops = [(60, 208, 226), (232, 44, 122), (255, 122, 89), (255, 200, 62)]
    for x in range(W):
        t = x / (W - 1) * (len(stops) - 1); i = min(int(t), len(stops) - 2); k = t - i
        c = tuple(int(stops[i][j] + (stops[i + 1][j] - stops[i][j]) * k) for j in range(3))
        draw.line([(x, H - 10), (x, H)], fill=c)

    # Insignia del canal + etiqueta en píxel
    icon_p = os.path.join(ROOT, "assets", "img", "icon-192.png")
    if os.path.exists(icon_p):
        icon = Image.open(icon_p).convert("RGBA").resize((92, 92), Image.LANCZOS)
        base.alpha_composite(icon, (56, 50))
    px = ImageFont.truetype(os.path.join(FONTS, "PressStart2P.ttf"), 20)
    label = f"GTA MASTER · {a.etiqueta.upper()}"
    lw = draw.textlength(label, font=px)
    draw.rounded_rectangle([166, 76, 166 + lw + 36, 76 + 44], radius=10, fill=(232, 44, 122, 235))
    draw.text((184, 87), label, font=px, fill=(255, 255, 255))

    # Titular
    font, lines = fit_title(draw, a.titulo, os.path.join(FONTS, "Anton.ttf"), max_w=760, max_lines=4)
    lh = int(font.size * 1.13)
    y0 = H - 70 - lh * len(lines)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
    for n, l in enumerate(lines):
        gd.text((60, y0 + n * lh), l, font=font, fill=(0, 0, 0, 200))
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    for n, l in enumerate(lines):
        draw.text((60, y0 + n * lh), l, font=font, fill=(255, 243, 209))

    out = os.path.join(ROOT, "assets", "blog"); os.makedirs(out, exist_ok=True)
    rgb = base.convert("RGB")
    rgb.save(os.path.join(out, f"{a.slug}.jpg"), "JPEG", quality=86, optimize=True, progressive=True)
    rgb.save(os.path.join(out, f"{a.slug}.webp"), "WEBP", quality=80, method=6)
    rgb.resize((640, 360), Image.LANCZOS).save(os.path.join(out, f"{a.slug}-640.webp"), "WEBP", quality=78, method=6)
    print("Portada:", os.path.join("assets", "blog", f"{a.slug}.jpg"))


if __name__ == "__main__":
    main()
