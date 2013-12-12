from datetime import datetime

from django.shortcuts import render, get_object_or_404
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError

from rt.models import Book, Info, MyUser, BookCopy, Borrowing
from rt.forms import RegisterForm, LoginForm
from rt.views_utils import FC, render_JSON_OK, render_JSON_Error, \
    POST_required, login_required_JSON, catch_404_JSON


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
@POST_required('content')
@login_required_JSON
@catch_404_JSON
def comment(request, book_id):
    """Add a comment for the book specified by book_id.

    POST:
    content -- the content of the comment.

    Renders JSON: (besides 'status' or 'err')

    User is derived from the session.
    """
    book = get_object_or_404(Book, pk=book_id)
    content = request.POST['content']
    # call model to post the comment
    # maybe permission errors
    # maybe truncation errors
    # maybe others insert errors
    return render_JSON_OK({})


@catch_404_JSON
def ajax_comment(request, book_id):
    """Fetch comments for the book specified by book_id.

    GET:
    page -- the desired page. 0 is reserved for the default ones returned on
            the book page. The first load operation should use 1 (default).
            Large page numbers exceeds the total number returns empty list.
    Other parameters may be used such as 'last_date' or 'last_id', so it's not
    a good idea to put them into URL.

    Renders JSON: (besides 'status' or 'err')
    comment -- (on 'OK') a list of comments
      name     -- the name of the user
      datetime -- datetime when the comment was posted
      title    -- title of the comment
      content  -- content of the comment
      rate     -- rate of the comment
      spoiler  -- whether this comment is a spoiler

    Everyone can view comments.
    """
    book = get_object_or_404(Book, pk=book_id)
    page = request.GET.get('page', 1)
    CMT = ['name', 'datetime', 'title', 'content', 'rate', 'spoiler']
    return render_JSON_OK({
        'comment': [
            FC(
                CMT, 'Tester', '2013-12-12 12:12:12', 'Title', 'Content',
                3, True,
                ),
            FC(
                CMT, 'SuperBug', '2013-12-12 12:12:12', 'No Title', 'Super!',
                4, False,
                ),
            ],
        })


@POST_required()
def login(request):
    """Backend for AJAX login."""
    form = LoginForm(request.POST)
    if form.is_valid():
        user = auth.authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
            )
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return render_JSON_OK({
                    'username': user.username,
                    'name': user.myuser.name,
                    })
        return render_JSON_Error('Login failed.')
    return render_JSON_Error('Login syntax error.', {
        'detail': form.errors,
        })


@POST_required()
def register(request):
    """Backend for AJAX register."""
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
            return render_JSON_OK({
                'username': user.username,
                'name': user.myuser.name,
                })
        except IntegrityError as err:
            return render_JSON_Error('Username taken.')
    return render_JSON_Error('Register syntax error.', {
        'detail': form.errors,
        })


def logout(request):
    """Backend for AJAX logout."""
    auth.logout(request)
    return render_JSON_OK({})


@login_required(login_url=urlresolvers.reverse_lazy('rt:index'))
def user(request):
    """Show the user panel page."""
    return render(request, 'rt/user-panel.html', {
        'profile': request.user.myuser,
        })


@POST_required()
@login_required_JSON
@catch_404_JSON
def queue(request, copy_id):
    """Backend for AJAX book queueing."""
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.queue(request.user.myuser, copy)
    return render_JSON_OK({
        'username': request.user.username,
        'copy_id': copy_id,
        })


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
