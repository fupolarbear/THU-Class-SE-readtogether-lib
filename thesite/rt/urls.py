from django.conf.urls import patterns, url

from rt import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),

    url(r'^search/$', views.search, name='search'),
    url(r'^book/(\d+)/$', views.book, name='book'),
    url(r'^comment/(\d+)/$', views.comment, name='comment'),
    url(r'^ajax/comment/(\d+)/$', views.ajax_comment, name='ajax_comment'),

    url(r'^login/$', views.login, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^user/$', views.user, name='user'),

    url(r'^queue/(\d+)/$', views.queue, name='queue'),
    url(r'^reborrow/(\d+)/$', views.reborrow, name='reborrow'),

    url(r'^borrow/(\d+)/u(\d+)/$', views.borrow, name='reborrow'),
    url(r'^return/(\d+)/$', views.back, name='return'),
    url(r'^next/(\d+)/$', views.queue_next, name='queue_next'),
    url(r'^readify/(\d+)/$', views.readify, name='readify'),

    url(r'^admin/borrow/$', views.ad_borrow, name='ad_reborrow'),
    url(r'^admin/return/$', views.ad_back, name='ad_return'),
    url(r'^admin/next/$', views.ad_queue_next, name='ad_queue_next'),
    url(r'^admin/readify/$', views.ad_readify, name='ad_readify'),
    url(r'^admin/user/$', views.ad_user, name='ad_user'),
    url(r'^admin/root/$', views.ad_root, name='ad_root'),

    url(r'^info/list/$', views.info, name='info'),
    url(r'^info/(\d+)/$', views.info_detail, name='info_detail'),

    url(r'^rank/$', views.rank, name='rank'),
    url(r'^test/$', views.test, name='test'),
    )
