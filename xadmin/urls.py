#-*- encoding:utf-8 -*-
__author__ = 'changjie.fan' '15-3-14'

from django.conf.urls import url, patterns

from xadmin.views import login_page, sys_login, sys_setting_page

urlpatterns = patterns('',
    url(r'^sys_login/$', sys_login, name='sys_login'),
    url(r'^sys_setting/$', sys_setting_page, name='sys_setting_page'),

)