#-*- encoding:utf-8 -*-
__author__ = 'changjie.fan' '15-3-14'

from django.conf.urls import url, patterns

from xadmin.views import login_page

urlpatterns = patterns('',


    url(r'^$', login_page, name='login_page')
)