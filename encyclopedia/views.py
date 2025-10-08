from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from . import util
import markdown
import os
import random
from .forms import NewWiki
import bleach

# Bleach policy: allow class attribute so users can use CSS classes defined in site CSS
ALLOWED_TAGS = [
    'p','br','ul','ol','li','strong','em','a','img','h1','h2','h3','pre','code','blockquote',
    # table-related tags
    'table','thead','tbody','tr','th','td'
]
ALLOWED_ATTRS = {
    'a': ['href', 'title', 'rel'],
    'img': ['src', 'alt', 'title'],
    # allow certain table attributes that are commonly used
    'th': ['colspan', 'rowspan', 'scope', 'class'],
    'td': ['colspan', 'rowspan', 'class'],
    '*': ['class']
}

def index(request):
    entries = util.list_entries()
    entries_meta = util.get_entries_meta(entries)
    return render(request, "encyclopedia/index.html", {
        "entries": entries_meta,
        
    })
    
def wiki(request, title):
    achive = util.get_entry(title)
    if achive is None:
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "wikis": "Enciclopedia no encontrada :(..."
        })

    # Convert markdown to HTML with 'extra' extension (tables, etc.) and sanitize
    raw_html = markdown.markdown(achive, extensions=["extra", "fenced_code"]) 
    content = bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    return render(request, "encyclopedia/wiki.html", {
        "title": title,
        "wikis": mark_safe(content)
    })
        
def search(request):
    query = request.GET.get("q", "")
    list_entries = util.list_entries()
    results = util.match(list_entries, query)
    
    if util.get_entry(query) is not None:
        raw_html = markdown.markdown(util.get_entry(query), extensions=["extra", "fenced_code"]) 
        content = bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
        return render(request, "encyclopedia/wiki.html", {
            "wikis": mark_safe(content), "title": query
        })  
    elif len(results) == 0:
        return render(request, "encyclopedia/results.html", {
            "results": "No results :(..."
        }) 
    else:
        entries_meta = util.get_entries_meta(results)
        return render(request, "encyclopedia/results.html", {
            "entries": entries_meta,
        
    })
        
def newpage(request):
    if request.method == "POST":
        form = NewWiki(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data["title"]
            category = form.cleaned_data["category"]
            author = form.cleaned_data["author"]
            content = form.cleaned_data["content"]
            image = form.cleaned_data["image"]

            # Validation: do not allow duplicate content entries or duplicate metadata
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error": "Ya existe una entrada con este titulo :(..."
                })

            # Check metadata duplicates (case-insensitive)
            existing_meta = util.get_entries_meta([title])
            if existing_meta:
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error": "Ya existe metadatos para una entrada con este titulo :(..."
                })

            # Save image only after validations succeed
            image_path = None
            if image:
                image_ext = os.path.splitext(image.name)[1]
                image_path = f"encyclopedia/static/images/{title}{image_ext}"
                default_storage.save(image_path, image)

            # Save entry content and metadata. If metadata saving fails, rollback saved files.
            util.save_entry(title, content)
            saved = util.save_data(title, category, author)
            if not saved:
                # Rollback: delete the entry file and image if they were saved
                entry_path = f"entries/{title}.md"
                if default_storage.exists(entry_path):
                    default_storage.delete(entry_path)
                if image_path and default_storage.exists(image_path):
                    default_storage.delete(image_path)
                return render(request, "encyclopedia/newpage.html", {
                    "form": form,
                    "error": "No se pudieron guardar los metadatos (posible duplicado)."
                })

            raw_html = markdown.markdown(content, extensions=["extra", "fenced_code"]) 
            clean_html = bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
            return render(request, "encyclopedia/wiki.html",{
                "title": title,
                "wikis": mark_safe(clean_html)
            })
    else:
        form = NewWiki()
    return render(request, "encyclopedia/newpage.html",{
        "form": form
    })
    
def edit_entry(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/wiki.html", {
                "title": title,
                "wikis": "Enciclopedia no encontrada :(..."
            })
        return render(request, "encyclopedia/edit_entry.html",{
            "title":title,
            "content":content
        })
    else:
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        
        return redirect("wiki", title=title)
    
def randpage(request):
    entries = util.list_entries()
    selection = random.choice(entries)
    raw_html = markdown.markdown(util.get_entry(selection), extensions=["extra", "fenced_code"]) 
    clean_html = bleach.clean(raw_html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    return render(request, "encyclopedia/wiki.html",{
        "title":selection,
        "wikis": mark_safe(clean_html)
    })
        
    