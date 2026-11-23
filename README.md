# GTA MASTER · web

Web de [GTA MASTER](https://www.youtube.com/@GtaMaster2027): GTA 6 en español.

- `data/videos.json`: los vídeos de la web. Se pueden editar a mano (títulos, textos, categoría).
- `scripts/actualizar_videos.py`: añade los vídeos nuevos del canal leyendo su feed público.
- `build.py`: genera todas las páginas, el sitemap y los datos estructurados.
- `.github/workflows/publicar.yml`: cada hora busca vídeos nuevos y, si los hay, regenera y publica la web. También publica con cada cambio en `main`.

Para cambiar el dominio, edita `SITE` en `build.py`.

## Portadas del blog (norma, 23/11/2026)

- Toda portada se genera con ChatGPT, va acorde a la noticia y lleva **uno o más personajes** inventados (no de Rockstar ni personas reales), cada vez de etnia, edad y ropa distintas.
- El titular de 1–3 palabras va dentro de la ilustración, en tipografía cartel GTA 6. La esquina superior izquierda queda libre.
- Se monta con `python3 scripts/portada.py --slug <slug> --titulo "<titular>" --etiqueta <categoría> --imagen <png> --sin-titulo`, que añade la insignia, la etiqueta y la franja sin estirar.
- Ya no se usan los fondos de `assets/bg` sin personajes como portada.
