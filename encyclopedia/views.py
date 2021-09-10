from django.shortcuts import render
from . import util
import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    }) 


def entry(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/page_not_found.html", {
            "entryTitle": entry
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markdown.markdown(entryPage)
        })

def search(request):
    search = request.GET.get('q')
    if util.get_entry(search) is not None:
        return HttpResponseRedirect(reverse('entry', kwargs={ 'entry': search }))
    else:
        result = []
        for entry in util.list_entries():
            if search.upper() in entry.upper():
                result.append(entry)
        if not result:
            return render(request, "encyclopedia/page_not_found.html", {
            "entryTitle": search
        })
        else:
            return render(request, "encyclopedia/search_res.html",{
                "result": result
             })

class NewEntryForm(forms.Form):
    entryTitle = forms.CharField(label="New Entry")
    entryContent = forms.CharField(label="New Content")
    
def add(request):
    if request.method == "POST":
        newpage = NewEntryForm(request.POST)
        if newpage.is_valid():
            entryT = newpage.cleaned_data["entryTitle"]
            entryC = newpage.cleaned_data["entryContent"]
            if util.get_entry(entryT) is None:
                util.save_entry(entryT, entryC)
                return render(request, "encyclopedia/entry.html", {
                    "entry": markdown.markdown(util.get_entry(entryT))
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "entryTitle": entryT
                })
        else:
            return render(request, "encyclopedia/add.html", {
                "form": newpage
            })
    return render(request, "encyclopedia/add.html", {
        "form": NewEntryForm()
    })

# class EditForm(forms.Form):
#     edit = forms.CharField(label="New Content")

# def edit(request):
#     if request.method == "POST":
#         new_content = EditForm(request.POST)
#         if new_content.is_valid():
#             edit = new_content.cleaned_data["entryContentNew"]
#             util.save_entry(entry, edit)
#                 return HttpResponseRedirect(reverse('entry'))
#         else:
#             return render(request, "encyclopedia/edit.html", {
#                 "form": new_content
#             })
#     return render(request, "encyclopedia/edit.html", {
#         "form": EditForm()
#     })