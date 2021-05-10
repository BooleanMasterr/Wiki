from django.shortcuts import render
from .forms import NewEntryForm, UpdateForm, Search
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
import markdown
import random


# Create your views here.


md = markdown.Markdown()
search = Search()


def index(request):
    entries = util.list_entries()
    context = {
        "entries": entries,
        "search": search,
    }
    return render(request, "encyc/index.html", context)


def get_page(request, title):
    entry = util.get_entry(title)

    try:
        converted = md.convert(entry)

    except AttributeError:

        context = {
            "message": "No results found"
        }
        return render(request, "encyc/details.html", context)
    context = {
        "entry": converted,
        "title": title,
        "search": search,
    }

    return render(request, "encyc/details.html", context)


def help(request):
    context = {
        "context": {},
        "raw": {},
        "search": search,

    }

    for example in util.list_example():
        converted = md.convert(util.get_example(example))
        raw = util.get_example(example)
        context["context"][example] = converted
        context["raw"][example] = raw

    return render(request, "encyc/help.html", context)


def create_entry(request):
    form = NewEntryForm()

    if request.method == "POST":
        form = NewEntryForm(request.POST or None)

        if form.is_valid():

            title = form.cleaned_data['title']
            content = form.cleaned_data['content']

            util.save_entry(title, content)

            return HttpResponseRedirect(f'/wiki/{title}')

    context = {
        'form': form,
        "search": search,
    }
    return render(request, "encyc/new.html", context)


def update_entry(request, title):

    content = util.get_entry(title)
    initial = {
        "content": content
    }

    form = UpdateForm(initial=initial)

    if request.method == "POST":
        form = UpdateForm(request.POST or None, initial=initial)

        if form.is_valid():

            content = form.cleaned_data['content']

            util.save_entry(title=title, content=content)

            return HttpResponseRedirect(reverse('details', args=(title,)))
    context = {
        "form": form,
        "title": title,
        "search": search,
    }
    return render(request, "encyc/update.html", context)


def random_page(request):
    entries = util.list_entries()

    title = random.choice(entries)
    return get_page(request, title)


def get_search_query(request):

    if request.method == 'GET':

        form = Search(request.GET)

        if form.is_valid():

            search_query = form.cleaned_data.get('search').lower()
            entries = util.list_entries()

            matches = [match for match in entries if search_query in match.lower()]

            if len(matches) == 1 and search_query == matches[0].lower():

                title = matches[0]
                return get_page(request, title=title)

            elif len(matches) > 1:

                context = {
                    "results": matches,
                    "search": search,
                }
                return render(request, "encyc/results.html", context)

            elif len(matches) == 1 and search_query != matches[0]:
                context = {
                    "results": matches,
                    "search": search,
                }

                return render(request, "encyc/results.html", context)

            elif len(matches) == 0:
                context = {
                    "message": "No matching results",
                    "search": search
                }
                return render(request, "encyc/results.html", context)

        else:
            return index(request)

    return index(request)
