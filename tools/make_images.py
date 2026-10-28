"""Иконки и картинка для соцсетей: public/favicon.svg, apple-touch-icon.png, og.png.
og.png рисуется через Microsoft Edge в режиме без окна (нужны шрифты из fetch_assets.py).

Запуск:  python tools/make_images.py
"""
import subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw

PUB = Path(__file__).resolve().parent.parent / "public"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
INK, PAPER, SIGNAL, STONE = "#0F1B2D", "#FBF8F3", "#FF5B1F", "#F2ECE2"

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 34 34"><rect width="34" height="34" rx="10" fill="#0F1B2D"/>'
           '<circle cx="10" cy="23" r="3.2" fill="#FBF8F3"/><circle cx="24" cy="11" r="3.2" fill="#FF5B1F"/>'
           '<path d="M12.5 21 Q 14 12 21.5 12.5" stroke="#FBF8F3" stroke-width="2" fill="none" stroke-dasharray="2.5 2.5"/></svg>\n')


def touch_icon():
    s = 180 * 4
    im = Image.new("RGB", (s, s), INK)
    d = ImageDraw.Draw(im)
    k = s / 34
    for i in range(0, 9):
        t = i / 8
        # пунктирная дуга (квадратичная кривая) между точками
        x = (1 - t) ** 2 * 12.5 + 2 * (1 - t) * t * 14 + t ** 2 * 21.5
        y = (1 - t) ** 2 * 21 + 2 * (1 - t) * t * 12 + t ** 2 * 12.5
        if i % 2 == 0:
            d.ellipse([(x - 1) * k, (y - 1) * k, (x + 1) * k, (y + 1) * k], fill=PAPER)
    d.ellipse([(10 - 3.6) * k, (23 - 3.6) * k, (10 + 3.6) * k, (23 + 3.6) * k], fill=PAPER)
    d.ellipse([(24 - 3.6) * k, (11 - 3.6) * k, (24 + 3.6) * k, (11 + 3.6) * k], fill=SIGNAL)
    im.resize((180, 180), Image.LANCZOS).save(PUB / "apple-touch-icon.png")


OG = """<!doctype html><html lang="ru"><head><meta charset="utf-8">
<link rel="stylesheet" href="{fonts}">
<style>
*{{margin:0;box-sizing:border-box}}
body{{width:1200px;height:630px;background:#F2ECE2;font-family:Onest,sans-serif;color:#0F1B2D;position:relative;overflow:hidden}}
.l{{position:absolute;left:72px;top:64px;display:flex;align-items:center;gap:16px;font:800 34px Unbounded}}
h1{{position:absolute;left:72px;top:160px;font:800 64px/1.04 Unbounded;letter-spacing:-.03em;width:680px}}
h1 span{{color:#E04A12;display:block}}
p{{position:absolute;left:72px;bottom:64px;font:500 26px Onest;color:#4A5568}}
.t{{position:absolute;right:70px;top:120px;width:330px;background:#FBF8F3;border-radius:28px;transform:rotate(4deg);box-shadow:0 40px 80px -40px rgba(15,27,45,.55);overflow:hidden}}
.th{{background:#0F1B2D;color:#FBF8F3;font:700 17px Unbounded;padding:20px 24px;letter-spacing:.06em}}
.tr{{padding:26px 24px;display:flex;justify-content:space-between;align-items:center;font:800 32px Unbounded}}
.tr i{{color:#FF5B1F;font-style:normal}}
.b{{margin:0 24px 26px;height:60px;background:repeating-linear-gradient(90deg,#0F1B2D 0 3px,transparent 3px 7px,#0F1B2D 7px 9px,transparent 9px 13px)}}
.d{{margin:0 24px 22px;border-top:2px dashed rgba(15,27,45,.2);padding-top:18px;font:600 20px Onest}}
</style></head><body>
<div class="l">{logo}<span>DEHR</span></div>
<h1>Работа в Израиле. <span>Без обходных путей.</span></h1>
<div class="t"><div class="th">DEHR · WORK PASS</div><div class="tr"><span>Ваш<br>город</span><i>→</i><span>TLV</span></div>
<div class="d">Жильё · подвозка · документы</div><div class="b"></div></div>
<p>dehr.ltd · Лицензированное кадровое агентство · RU · HE · EN</p>
</body></html>"""


def og():
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "og.html"
        logo = FAVICON.replace('viewBox="0 0 34 34"', 'viewBox="0 0 34 34" width="52" height="52"')
        page.write_text(OG.format(fonts=(PUB / "assets/fonts/fonts.css").as_uri(), logo=logo), encoding="utf-8")
        shot = Path(tmp) / "og.png"
        subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={tmp}/prof",
                        "--allow-file-access-from-files", "--virtual-time-budget=4000", "--window-size=1200,630",
                        f"--screenshot={shot}", page.as_uri()], check=True, capture_output=True)
        Image.open(shot).convert("RGB").crop((0, 0, 1200, 630)).save(PUB / "og.png", optimize=True)


if __name__ == "__main__":
    (PUB / "favicon.svg").write_text(FAVICON, encoding="utf-8")
    touch_icon()
    og()
    print("images: ok")
