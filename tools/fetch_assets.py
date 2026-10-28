"""Один раз скачивает в public/ то, что сайт отдаёт со своего домена:
шрифты (Google Fonts, лицензия OFL) и MapLibre GL JS (BSD-3). Так сайт не зависит от чужих CDN
и не передаёт IP посетителей в Google Fonts.

Запуск:  python tools/fetch_assets.py
"""
import re, urllib.request
from pathlib import Path

PUB = Path(__file__).resolve().parent.parent / "public"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
FONTS = ("https://fonts.googleapis.com/css2?family=Unbounded:wght@500;700;800"
         "&family=Onest:wght@400;500;600&family=Secular+One&family=Heebo:wght@400;500;700&display=swap")
MAPLIBRE = "4.7.1"
# только нужные алфавиты: латиница, кириллица, иврит
KEEP = {"latin", "latin-ext", "cyrillic", "cyrillic-ext", "hebrew"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fonts():
    out = PUB / "assets" / "fonts"
    out.mkdir(parents=True, exist_ok=True)
    css = get(FONTS).decode()
    blocks = re.findall(r"/\* ([\w-]+) \*/\s*(@font-face\s*\{[^}]+\})", css)
    kept, n = [], 0
    for subset, block in blocks:
        if subset not in KEEP:
            continue
        fam = re.search(r"font-family:\s*'([^']+)'", block).group(1).replace(" ", "")
        wt = re.search(r"font-weight:\s*(\d+)", block).group(1)
        src = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
        name = f"{fam}-{wt}-{subset}.woff2"
        (out / name).write_bytes(get(src))
        kept.append(f"/* {subset} */\n" + block.replace(src, name))
        n += 1
    (out / "fonts.css").write_text("\n".join(kept) + "\n", encoding="utf-8")
    print(f"fonts: {n} files")


def maplibre():
    out = PUB / "assets" / "vendor"
    out.mkdir(parents=True, exist_ok=True)
    for f in ("maplibre-gl.js", "maplibre-gl.css"):
        (out / f).write_bytes(get(f"https://unpkg.com/maplibre-gl@{MAPLIBRE}/dist/{f}"))
    (out / "MAPLIBRE-LICENSE.txt").write_bytes(get(f"https://unpkg.com/maplibre-gl@{MAPLIBRE}/LICENSE.txt"))
    print(f"maplibre {MAPLIBRE}: ok")


if __name__ == "__main__":
    fonts()
    maplibre()
