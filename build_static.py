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
import re
import unicodedata
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
    <link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css\" integrity=\"sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh\" crossorigin=\"anonymous\">
    <link rel=\"stylesheet\" href=\"/static/encyclopedia/stylesv1.css\"> 
    <link rel=\"stylesheet\" href=\"/static/encyclopedia/stylecards.css\"> 
</head>
<body>
    <div class=\"row\"> 
        <div class=\"sidebar col-lg-2 col-md-3\"> 
            <h2 class=\"letters\">Wiki</h2>
                <form action=\"/search/\" method=\"get\"> 
                <div class=\"search-input\"> 
                        <input class="search" type="text" name="q" placeholder="Search Encyclopedia"> 
                </div>
            </form>
            <div class=\"sidebar-elements\"> 
                <a class=\"sidebar-links\" href=\"/\">Home</a>
            </div>
            <div class=\"sidebar-elements\"> 
                <a class=\"sidebar-links\" href=\"/newpage.html\">Create New Page</a>
            </div>
            <div class=\"sidebar-elements\"> 
                <a class=\"sidebar-links\" href=\"/random.html\">Random Page</a>
            </div>
        </div>
        <div class=\"main col-lg-10 col-md-9\">{body}</div>
    </div>
</body>
</html>
"""

CARD_TEMPLATE = """
<div class=\"card\" data-title=\"{title_lower}\">\n  <div class=\"card__img\" style=\"background-image: url('{img_url}')\"></div>\n  <div class=\"card__img--hover\" style=\"background-image: url('{img_url}')\"></div>\n  <div class=\"card__info\">\n    <p class=\"card__category\">{category}</p>\n    <h3 class=\"card__title\">{title}</h3>\n    <p class=\"card__by\">By <span class=\"card__author\">{author}</span></p>\n    <a class=\"ct\" href=\"/wiki/{url_title}\">Ver</a>\n  </div>\n</div>\n"""


def slugify(value):
        """Return URL-friendly slug for a given title."""
        value = str(value)
        # Normalize unicode characters to closest ASCII representation
        value = unicodedata.normalize('NFKD', value)
        value = value.encode('ascii', 'ignore').decode('ascii')
        value = value.lower()
        # replace non-alphanumeric characters with hyphens
        value = re.sub(r'[^a-z0-9]+', '-', value)
        value = value.strip('-')
        return value or 'untitled'


def ensure_public():
    if PUBLIC.exists():
        try:
            shutil.rmtree(PUBLIC)
        except PermissionError:
            print("ERROR: no se puede eliminar 'public/' porque está en uso por otro proceso.")
            print("Por ejemplo: si estás ejecutando 'python -m http.server' en la carpeta 'public', detén ese servidor y vuelve a ejecutar el build.")
            print("En Windows puedes detener la ejecución con Ctrl+C en la terminal que lanzó el servidor o matar procesos 'python' si están en background.")
            raise
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
    # Also return mapping from title -> slug
    title_to_slug = {}
    for md in ENTRIES.glob("*.md"):
        title = md.stem
        titles.append(title)
        slug = slugify(title)
        title_to_slug[title] = slug
        with open(md, "r", encoding="utf-8") as f:
            content = f.read()
        html = markdown(content, extensions=["extra", "fenced_code"])
        body = f"<h1>{title}</h1>\n" + html
        out = BASE_HTML.format(title=title, body=body)
        # create directory public/wiki/<slug>/index.html for pretty URLs
        out_dir = PUBLIC / "wiki" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_path = out_dir / "index.html"
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(out)
        # Also create legacy flat HTML filename to preserve old links
        legacy_path = PUBLIC / "wiki" / f"{title}.html"
        with open(legacy_path, "w", encoding="utf-8") as f:
            f.write(out)
    return titles, title_to_slug


