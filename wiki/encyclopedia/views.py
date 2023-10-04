from django.shortcuts import render

from . import util
import markdown2
import random

def markdown_to_html(name):
    file = util.get_entry(name)

    if file == None:
        return None

    converted_file = markdown2.markdown(file)
    return converted_file


def error_page(request, message):
    return render(request, "encyclopedia/error.html", {"context": message})


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


def dynamic_look_up(request, slug):
    file = markdown_to_html(slug)

    if file == None:
        return error_page(request, "Page not found")

    return render(request, "encyclopedia/template.html", {
        'title': slug,
        'content': file})


def search(request):
    if request.method == "POST":
        query_dict = request.POST
        markdown_content = query_dict.get('q')

        html_content = markdown_to_html(markdown_content)
        if html_content is not None:
            return render(request, "encyclopedia/template.html", {
                'title': markdown_content,
                'content': html_content})
        else:
            entries = util.list_entries()
            recommendation = []
            for entry in entries:
                if markdown_content.lower() in entry.lower():
                    recommendation.append(entry)
            return render(request, "encyclopedia/search.html", {"entries": recommendation})

    return error_page(request, "Page not found")


def new_page(request):
    if request.method == "GET":
        # Just want to see the page
        return render(request, "encyclopedia/new_page.html", {})
    else:
        query_dict = request.POST
        title = query_dict.get('title')
        content = query_dict.get('content')

        if util.get_entry(title):
            return render(request, "encyclopedia/error.html", {"context": "The page already exist"})

        util.save_entry(title, content)
        return dynamic_look_up(request, title)


def edit_page(request):
    if request.method == "POST":
        query_dict = request.POST
        title = query_dict.get('entry_title')
        content = util.get_entry(title)

        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })

    return error_page(request, "Page can't be edited. Please try again")


def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']

        util.save_entry(title, content)

        return dynamic_look_up(request, title)

    return error_page(request , "Page can't be edited. Please try again")

def random_page(request):
    list = util.list_entries()
    random_page = random.choice(list)
    return dynamic_look_up(request, random_page)
