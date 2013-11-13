# encoding: utf-8
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    rank = [
        ('Mark', 'Otto', '@mdo'),
        ('Jacob', 'Thornton', '@fat'),
        ('Larry', 'the Bird', '@twitter'),
        ]
    return render(request, 'rt/index.html', {
        'top10': rank,
        'information': rank,
        'help': rank,
        })


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


def search(request):
    Book = ['title', 'author', 'year']
    return render(request, 'rt/searchResult.html', {
        'result': [
            FC(Book, '哈利波特与魔法石头', 'JK罗琳', '2000'),
            FC(Book, '哈利波特与密室', 'JK罗琳', '2001'),
            FC(Book, '哈利波特与阿兹卡班的囚徒', 'JK罗琳', '2002'),
            FC(Book, '哈利波特与火焰杯', 'JK罗琳', '2003'),
            FC(Book, '哈利波特与凤凰社', 'JK罗琳', '2004'),
            FC(Book, '哈利波特与混血王子', 'JK罗琳', '2005'),
            FC(Book, '哈利波特与死亡圣器', 'JK罗琳', '2006'),
            FC(Book, '哈利波特与软工作业', 'JK罗琳', '2013'),
            FC(Book, '哈利波特与伏地魔不得不说的故事', 'JK罗琳', '2013'),
            ],
        })


def test(request):
    return render(request, 'rt/test.html', {})


def FC(prototype, *args):  # Fake Class
    return dict(zip(prototype, args))
