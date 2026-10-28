"""Сборка сайта DEHR Ltd: src/ + public/ -> docs/.

Запуск:  python build.py
GitHub Pages публикует docs/ из ветки main.
"""
import hashlib, html, json, re, shutil, sys
sys.stdout.reconfigure(encoding="utf-8")
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC, PUB, DIST = ROOT / "src", ROOT / "public", ROOT / "docs"   # GitHub Pages публикует папку docs/

# ---- настройки компании ----
SITE = "https://dehr.ltd"
PHONE, PHONE_TEL, WA = "+972 54-873-2037", "+972548732037", "972548732037"
TELEGRAM = "dehrcompany"
YANDEX_METRIKA = 108522291
REVIEWS_URL = "https://www.google.com/maps/search/?api=1&query=DEHR+Ltd"
SOCIAL = [
    ("Telegram", "https://t.me/dehrcompany", "tg"),
    ("Instagram", "https://www.instagram.com/dehrcompany/", "ig"),
    ("TikTok", "https://www.tiktok.com/@dehrcompany", "tt"),
    ("Facebook", "https://www.facebook.com/groups/workinginsrael", "fb"),
]
LANGS = [("ru", "", "ltr"), ("he", "he/", "rtl"), ("en", "en/", "ltr")]   # ru — основной язык и x-default
PAGES = [("privacy", "priv_title"), ("accessibility", "a11y_title")]
VALID_DAYS_NOTE = "2026-12-31"   # до какой даты вакансии считаются открытыми (для Google Jobs)

ICONS = {
 "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.4 14.1c-.2.6-1.3 1.2-1.8 1.3-.5 0-1 .2-3.3-.7-2.8-1.1-4.5-4-4.7-4.2-.1-.2-1.1-1.5-1.1-2.9s.7-2 1-2.3c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.9 2.1c.1.2.1.4 0 .5l-.3.5-.4.4c-.1.2-.3.3-.1.6.2.3.8 1.3 1.7 2.1 1.2 1 2.1 1.3 2.4 1.5.3.1.5.1.6-.1l.9-1.1c.2-.3.4-.2.6-.1l2 1c.3.1.5.2.5.3.1.2.1.7-.1 1.3Z"/></svg>',
 "tg": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.5 4.3 2.9 11.5c-1.3.5-1.2 1.2-.2 1.5l4.8 1.5 1.8 5.6c.2.6.4.8.9.8.4 0 .6-.2.9-.5l2.4-2.3 4.9 3.6c.9.5 1.5.2 1.8-.8l3.2-15.1c.3-1.3-.5-1.9-1.4-1.5ZM9.3 14.3l9-5.7c.4-.3.8-.1.5.2l-7.4 6.7-.3 3.3-1.8-4.5Z"/></svg>',
 "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/></svg>',
 "tt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 3c.4 2.3 1.8 3.8 4.1 4v3.1c-1.5.1-2.9-.3-4.1-1.1v6.3c0 3.4-2.5 5.7-5.6 5.7A5.6 5.6 0 0 1 5.4 15.4c0-3.3 2.8-5.9 6.3-5.5v3.2c-1.6-.3-3.1.8-3.1 2.4 0 1.4 1.1 2.4 2.4 2.4 1.5 0 2.4-1 2.4-2.6V3h3.2Z"/></svg>',
 "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.6h2.6l.4-3h-3V8.5c0-.9.3-1.5 1.5-1.5h1.6V4.3c-.3 0-1.2-.1-2.3-.1-2.3 0-3.9 1.4-3.9 4v2.2H7.8v3h2.6V21h3.1Z"/></svg>',
}
LOGO = ('<svg width="34" height="34" viewBox="0 0 34 34" aria-hidden="true"><rect width="34" height="34" rx="10" fill="#0F1B2D"/>'
        '<circle cx="10" cy="23" r="3.2" fill="#FBF8F3"/><circle cx="24" cy="11" r="3.2" fill="#FF5B1F"/>'
        '<path d="M12.5 21 Q 14 12 21.5 12.5" stroke="#FBF8F3" stroke-width="2" fill="none" stroke-dasharray="2.5 2.5"/></svg>')
SCHEMA_UNIT = {"hour": "HOUR", "month": "MONTH"}


def fill(tpl, ctx, name):
    def sub(m):
        k = m.group(1)
        if k not in ctx:
            raise KeyError(f"{name}: нет значения для {{{{{k}}}}}")
        return str(ctx[k])
    return re.sub(r"\{\{(\w+)\}\}", sub, tpl)


