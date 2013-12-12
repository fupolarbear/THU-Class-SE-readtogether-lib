from datetime import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

from rt.models import Book, Info, MyUser, BookCopy, Borrowing
from rt.forms import RegisterForm, LoginForm


def index(request):
    """Render index page with rank, news and guide."""
    return render(request, 'rt/index.html', {
        'rank': [],
        'news': Info.get_all('news')[:5],
        'guide': Info.get_all('guide')[:5],
        })


def search(request):
    """Search for books."""
    q = request.GET.get('q', '')
    return render(request, 'rt/searchResult.html', {
        'q': q,
        'result': Book.search(q),
        })


def book(request, book_id):
    """Show the detail page for a certain book."""
    book = get_object_or_404(Book, pk=book_id)
    copy = book.bookcopy_set.all()
    return render(request, 'rt/book-detail.html', {
        'book': book,
        'copy': copy,
        })


# Error checking below should work as standard or example for similar views.
# A decorator may be introduced to DRY the code.
# queue should be modified to meet this standard, as well as login/out/reg.
def comment(request, book_id):
    """Add a comment for the book specified by book_id.

    POST:
    content -- the content of the comment.

    Renders JSON with 'status' ('Error' or 'OK') and optionally 'err' for
    detailed (human-readable but English) error message.

    User is derived from the session.
    """
    if request.method != 'POST':
        return HttpResponse(json.dumps({
            'status': 'Error',
            'err': 'Only POST method is accepted.',
            }))
    if not request.user.is_authenticated():
        return HttpResponse(json.dumps({
            'status': 'Error',
            'err': 'Not logged in.',
            }))
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist as err:
        return HttpResponse(json.dumps({
            'status': 'Error',
            'err': 'Invalid book_id.',
            }))
    try:
        content = request.POST['content']
    except MultiValueDictKeyError as err:
        return HttpResponse(json.dumps({
            'status': 'Error',
            'err': 'POST data not found: content.',
            }))
    # call model to post the comment
    # maybe permission errors
    # maybe truncation errors
    # maybe others insert errors
    return HttpResponse(json.dumps({
        'status': 'OK',
        }))


def ajax_comment(request, book_id):
    pass


def login(request):
    """Backend for AJAX login."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                )
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    return HttpResponse(json.dumps({
                        'status': 'OK',
                        'username': user.username,
                        'name': user.myuser.name,
                        }))
            return HttpResponse(json.dumps({
                'status': 'Error',
                'err': 'Login failed.',
                }))
    else:
        form = LoginForm()
    return HttpResponse(json.dumps({
        'status': 'Error',
        'err': 'Login syntax error.',
        'detail': form.errors,
        }))


def register(request):
    """Backend for AJAX register."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            u = MyUser()
            try:
                u.register(
                    form.cleaned_data['username'],
                    form.cleaned_data['password'],
                    form.cleaned_data['email'],
                    form.cleaned_data['name'],
                    )
                user = auth.authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    )
                assert user is not None
                auth.login(request, user)
                return HttpResponse(json.dumps({
                    'status': 'OK',
                    'username': user.username,
                    'name': user.myuser.name,
                    }))
            except IntegrityError as err:
                return HttpResponse(json.dumps({
                    'status': 'Error',
                    'err': 'Username taken.',
                    }))
    else:
        form = RegisterForm()
    return HttpResponse(json.dumps({
        'status': 'Error',
        'err': 'Register syntax error.',
        'detail': form.errors,
        }))


def logout(request):
    """Backend for AJAX logout."""
    auth.logout(request)
    return HttpResponse(json.dumps({
        'status': 'OK',
        }))


@login_required(login_url=urlresolvers.reverse_lazy('rt:index'))
def user(request):
    """Show the user panel page."""
    return render(request, 'rt/user-panel.html', {
        'profile': request.user.myuser,
        })


def queue(request, copy_id):
    """Backend for AJAX book queueing."""
    if request.user.is_authenticated():
        pass  # More permission check
    else:
        return HttpResponse(json.dumps({
            'status': 'Error',
            'err': 'Not logged in.',
            }))
    try:
        copy = BookCopy.objects.get(pk=copy_id)
        Borrowing.queue(request.user.myuser, copy)
        return HttpResponse(json.dumps({
            'status': 'OK',
            'username': request.user.username,
            'copy_id': copy_id,
            }))
    except BookCopy.DoesNotExist as err:
        return HttpResponse(json.dumps({
            'status': 'Error',
            'err': 'Invalid copy_id.',
            'copy_id': copy_id,
            }))


def reborrow(request, book_id):
    pass


def borrow(request, book_id, user_id):
    pass


def back(request, book_id):
    pass


def queue_next(request, book_id):
    pass


def readify(request, book_id):
    pass


def ad_borrow(request):
    pass


def ad_back(request):
    pass


def ad_queue_next(request):
    pass


def ad_readify(request):
    pass


def ad_user(request):
    pass


def ad_root(request):
    pass


def info(request):
    """Show news and guide list."""
    return render(request, 'rt/info.html', {
        'news': Info.get_all('news'),
        'guide': Info.get_all('guide'),
        })


def info_detail(request, info_id):
    """Show the content of the specific news of guide."""
    info = get_object_or_404(Info, pk=info_id)
    return render(request, 'rt/info.html', {
        'info': info,
        'news': Info.get_all('news'),
        'guide': Info.get_all('guide'),
        })


def rank(request):
    """Show the rank page. Uncomplete."""
    return render(request, 'rt/rank.html', {})


def test(request):
    """Dummy page for various on-hand snippets."""
    return render(request, 'rt/test.html', {'l': LoginForm, 'r': RegisterForm})


def FC(prototype, *args):
    """Fake a object-like variable for templates based on the prototype."""
    return dict(zip(prototype, args))
