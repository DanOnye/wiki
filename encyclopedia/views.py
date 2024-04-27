from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from . import util
import markdown2


def index(request):
    entries = util.list_entries()

    if request.method == "POST":
        # Check for matches
        matches = []
        query = request.POST["q"]
        
        if query:
            for entry in entries:
                if query == entry:
                    return HttpResponseRedirect(reverse("entry", args=[entry]))
                if query in entry:
                    matches.append(entry)

        found = True if matches else False
        return render(request, "encyclopedia/search.html", {
            "entries": matches,
            "found": found
        })
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })

def entry(request, title):
    entry_file = util.get_entry(title)
    if not entry_file:
        raise Http404("PAGE NOT FOUND")
    
    entry_html = markdown2.markdown(entry_file)
    return render(request, "encyclopedia/entry.html",{
        "title": title,
        "entry": entry_html
    })

def search(request):
    return HttpResponse("Search Page")

