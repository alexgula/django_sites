from django.db.models import Max
from django.template import loader, RequestContext
from django.http import HttpResponse
from django.shortcuts import get_list_or_404, get_object_or_404
from django.views.decorators.cache import cache_page
from .models import Book, Part

def book_list(request):
    books = Book.objects.all()
    t = loader.get_template("book_list.html")
    c = RequestContext(request, {'object_list': books})
    return HttpResponse(t.render(c))

def _build_multilevel_list(parts, parts_len, current_level, start_index):
    result = []
    i = start_index
    while i < parts_len:
        title, level, page_num, slug = parts[i]
        if level == current_level:
            children, i = _build_multilevel_list(parts, parts_len, current_level+1, i+1)
            part = {'part_title': title, 'children': children, 'level': level, 'page_num': page_num, 'slug': slug}
            result.append(part)
        else:
            return result, i
    return result, i

def build_multilevel_list(parts):
    """
    [
        ('part1', 1),
        ('part2', 2),
        ('part3', 2),
        ('part4', 1),
    ]
    [
        {'part_title': 'part1', 'children': [
            {'part_title': 'part2', 'children': []},
            {'part_title': 'part3', 'children': []},
        ]},
        {'part_title': 'part4', 'children': []},
    ]
    """
    result, i = _build_multilevel_list(parts, len(parts), 1, 0)
    return result

@cache_page(60 * 5)
def book_details(request, book_slug, page_num):
    page_num = int(page_num)
    parts = get_list_or_404(Part, in_book__slug=book_slug, page_num=page_num)
    all_parts = Part.objects.filter(in_book__slug=book_slug).values_list('title', 'level', 'page_num', 'slug')
    contents = build_multilevel_list(all_parts)
    pages = Part.objects.filter(in_book__slug=book_slug).aggregate(Max('page_num'))
    book = get_object_or_404(Book, slug=book_slug)
    prev_num = page_num - 1 if page_num > 1 else None
    next_num = page_num + 1 if page_num < pages['page_num__max'] else None
    t = loader.get_template("book_details.html")
    c = RequestContext(request, {'parts': parts, 'book': book, 'pages': pages, 'prev_num': prev_num, 'next_num': next_num, 'contents': contents})
    return HttpResponse(t.render(c))
