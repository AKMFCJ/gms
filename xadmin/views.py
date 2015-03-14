#-*- encoding:utf-8 -*-
__author__ = 'changjie.fan' '15-3-14'

from django.shortcuts import render, HttpResponse, Http404


def login_page(request):
    return render(request, 'xadmin/login.html')