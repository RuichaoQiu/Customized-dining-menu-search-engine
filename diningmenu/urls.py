from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'diningmenu.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^dm/', include('dm.urls', namespace="dm")),
    url(r'^admin/', include(admin.site.urls)),
)
