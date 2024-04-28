from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from . import util
from .forms import CreateEntryForm, EditEntryForm
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
            "found": found,
            "all_entries": util.list_entries()
        })
    return render(request, "encyclopedia/index.html", {
        "entries": entries,
        "all_entries": util.list_entries()
    })

def entry(request, title):
    entry_file = util.get_entry(title)
    if not entry_file:
        raise Http404("PAGE NOT FOUND")
    
    entry_html = markdown2.markdown(entry_file)
    return render(request, "encyclopedia/entry.html",{
        "title": title,
        "entry": entry_html,
        "all_entries": util.list_entries()
    })

def search(request):
    return HttpResponse("Search Page")

def create(request):
    if request.method == "POST":
        # Validate form first 
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            form_title = form.cleaned_data['title']
            form_content = form.cleaned_data['content']
            entries = util.list_entries()
            # Check if entry title already exists
            for entry in entries:
                if form_title == entry:
                    error = "Error: Title Already Exists. Try Another."
                    return render(request, "encyclopedia/create.html", {
                        "form": form,
                        "error": error,
                        "all_entries": util.list_entries()
                    })
            # Save new entry to disk and go to page
            util.save_entry(form_title, form_content)
            return HttpResponseRedirect(reverse("entry", args=[form_title]))
    else:
        form = CreateEntryForm()

    return render(request, "encyclopedia/create.html", {
        "form": form,
        "all_entries": util.list_entries()
    })

def edit(request, title):
    form = EditEntryForm({'content': util.get_entry(title)})
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid:
            form_content = request.POST['content']
            util.save_entry(title, form_content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        
    return render(request, "encyclopedia/edit.html", {
        "form": form,
        "title": title,
        "all_entries": util.list_entries()
    })
