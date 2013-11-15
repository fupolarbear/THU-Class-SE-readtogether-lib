from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render

from rt.models import Book


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
        'news': [
            FC(PInfo, 'Title of news 1', datetime(2013, 11, 15), 12),
            FC(PInfo, 'Title of news 2', datetime(2012, 2, 29), 7),
            ],
        'guide': [
            FC(PInfo, 'Title of guide 1', datetime(2010, 1, 1), 25),
            ],
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
    TC = ['title', 'content']  # Title & Content
    one = FC(TC, 'Alice has been fined 5RMB', '''Leggings occaecat craft beer
        farm-to-table, raw denim aesthetic synth nesciunt you probably haven't
        heard of them accusamus labore sustainable VHS.''')
    return render(request, 'rt/info.html', {
        'news': [
            FC(TC, 'Harry Potter 8 has been introduced into the library\
                already', '''Anim pariatur cliche reprehenderit, enim eiusmod
                high life accusamus terry richardson ad squid. 3 wolf moon
                officia aute, non cupidatat skateboard dolor brunch. Food truck
                quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon tempor,
                sunt aliqua put a bird on it squid single-origin coffee nulla
                assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft
                beer labore wes anderson cred nesciunt sapiente ea proident.
                Ad vegan excepteur butcher vice lomo. Leggings occaecat craft
                beer farm-to-table, raw denim aesthetic synth nesciunt you
                probably haven\'t heard of them accusamus labore sustainable
                VHS.'''),
            FC(TC, 'the library will be closed temporary because of double\
                eleven festival', '''Anim pariatur cliche reprehenderit, enim
                eiusmod high life accusamus terry richardson ad squid. 3 wolf
                moon officia aute, non cupidatat skateboard dolor brunch. Food
                truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon
                tempor, sunt aliqua put a bird on it squid single-origin coffee
                nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica,
                craft beer labore wes anderson cred nesciunt sapiente ea
                proident. Ad vegan excepteur butcher vice lomo. Leggings
                occaecat craft beer farm-to-table, raw denim aesthetic synth
                nesciunt you probably haven't heard of them accusamus labore
                sustainable VHS.'''),
            FC(TC, 'the library will be closed temporary because of double\
                eleven festival', '''Leggings occaecat craft beer
                farm-to-table, raw denim aesthetic synth nesciunt you probably
                haven't heard of them accusamus labore sustainable VHS.'''),
            one, one, one, one, one, one,
            ],
        'guide': [
            FC(TC, 'How to borrow', '''Anim pariatur cliche reprehenderit,
                enim eiusmod high life accusamus terry richardson ad squid. 3
                wolf moon officia aute, non cupidatat skateboard dolor brunch.
                Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon
                tempor, sunt aliqua put a bird on it squid single-origin coffee
                nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica,
                craft beer labore wes anderson cred nesciunt sapiente ea
                proident. Ad vegan excepteur butcher vice lomo. Leggings
                occaecat craft beer farm-to-table, raw denim aesthetic synth
                nesciunt you probably haven't heard of them accusamus labore
                sustainable VHS.
                Anim pariatur cliche reprehenderit, enim eiusmod high life
                accusamus terry richardson ad squid. 3 wolf moon officia aute,
                non cupidatat skateboard dolor brunch. Food truck quinoa
                nesciunt laborum eiusmod. Brunch 3 wolf moon tempor, sunt
                aliqua put a bird on it squid single-origin coffee nulla
                assumenda shoreditch et. Nihil anim keffiyeh helvetica, craft
                beer labore wes anderson cred nesciunt sapiente ea proident.
                Ad vegan excepteur butcher vice lomo. Leggings occaecat craft
                beer farm-to-table, raw denim aesthetic synth nesciunt you
                probably haven't heard of them accusamus labore sustainable
                VHS.'''),
            FC(TC, 'Open time', '''Anim pariatur cliche reprehenderit, enim
                eiusmod high life accusamus terry richardson ad squid. 3 wolf
                moon officia aute, non cupidatat skateboard dolor brunch. Food
                truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon
                tempor, sunt aliqua put a bird on it squid single-origin coffee
                nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica,
                craft beer labore wes anderson cred nesciunt sapiente ea
                proident. Ad vegan excepteur butcher vice lomo. Leggings
                occaecat craft beer farm-to-table, raw denim aesthetic synth
                nesciunt you probably haven't heard of them accusamus labore
                sustainable VHS.'''),
            FC(TC, 'Bring your money', '''Anim pariatur cliche reprehenderit,
                enim eiusmod high life accusamus terry richardson ad squid. 3
                wolf moon officia aute, non cupidatat skateboard dolor brunch.
                Food truck quinoa nesciunt laborum eiusmod. Brunch 3 wolf moon
                tempor, sunt aliqua put a bird on it squid single-origin coffee
                nulla assumenda shoreditch et. Nihil anim keffiyeh helvetica,
                craft beer labore wes anderson cred nesciunt sapiente ea
                proident. Ad vegan excepteur butcher vice lomo. Leggings
                occaecat craft beer farm-to-table, raw denim aesthetic synth
                nesciunt you probably haven't heard of them accusamus labore
                sustainable VHS.'''),
            ],
        })


def info_detail(request):
    pass


def rank(request):
    pass


def test(request):
    return render(request, 'rt/test.html', {})


def FC(prototype, *args):  # Fake Class
    return dict(zip(prototype, args))
