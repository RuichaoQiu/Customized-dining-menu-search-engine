from django.conf.urls import patterns, url

from dm import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^recordmanager/$', views.recordmanager, name='recordmanager'),
    url(r'^searchquery/$', views.searchquery, name='searchquery'),
    url(r'^(?P<choice>\d+)/review/$', views.review, name='review'),
    url(r'^(?P<choice>\d+)/route/$', views.route, name='route'),
)