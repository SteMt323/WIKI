"""build_static.py
Genera un sitio estático en `public/` a partir de los markdown en `entries/`
- Convierte cada `.md` a HTML usando markdown
- Copia assets estáticos a `public/static/`
- Crea `index.html` con tarjetas usando metadata de `datas/wikis.json` si existe

Uso:
    python build_static.py
"""
import os
import shutil
import json
from markdown import markdown
from pathlib import Path

ROOT = Path(__file__).parent
ENTRIES = ROOT / "entries"
DATAS = ROOT / "datas" / "wikis.json"
PUBLIC = ROOT / "public"
TEMPLATES = ROOT / "encyclopedia" / "templates" / "encyclopedia"
STATIC_SRC = [ROOT / "static", ROOT / "encyclopedia" / "static"]

BASE_HTML = """<!doctype html>
<html lang=\"es\"> 
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
  <title>{title}</title>
  <link rel=\"stylesheet\" href=\"/static/encyclopedia/stylesv1.css\"> 
  <link rel=\"stylesheet\" href=\"/static/encyclopedia/stylecards.css\"> 
</head>
<body>
  <div class=\"container\">{body}</div>
</body>
</html>
"""

CARD_TEMPLATE = """
<div class="card">
  {img}
  <h3>{title}</h3>
  <p>Categoria: {category}</p>
  <p>Author: {author}</p>
  <a href="/wiki/{url_title}">Ver</a>
</div>
"""


def ensure_public():
    if PUBLIC.exists():
        shutil.rmtree(PUBLIC)
    PUBLIC.mkdir(parents=True)
    (PUBLIC / "wiki").mkdir()
    (PUBLIC / "static").mkdir()


def load_metadata():
    if DATAS.exists():
        try:
            with open(DATAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def copy_static():
    for src in STATIC_SRC:
        if not src.exists():
            continue
        for root, dirs, files in os.walk(src):
            rel = Path(root).relative_to(src)
            target_dir = PUBLIC / "static" / rel
            target_dir.mkdir(parents=True, exist_ok=True)
            for file in files:
                shutil.copy2(Path(root) / file, target_dir / file)


def build_entries(meta):
    titles = []
    for md in ENTRIES.glob("*.md"):
        title = md.stem
        titles.append(title)
        with open(md, "r", encoding="utf-8") as f:
            content = f.read()
        html = markdown(content, extensions=["extra", "fenced_code"])
        body = f"<h1>{title}</h1>\n" + html
        out = BASE_HTML.format(title=title, body=body)
        out_path = PUBLIC / "wiki" / f"{title}.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)
    return titles


def build_index(titles, meta):
    # build cards
    meta_map = {m.get("title", ""): m for m in meta}
    cards = []
    for t in titles:
        m = meta_map.get(t, {})
        img = ''
        if m.get('image_url'):
            img = f"<img src=\"{m.get('image_url')}\" alt=\"{t}\">"
        cards.append(CARD_TEMPLATE.format(img=img, title=t, category=m.get('category','-'), author=m.get('author','-'), url_title=t))
    body = '<h1>Wiki</h1>\n<div class="cards">' + '\n'.join(cards) + '</div>'
    out = BASE_HTML.format(title="Index", body=body)
    with open(PUBLIC / "index.html", "w", encoding="utf-8") as f:
        f.write(out)


def main():
    ensure_public()
    meta = load_metadata()
    copy_static()
    titles = build_entries(meta)
    build_index(titles, meta)
    print(f"Built static site at {PUBLIC}")

if __name__ == '__main__':
    main()
