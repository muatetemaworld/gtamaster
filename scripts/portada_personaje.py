#!/usr/bin/env python3
"""Portada de personaje con el estilo de las miniaturas de GTA MASTER.

No dibuja al personaje (es propiedad de Rockstar): usa un fondo ilustrado
de la web, recortado a 16:9 sin deformar, y el nombre en grande con el
degradado oro > rosa > magenta y el contorno violeta de las miniaturas.

Uso:
  python3 scripts/portada_personaje.py --slug raul-bautista \
      --nombre "Raul Bautista" --lema "Atracador de bancos" --fondo costa-urbana-pastel
Salida: assets/personajes/<slug>.jpg (1280x720), <slug>.webp, <slug>-640.webp
"""
import argparse, os
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
W, H = 1280, 720


def cover_crop(im, w, h, fx=0.5, fy=0.5):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = round((im.width - w) * fx); y = round((im.height - h) * fy)
    return im.crop((x, y, x + w, y + h))


def gradient(w, h, stops):
    g = Image.new("RGBA", (w, h)); d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1) * (len(stops) - 1); i = min(int(t), len(stops) - 2); k = t - i
        c = tuple(int(stops[i][j] + (stops[i + 1][j] - stops[i][j]) * k) for j in range(3))
        d.line([(0, y), (w, y)], fill=c + (255,))
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--nombre", required=True)
    ap.add_argument("--lema", default="")
    ap.add_argument("--fondo", default="horizonte-neon-noche")
    ap.add_argument("--imagen", help="ilustración propia (por ejemplo, generada con IA)")
    ap.add_argument("--fx", type=float, default=0.55)
    a = ap.parse_args()

    src = a.imagen or os.path.join(ROOT, "assets", "bg", f"{a.fondo}-1600.webp")
    base = cover_crop(Image.open(src).convert("RGB"), W, H, fx=a.fx).convert("RGBA")
    # Tinte violeta-rosa de las miniaturas y velado a la izquierda
    tint = Image.new("RGBA", (W, H), (120, 40, 150, 70)); base.alpha_composite(tint)
    shade = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(shade)
    for x in range(W):
        d.line([(x, 0), (x, H)], fill=(20, 8, 46, int(200 * max(0, 1 - x / 980) ** 1.3)))
    base.alpha_composite(shade)

    # Nombre: una palabra por línea, lo más grande posible
    words = a.nombre.upper().replace("-", "- ").split()
    lines = []
    for w_ in words:
        if lines and len(lines[-1]) + len(w_) <= 7: lines[-1] += " " + w_
        else: lines.append(w_)
    lines = [l.replace("- ", "-") for l in lines]
    fp = os.path.join(FONTS, "Anton.ttf"); max_w, max_h = 820, 470
    for size in range(260, 60, -6):
        f = ImageFont.truetype(fp, size); lh = int(size * 1.08)
        if max(f.getlength(l) for l in lines) <= max_w and lh * len(lines) <= max_h: break
    tw = int(max(f.getlength(l) for l in lines)); th = lh * len(lines) + 30
    mask = Image.new("L", (tw + 40, th), 0); md = ImageDraw.Draw(mask)
    for n, l in enumerate(lines):
        md.text((20, n * lh), l, font=f, fill=255)
    x0, y0 = 64, max(150, (H - th) // 2 + 30)
    # Contorno violeta grueso + resplandor rosa
    outline = mask.filter(ImageFilter.MaxFilter(15))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow.paste(Image.new("RGBA", mask.size, (255, 70, 200, 230)), (x0, y0), outline)
    base.alpha_composite(glow.filter(ImageFilter.GaussianBlur(18)))
    ol = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ol.paste(Image.new("RGBA", mask.size, (52, 14, 92, 255)), (x0, y0), outline)
    base.alpha_composite(ol)
    grad = gradient(mask.size[0], mask.size[1], [(255, 236, 120), (255, 176, 92), (255, 92, 168), (196, 62, 230)])
    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fill.paste(grad, (x0, y0), mask)
    base.alpha_composite(fill)
    # Brillo superior blanco en las letras
    hl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    inner = ImageChops.subtract(mask, mask.filter(ImageFilter.MinFilter(5)).transform(mask.size, Image.AFFINE, (1, 0, 0, 0, 1, 4)))
    hl.paste(Image.new("RGBA", mask.size, (255, 255, 255, 120)), (x0, y0), inner)
    base.alpha_composite(hl)

    draw = ImageDraw.Draw(base)
    if a.lema:
        bc = ImageFont.truetype(os.path.join(FONTS, "BarlowCondensed.ttf"), 46)
        ly = y0 - 66
        lw = draw.textlength(a.lema.upper(), font=bc)
        draw.rounded_rectangle([x0 + 14, ly, x0 + 14 + lw + 40, ly + 58], radius=12, fill=(20, 8, 46, 210), outline=(255, 210, 90), width=3)
        draw.text((x0 + 34, ly + 4), a.lema.upper(), font=bc, fill=(255, 243, 209))
    # Insignia del canal
    icon_p = os.path.join(ROOT, "assets", "img", "icon-192.png")
    if os.path.exists(icon_p):
        icon = Image.open(icon_p).convert("RGBA").resize((84, 84), Image.LANCZOS)
        base.alpha_composite(icon, (W - 84 - 40, 36))
    stops = [(60, 208, 226), (232, 44, 122), (255, 122, 89), (255, 200, 62)]
    for x in range(W):
        t = x / (W - 1) * (len(stops) - 1); i = min(int(t), len(stops) - 2); k = t - i
        draw.line([(x, H - 10), (x, H)], fill=tuple(int(stops[i][j] + (stops[i + 1][j] - stops[i][j]) * k) for j in range(3)))

    out = os.path.join(ROOT, "assets", "personajes"); os.makedirs(out, exist_ok=True)
    rgb = base.convert("RGB")
    rgb.save(os.path.join(out, f"{a.slug}.jpg"), "JPEG", quality=86, optimize=True, progressive=True)
    rgb.save(os.path.join(out, f"{a.slug}.webp"), "WEBP", quality=80, method=6)
    rgb.resize((640, 360), Image.LANCZOS).save(os.path.join(out, f"{a.slug}-640.webp"), "WEBP", quality=78, method=6)
    print("Portada:", f"assets/personajes/{a.slug}.jpg")


if __name__ == "__main__":
    main()
