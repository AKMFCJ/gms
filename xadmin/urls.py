#-*- encoding:utf-8 -*-
__author__ = 'changjie.fan' '15-3-14'

from django.conf.urls import url, patterns

from xadmin.views import login_page, sys_login

urlpatterns = patterns('',
    url(r'^sys_login/$', sys_login, name='sys_login'),
)