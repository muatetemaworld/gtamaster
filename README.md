# GTA MASTER · web

Web de [GTA MASTER](https://www.youtube.com/@GtaMaster2027): GTA 6 en español.

- `data/videos.json`: los vídeos de la web. Se pueden editar a mano (títulos, textos, categoría).
- `scripts/actualizar_videos.py`: añade los vídeos nuevos del canal leyendo su feed público.
- `build.py`: genera todas las páginas, el sitemap y los datos estructurados.
- `.github/workflows/publicar.yml`: cada hora busca vídeos nuevos y, si los hay, regenera y publica la web. También publica con cada cambio en `main`.

Para cambiar el dominio, edita `SITE` en `build.py`.
