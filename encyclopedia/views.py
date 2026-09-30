import random
from django.shortcuts import render, redirect
from markdown2 import Markdown

from . import util



def convert_to_HTML(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content is None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    html_content = convert_to_HTML(title)
    if html_content is None:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/entry.html",{
            "title":title,
            "content":html_content
            })


def search(request):

    query = request.GET.get("q")

    entries = util.list_entries()

    for entry in entries:
        if query.lower() == entry.lower():
            html_content = convert_to_HTML(entry)
            return render(request, "encyclopedia/entry.html", {
            "title":query,
            "content":html_content
            })


    results = []

    for entry in entries:
        if query.lower() in entry.lower():
            results.append(entry)
    return render(request, "encyclopedia/search.html", {
        "entries": results,
        "query": query
            })

def new_page(request):

    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message":"An entry with this title already exist."
            })

        util.save_entry(title, content)

        return redirect("entry", title=title)

    return render(request, "encyclopedia/new_page.html")


def edit_page(request, title):

    if request.method == "POST":
        content = request.POST.get("content")

        util.save_entry(title, content)
        return redirect("entry", title = title)

    content = util.get_entry(title)
    return render(request, "encyclopedia/edit_page.html", {
        "title":title,
        "content":content
    })

def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return redirect("entry", title = title)



