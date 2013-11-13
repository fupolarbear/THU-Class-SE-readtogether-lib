from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'rt/index.html', {'username': 'Django'})


def info(request):
    return render(request, 'rt/info.html', {})


def search(request):
    return render(request, 'rt/searchResult.html', {})
