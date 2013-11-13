from django.conf.urls import patterns, url

from rt import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^info/$', views.info, name='info'),
    url(r'^search/$', views.search, name='searchResult'),
    url(r'^test/$', views.test, name='test'),
    )