def build_index(titles, meta, title_to_slug):
    # build cards
    meta_map = {m.get("title", ""): m for m in meta}
    cards = []
    for t in titles:
        m = meta_map.get(t, {})
        img_url = m.get('image_url', '')
        # If metadata doesn't include an image_url, try to find a matching image
        if not img_url:
            image_dir = ROOT / 'encyclopedia' / 'static' / 'images'
            if image_dir.exists():
                for ext in ('.webp', '.png', '.jpg', '.jpeg', '.gif', '.bmp'):
                    cand = image_dir / f"{t}{ext}"
                    if cand.exists():
                        img_url = f"/static/images/{cand.name}"
                        break
        slug = title_to_slug.get(t, slugify(t))
        cards.append(CARD_TEMPLATE.format(img_url=img_url, title=t, title_lower=t.lower(), category=m.get('category','-'), author=m.get('author','-'), url_title=slug))
    body = '<h1>Wiki</h1>\n<div class="cards">' + '\n'.join(cards) + '</div>'
    out = BASE_HTML.format(title="Index", body=body)
    with open(PUBLIC / "index.html", "w", encoding="utf-8") as f:
        f.write(out)


def build_search_page(titles, title_to_slug, meta):
        meta_map = {m.get("title", ""): m for m in meta}
        cards_html = []
        for t in titles:
                m = meta_map.get(t, {})
                img_url = m.get('image_url', '')
                if not img_url:
                        image_dir = ROOT / 'encyclopedia' / 'static' / 'images'
                        if image_dir.exists():
                                for ext in ('.webp', '.png', '.jpg', '.jpeg', '.gif', '.bmp'):
                                        cand = image_dir / f"{t}{ext}"
                                        if cand.exists():
                                                img_url = f"/static/images/{cand.name}"
                                                break
                slug = title_to_slug.get(t, slugify(t))
                cards_html.append(CARD_TEMPLATE.format(img_url=img_url, title=t, title_lower=t.lower(), category=m.get('category','-'), author=m.get('author','-'), url_title=slug))
        search_body = '<h1>Search</h1>\n<p id="msg"></p>\n<div id="cards" class="cards">' + '\n'.join(cards_html) + '</div>'
        search_html = BASE_HTML.format(title="Search", body=search_body)
        script = """
<script>
    (function(){
        const params = new URLSearchParams(window.location.search);
        const q = (params.get('q') || '').toLowerCase();
        const cards = Array.from(document.querySelectorAll('.card'));
        if(!q){
            document.getElementById('msg').textContent = 'Use the search box to filter entries.';
            return;
        }
        let found = 0;
        cards.forEach(c=>{
            const title = c.getAttribute('data-title') || '';
            if(title.includes(q)){
                c.style.display = '';
                found++;
            } else {
                c.style.display = 'none';
            }
        });
        document.getElementById('msg').textContent = found ? found + ' results' : 'No results';
        if(found === 1){
            const visible = cards.find(c=>c.style.display !== 'none');
            const a = visible && visible.querySelector('a');
            if(a) window.location.href = a.href;
        }
    })();
</script>
"""
        search_html = search_html.replace('</body>', script + '\n</body>')
        out_dir = PUBLIC / 'search'
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / 'index.html', 'w', encoding='utf-8') as f:
                f.write(search_html)


def build_newpage(meta):
        body = '<h1>Create New Page</h1>\n<p>This is a static copy of the new page form. To add entries, edit the Markdown files in the <code>entries/</code> folder or use the dynamic Django app.</p>'
        body += '<form><input placeholder="Title"><br><textarea placeholder="Content"></textarea><br><button disabled>Submit (not available in static)</button></form>'
        out = BASE_HTML.format(title='Create New Page', body=body)
        with open(PUBLIC / 'newpage.html', 'w', encoding='utf-8') as f:
                f.write(out)


def build_random_page(title_to_slug):
        slugs = [title_to_slug[t] for t in title_to_slug]
        script = '<script>const s=' + json.dumps(slugs) + '; location.href = \'/wiki/\' + s[Math.floor(Math.random()*s.length)];</script>'
        body = '<h1>Random page</h1>' + script
        out = BASE_HTML.format(title='Random', body=body)
        with open(PUBLIC / 'random.html', 'w', encoding='utf-8') as f:
                f.write(out)



def main():
    ensure_public()
    meta = load_metadata()
    copy_static()
    titles, title_to_slug = build_entries(meta)
    build_index(titles, meta, title_to_slug)
    # auxiliary static pages
    try:
        build_search_page(titles, title_to_slug, meta)
        build_newpage(meta)
        build_random_page(title_to_slug)
    except Exception:
        # If auxiliary page generation fails, print and continue
        print('Warning: failed to generate auxiliary static pages')
    print(f"Built static site at {PUBLIC}")

if __name__ == '__main__':
    main()
