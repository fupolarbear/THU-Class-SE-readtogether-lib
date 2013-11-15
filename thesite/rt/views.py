from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from rt.models import Book, Info


PInfo = ['title', 'pub', 'id']
PBook = ['simple_name', 'author', 'simple_version', 'id']
PCopy = ['status', 'id']
'''
XCopy = {
    'where': 'Shelf 01',
    }
Copy.__getitem__ = lambda obj, key: XCopy[key]
'''


def index(request):
    return render(request, 'rt/index.html', {
        'rank': [],
        'news': Info.get_all('news')[:5],
        'guide': Info.get_all('guide')[:5],
        })


def search(request):
    q = request.GET['q']
    return render(request, 'rt/searchResult.html', {
        'q': q,
        'result': Book.search(q),
        })


def book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    copy = book.bookcopy_set.all()
    return render(request, 'rt/book-detail.html', {
        'book': book,
        'copy': copy,
        })


def login(request):
    pass


def register(request):
    pass


def logout(request):
    pass


def user(request):
    pass


def queue(request):
    pass


def info(request):
    return render(request, 'rt/info.html', {
        'news': Info.get_all('news'),
        'guide': Info.get_all('guide'),
        })


def info_detail(request, info_id):
    info = get_object_or_404(Book, pk=info_id)
    return render(request, 'rt/info.html', {
        'info': info,
        'news': Info.get_all('news'),
        'guide': Info.get_all('guide'),
        })


def rank(request):
    pass


def test(request):
    return render(request, 'rt/test.html', {})


def FC(prototype, *args):  # Fake Class
    return dict(zip(prototype, args))
