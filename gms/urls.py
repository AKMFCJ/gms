#-*- encoding:utf-8 -*-
from django.conf.urls import patterns, include, url
from xadmin.views import login_page

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'gms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', login_page),
    url(r'^xadmin/', include('xadmin.urls', namespace='xadmin')),

)
