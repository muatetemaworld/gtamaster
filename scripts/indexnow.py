#!/usr/bin/env python3
"""Avisa a los buscadores (IndexNow: Bing, Yandex, Seznam, Naver) de las URL del sitemap.
Uso: python3 scripts/indexnow.py [url ...]   (sin argumentos envía todas las del sitemap)"""
import json, re, sys, os, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = open(os.path.join(ROOT, "build.py"), encoding="utf-8").read()
KEY = re.search(r'INDEXNOW = "([0-9a-f]+)"', src).group(1)
urls = sys.argv[1:] or re.findall(r"<loc>(https://gtamaster\.es/[^<]*)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())
body = json.dumps({"host": "gtamaster.es", "key": KEY, "keyLocation": f"https://gtamaster.es/{KEY}.txt", "urlList": urls[:10000]}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r: print("IndexNow:", r.status, len(urls), "URL")
except urllib.error.HTTPError as e: print("IndexNow:", e.code, e.read()[:200])
