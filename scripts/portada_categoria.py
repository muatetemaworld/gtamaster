"""Portada de categoría (ChatGPT, vertical 3:4) -> assets/cats/<slug>.webp (720x960) y .jpg.
Recorte centrado a 3:4 sin estirar."""
import sys, os
from PIL import Image
src, slug = sys.argv[1], sys.argv[2]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
im = Image.open(src).convert("RGB")
w, h = im.size
tw = min(w, round(h * 3 / 4)); th = round(tw * 4 / 3)
x0 = (w - tw) // 2; y0 = max(0, (h - th) // 2)
im = im.crop((x0, y0, x0 + tw, y0 + th)).resize((720, 960), Image.LANCZOS)
d = os.path.join(root, "assets", "cats"); os.makedirs(d, exist_ok=True)
im.save(os.path.join(d, slug + ".webp"), "WEBP", quality=82, method=6)
im.save(os.path.join(d, slug + ".jpg"), "JPEG", quality=86, optimize=True, progressive=True)
print("Portada de categoría:", slug, im.size)
