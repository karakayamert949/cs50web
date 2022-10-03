from django.http import HttpResponseRedirect
from django.shortcuts import render

from . import util

import markdown2


def index(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })
    elif request.method == 'POST':
        search_string=request.POST["q"]
        if util.get_entry(search_string):
            return HttpResponseRedirect(f"/wiki/{search_string}")
        # buradan devam et
        else:
            results = []
            for entry in util.list_entries():
                if search_string.lower() in entry.lower():
                    results.append(entry)
            return render(request, "encyclopedia/results.html", {
                "results": results,
                "search": search_string
            })

def dispEntry(request,title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "content": markdown2.markdown(util.get_entry(title))
            })
    else:
        return render(request,"encyclopedia/error.html", {
            "title":title.capitalize()
        }, status=404)
