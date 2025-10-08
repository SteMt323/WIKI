import re
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import json
import os
from PIL import Image
import os
from difflib import SequenceMatcher

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    # Ensure we write UTF-8 bytes to avoid corruption of accents/emojis
    if isinstance(content, str):
        content_bytes = content.encode("utf-8")
    else:
        content_bytes = content
    default_storage.save(filename, ContentFile(content_bytes))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md", "rb")
        raw = f.read()
        if isinstance(raw, bytes):
            return raw.decode("utf-8")
        return raw
    except FileNotFoundError:
        return None

def save_data(title, category, author):
    dir_path = 'datas'
    if not default_storage.exists(dir_path):
        os.makedirs(os.path.join(default_storage.location, dir_path), exist_ok=True)
    file_path = f"{dir_path}/wikis.json"
    data = []
    if default_storage.exists(file_path):
        # Read file as bytes and decode using utf-8 to preserve special chars
        with default_storage.open(file_path, 'rb') as f:
            try:
                raw = f.read()
                if isinstance(raw, bytes):
                    data = json.loads(raw.decode('utf-8'))
                else:
                    data = json.load(f)
            except Exception:
                data = []
    # Prevent duplicate metadata entries by title (case-insensitive)
    normalized_title = title.strip().lower()
    for entry in data:
        if entry.get('title', '').strip().lower() == normalized_title:
            # Duplicate found; don't add
            return False

    new_entry = {
        "title": title,
        "category": category,
        "author": author,
    }
    data.append(new_entry)
    # Write JSON using utf-8 bytes so special characters are preserved
    content_bytes = json.dumps(data, indent=2, ensure_ascii=False).encode('utf-8')
    content_file = ContentFile(content_bytes)
    if default_storage.exists(file_path):
        default_storage.delete(file_path)
    default_storage.save(file_path, content_file)
    return True
    
    
def get_entries_meta(titles):
    file_path = "datas/wikis.json"
    results = []
    if default_storage.exists(file_path):
        with default_storage.open(file_path, "rb") as f:
            try:
                raw = f.read()
                if isinstance(raw, bytes):
                    data = json.loads(raw.decode('utf-8'))
                else:
                    data = json.load(f)
            except Exception:
                data = []
        for title in titles:
            for entry in data:
                if entry.get("title", "").lower() == title.lower():
                    image_url = get_image(title)
                    results.append({
                        "title": entry.get("title"),
                        "category": entry.get("category"),
                        "author": entry.get("author"),
                        "image_url": image_url
                    })
    return results
    
def convert_to_webp(title):
    image_dir = "encyclopedia/static/images"
    for ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        img_path = os.path.join(image_dir, f"{title}{ext}")
        if os.path.exists(img_path):
            img = Image.open(img_path)
            webp_path = os.path.join(image_dir, f"{title}.webp")
            img.save(webp_path, "WEBP")
            os.remove(img_path)
            return webp_path
    return None

def get_image(title):
    image_dir = "encyclopedia/static/images"
    webp_path = os.path.join(image_dir, f"{title}.webp")
    if os.path.exists(webp_path):
        return f"/static/images/{title}.webp"
    for ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp"]:
        img_path = os.path.join(image_dir, f"{title}{ext}")
        if os.path.exists(img_path):
            return f"/static/images/{title}{ext}"
    return None


"""Con coincidencias"""    
"""
def match(lista, reference, umb=0.3):
    coincidence = []
    for palabra in lista:
        ratio = SequenceMatcher(None, palabra, reference).ratio()
        if ratio>=umb:
            coincidence.append((palabra))
    return coincidence

"""

"""Con subcadenas"""


def match(lista, reference):
    coincidence = []
    ref = reference.lower()
    for palabra in lista:
        if ref in palabra.lower():
            coincidence.append(palabra)
    return coincidence