def url(prefix, page=""):
    return "/" + prefix + (page + "/" if page else "")


def wa(text):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(text)}"


def main():
    S = json.loads((SRC / "strings.json").read_text(encoding="utf-8"))
    J = json.loads((SRC / "jobs.json").read_text(encoding="utf-8"))
    page_tpl = (SRC / "page.html").read_text(encoding="utf-8")
    legal_tpl = (SRC / "legal.html").read_text(encoding="utf-8")
    style = (SRC / "style.css").read_text(encoding="utf-8")
    app = (SRC / "app.js").read_text(encoding="utf-8")
    ver = hashlib.sha1((style + app).encode()).hexdigest()[:8]

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(PUB, DIST)
    (DIST / "assets").mkdir(exist_ok=True)
    (DIST / "assets" / "style.css").write_text(style, encoding="utf-8")
    (DIST / "assets" / "app.js").write_text(app, encoding="utf-8")

    for job in J["jobs"]:
        for c in job["cities"]:
            assert c in J["cities"], f"{job['id']}: неизвестный город {c}"
        if job.get("photo"):
            assert (PUB / job["photo"]).exists(), f"{job['id']}: нет файла {job['photo']}"

    sitemap = []
    for lang, prefix, d in LANGS:
        t = S[lang]
        cities = {k: {"ll": v["ll"], "name": v[lang]} for k, v in J["cities"].items()}
        jobs = []
        for j in J["jobs"]:
            x = j[lang]
            jobs.append({"id": j["id"], "cat": j["cat"], "cities": j["cities"], "pay": j["pay"], "house": j["house"],
                         "who": j["who"], "photo": j.get("photo"), "title": x["title"], "desc": x["desc"],
                         "tags": x["tags"], "docs": x.get("docs", ""), "langs": x.get("lang", "")})

        def alternates(page=""):
            out = [f'<link rel="alternate" hreflang="{l}" href="{SITE}{url(p, page)}">' for l, p, _ in LANGS]
            out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}{url("", page)}">')
            return "\n".join(out)

        def langs_nav(page=""):
            return "".join(f'<a href="{url(p, page)}" hreflang="{l}" lang="{l}"'
                           + (' aria-current="true"' if l == lang else "") + f">{l.upper()}</a>" for l, p, _ in LANGS)

        lic = f" · {t['ft_lic']}" if t.get("ft_lic") else ""
        footer = (f'<footer><div class="wrap"><span>© 2026 DEHR Ltd{lic} · {t["ft_tag"]}</span>'
                  f'<nav aria-label="{t["ft_priv"]}"><a href="{url(prefix, "privacy")}">{t["ft_priv"]}</a>'
                  f'<a href="{url(prefix, "accessibility")}">{t["ft_a11y"]}</a></nav></div></footer>')
        data_common = {"lang": lang, "wa": WA, "tg": TELEGRAM, "ym": YANDEX_METRIKA}
        base = {
            "lang": lang, "dir": d, "site": SITE, "ver": ver, "home": url(prefix), "logo_svg": LOGO,
            "icon_wa": ICONS["wa"], "footer": footer, "priv_url": url(prefix, "privacy"),
            "wa_general_url": html.escape(wa(t["wa_general"])),
        }
        base.update({k: v for k, v in t.items() if isinstance(v, str)})

        # --- главная ---
        org = {"@type": "EmploymentAgency", "@id": SITE + "/#org", "name": "DEHR Ltd", "url": SITE + "/",
               "logo": SITE + "/apple-touch-icon.png", "telephone": PHONE_TEL, "areaServed": "IL",
               "sameAs": [s[1] for s in SOCIAL]}
        postings = []
        for j, x in zip(J["jobs"], jobs):
            postings.append({
                "@type": "JobPosting", "identifier": {"@type": "PropertyValue", "name": "DEHR Ltd", "value": j["id"]},
                "title": x["title"], "description": f"<p>{html.escape(x['desc'])}</p><p>{html.escape(', '.join(x['tags']))}</p>",
                "datePosted": j["posted"], "validThrough": VALID_DAYS_NOTE + "T23:59", "employmentType": "FULL_TIME",
                "hiringOrganization": {"@id": SITE + "/#org"}, "directApply": False,
                "jobLocation": [{"@type": "Place", "address": {"@type": "PostalAddress",
                                 "addressLocality": J["cities"][c]["en"], "addressCountry": "IL"}} for c in j["cities"]],
                "baseSalary": {"@type": "MonetaryAmount", "currency": "ILS",
                               "value": {"@type": "QuantitativeValue", "value": j["pay"]["amount"], "unitText": SCHEMA_UNIT[j["pay"]["per"]]}},
                "url": f"{SITE}{url(prefix)}#job-{j['id']}", "inLanguage": lang,
            })
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": [org] + postings}, ensure_ascii=False).replace("</", "<\\/")
        tdyn = {k: v for k, v in t.items() if k.startswith("_") or k == "wa_job"}
        data = json.dumps(dict(data_common, t=tdyn, cities=cities, jobs=jobs), ensure_ascii=False).replace("</", "<\\/")
        nos = "".join(f'<li><a href="{html.escape(wa(t["wa_job"].replace("{id}", x["id"]).replace("{title}", x["title"]).replace("{cities}", ", ".join(cities[c]["name"] for c in x["cities"]))))}">'
                      f'{html.escape(x["id"])} · {html.escape(x["title"])} — {x["pay"]["amount"]} {html.escape(t["_month"] if x["pay"]["per"] == "month" else t["_hour"])}</a></li>' for x in jobs)
        social = "".join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}" title="{n}">{ICONS[i]}</a>' for n, u, i in SOCIAL)
        ctx = dict(base,
                   meta_title=html.escape(t["meta_title"]), meta_desc=html.escape(t["meta_desc"]),
                   canonical=SITE + url(prefix), alternates=alternates(), langs=langs_nav(), jsonld=jsonld, data=data,
                   noscript_jobs=f"<noscript><ul>{nos}</ul></noscript>",
                   wa_employer_url=html.escape(wa(t["wa_employer"])), wa_partner_url=html.escape(wa(t["wa_partner"])),
                   wa_candidate_url=html.escape(wa(t["wa_candidate"])), reviews_url=html.escape(REVIEWS_URL),
                   social=social, phone=PHONE, phone_tel=PHONE_TEL, telegram=TELEGRAM, telegram_url=f"https://t.me/{TELEGRAM}")
        out = DIST / prefix / "index.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(fill(page_tpl, ctx, f"{lang}/index"), encoding="utf-8")
        sitemap.append(SITE + url(prefix))

        # --- политика и доступность ---
        ldata = json.dumps(dict(data_common, t={}, cities={}, jobs=[]), ensure_ascii=False)
        for slug, title_key in PAGES:
            body = (SRC / "legal" / f"{slug}.{lang}.html").read_text(encoding="utf-8")
            lctx = dict(base, title=t[title_key], body=body, canonical=SITE + url(prefix, slug),
                        alternates=alternates(slug), langs=langs_nav(slug), data=ldata)
            o = DIST / prefix / slug / "index.html"
            o.parent.mkdir(parents=True, exist_ok=True)
            o.write_text(fill(legal_tpl, lctx, f"{lang}/{slug}"), encoding="utf-8")
            sitemap.append(SITE + url(prefix, slug))

    # --- 404 (на трёх языках сразу, GitHub Pages отдаёт один файл) ---
    nf_body = "".join(f'<section lang="{l}" dir="{d}" style="padding-block:28px"><h1>{S[l]["nf_title"]}</h1><p>{S[l]["nf_p"]}</p>'
                      f'<a class="btn btn-signal" href="{url(p)}">{S[l]["nf_btn"]}</a></section>' for l, p, d in LANGS)
    (DIST / "404.html").write_text(
        f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>404 — DEHR Ltd</title><meta name="robots" content="noindex"><link rel="icon" href="/favicon.svg" type="image/svg+xml">'
        f'<link rel="stylesheet" href="/assets/fonts/fonts.css?v={ver}"><link rel="stylesheet" href="/assets/style.css?v={ver}"></head>'
        f'<body><main class="nf"><div class="wrap">{nf_body}</div></main></body></html>', encoding="utf-8")

    (DIST / "CNAME").write_text("dehr.ltd\n", encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{u}</loc></url>\n" for u in sitemap) + "</urlset>\n", encoding="utf-8")
    n = sum(1 for _ in DIST.rglob("*") if _.is_file())
    print(f"OK: {n} файлов в {DIST} (версия {ver})")


if __name__ == "__main__":
    main()
