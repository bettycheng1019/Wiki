from django.shortcuts import render
from . import util
import markdown
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import random



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
            "entry": markdown.markdown(entryPage),
            "entryTitle": entry
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
            return render(request, "encyclopedia/noresult.html", {
            "entryTitle": search
        })
        else:
            return render(request, "encyclopedia/search_res.html",{
                "result": result
             })

class NewEntryForm(forms.Form):
    entryTitle = forms.CharField(label="New Entry", widget=forms.TextInput(attrs={'class': 'form-control col-md-10 cl-lg-10'}))
    entryContent = forms.CharField(label="New Content", widget=forms.Textarea(attrs={'class': 'form-control col-md-10 cl-lg-10','rows':10}))
    
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

def editPage(request):
        if request.method == 'POST':
            input_title = request.POST['title']
            text = util.get_entry(input_title)
        return render(request, "encyclopedia/editPage.html",{
            "entry": text,
            "entryTitle": input_title
        })

def saveEdit(request):
    if request.method == 'POST':
        entryTitle = request.POST['title']
        entry = request.POST['text']
        util.save_entry(entryTitle, entry)
        html = markdown.markdown(util.get_entry(entryTitle))
        return render (request, "encyclopedia/entry.html",{
            "entry": html,
            "entryTitle": entryTitle
        })

def randomEntry(request):
    entryR=random.choice(util.list_entries())
    entryPage = util.get_entry(entryR)
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown.markdown(entryPage),
        "entryTitle": entryR
    })