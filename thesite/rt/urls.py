from django.conf.urls import patterns, url

from rt import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^search/$', views.search, name='search'),
    url(r'^book/(\d+)/$', views.book, name='book'),

    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user/$', views.user, name='user'),

    url(r'^queue/(\d+)/$', views.queue, name='queue'),

    url(r'^info/list/$', views.info, name='info'),
    url(r'^info/(\d+)/$', views.info_detail, name='info_detail'),

    url(r'^rank/$', views.rank, name='rank'),
    url(r'^test/$', views.test, name='test'),
    )
