from datetime import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core import urlresolvers
from django.db.utils import IntegrityError
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator

from rt.models import Book, Info, MyUser, BookCopy, Borrowing, Comment, Rank
from rt.forms import RegisterForm, LoginForm
from rt.views_utils import FC, render_JSON_OK, render_JSON_Error, \
    POST_required, login_required_JSON, catch_404_JSON, get_page, \
    catch_PermException_JSON


COMMENT_PAGE_SIZE_0 = 0
COMMENT_PAGE_SIZE = 2


def index(request):
    """Show index page.

    GET:

    Renders rt/index.html with:
    rank  -- latest rank list by rate
    news  -- latest 5 pieces of news
    guide -- latest 5 pieces of guide
    """
    return render(request, 'rt/index.html', {
        'rank': Rank.get_top(),
        'news': Info.get_all('news')[:5],
        'guide': Info.get_all('guide')[:5],
        })


def search(request):
    """Search for books.

    GET:
    q -- the query string

    Renders rt/searchResult.html with:
    q      -- the query string
    result -- search result, as a list of books
    """
    q = request.GET.get('q', '')
    return render(request, 'rt/searchResult.html', {
        'q': q,
        'result': Book.search(q),
        })


def book(request, book_id):
    """Show the detail page for a certain book.
    
    GET:

    Renders rt/book-detail.html with:
    book             -- the book object
    copy             -- a list of all copies of this book
    comment_count    -- number of comments on this book
    comment & range5 -- latest comment list, and template helper
    """
    book = get_object_or_404(Book, pk=book_id)
    copy = book.bookcopy_set.all()
    comment = book.comment_set.all()[:COMMENT_PAGE_SIZE_0]
    return render(request, 'rt/book-detail.html', {
        'book': book,
        'copy': copy,
        'comment_count': book.comment_set.all().count(),
        'comment': comment,
        'range5': range(1, 6),
        })


# Error checking below should work as standard or example for similar views.
# A decorator may be introduced to DRY the code.
# queue should be modified to meet this standard, as well as login/out/reg.
@POST_required('title', 'content', 'rate', 'spoiler')
@login_required_JSON()
@catch_404_JSON
def comment(request, book_id):
    """Add a comment for the book specified by book_id.

    POST:
    title   -- the title of the comment
    content -- the content of the comment
    rate    -- the rate associated with the comment
    spoiler -- whether this comment is a spoiler

    Renders JSON: (besides 'status' or 'err')

    User is derived from the session.
    """
    myuser = request.user.myuser
    book = get_object_or_404(Book, pk=book_id)
    title = request.POST['title']
    content = request.POST['content']
    rate = request.POST['rate']
    if rate not in {str(i) for i in range(1, 6)}:
        return render_JSON_Error('Invalid rate.')
    rate = int(rate)
    spoiler = request.POST['spoiler'] == 'true'
    Comment.add(myuser, book, title, content, rate, spoiler)
    return render_JSON_OK({})


def ajax_comment(request, book_id):
    """Fetch comments for the book specified by book_id.

    GET:
    page -- the desired page. 0 is reserved for the default ones returned on
            the book page. The first load operation should use 1 (default).
            Large page numbers exceeds the total number returns empty list.
    Other parameters may be used such as 'last_date' or 'last_id', so it's not
    a good idea to put them into URL.

    Renders rt/fetch_comment.html for AJAX load with:
    comment -- (on 'OK') a list of comments
      myuser   -- the user who posted this comment
      datetime -- datetime when the comment was posted
      title    -- title of the comment
      content  -- content of the comment
      rate     -- rate of the comment
      spoiler  -- whether this comment is a spoiler

    Everyone can view comments.
    """
    book = get_object_or_404(Book, pk=book_id)
    page = request.GET.get('page', 1)
    comment_list = book.comment_set.all()[COMMENT_PAGE_SIZE_0:]
    paginator = Paginator(comment_list, COMMENT_PAGE_SIZE)
    comment = get_page(paginator, page)
    return render(request, 'rt/fetch_comment.html', {
        'comment': comment,
        'range5': range(1, 6),
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
    myuser = request.user.myuser
    if myuser.get_admin_type() == 'book manager':
        return redirect('rt:ad_book')
    return render(request, 'rt/user-panel.html', {
        'profile': myuser,
        'book_borrowing': myuser.get_all_borrowing(),
        'book_queue': myuser.get_all_queue(),
        'book_borrowed': myuser.get_all_borrowed(),
        'comment': myuser.comment_set.all(),
        'range5': range(1, 6),
        })


@POST_required()
@login_required_JSON()
@catch_404_JSON
@catch_PermException_JSON
def queue(request, copy_id):
    """Backend for AJAX book queueing."""
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.queue(request.user.myuser, copy)
    return render_JSON_OK({
        'username': request.user.username,
        'copy_id': copy_id,
        })


@POST_required()
@login_required_JSON()
@catch_404_JSON
@catch_PermException_JSON
def reborrow(request, copy_id):
    """Backend for AJAX book reborrow."""
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.reborrow(request.user.myuser, copy)
    return render_JSON_OK({
        'username': request.user.username,
        'copy_id': copy_id,
        })


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def borrow(request, copy_id, myuser_id):
    copy = get_object_or_404(BookCopy, pk=copy_id)
    myuser = get_object_or_404(MyUser, pk=myuser_id)
    Borrowing.borrow(myuser, copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def back(request, copy_id):
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.return_book(copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def queue_next(request, copy_id, myuser_id):
    copy = get_object_or_404(BookCopy, pk=copy_id)
    myuser = get_object_or_404(MyUser, pk=myuser_id)
    Borrowing.queue_next(myuser, copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def readify(request, copy_id):
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.readify(copy)
    return render_JSON_OK({})


@POST_required()
@login_required_JSON('book manager')
@catch_404_JSON
@catch_PermException_JSON
def disappear(request, copy_id):
    copy = get_object_or_404(BookCopy, pk=copy_id)
    Borrowing.disappear(copy)
    return render_JSON_OK({})


@login_required(login_url=urlresolvers.reverse_lazy('rt:index'))
def ad_book(request):
    return render(request, 'rt/book-manager-panel.html', {})


def ad_user(request):
    pass


def ajax_myuser(request):
    q_myuser = request.GET.get('q', '')
    return render(request, 'rt/fetch_myuser.html', {
        'myuser_list': MyUser.search(q_myuser),
        })


def ajax_book(request, book_id):
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
    """Show the rank page."""
    return render(request, 'rt/rank.html', {
        'rank_by_borrow': Rank.get_top(0),
        'rank_by_comment': Rank.get_top(1),
        'rank_by_rate': Rank.get_top(2),
        'range5': range(1, 6),
        })


def test(request):
    """Dummy page for various on-hand snippets."""
    comment = Comment.objects.all()
    return render(request, 'rt/fetch_comment.html', {
        'comment': comment,
        'range5': range(1, 6),
        })
