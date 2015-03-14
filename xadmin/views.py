#-*- encoding:utf-8 -*-
__author__ = 'changjie.fan' '15-3-14'

from django.shortcuts import render, HttpResponse, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User


def login_page(request):
    """系统登录页面"""
    return render(request, 'xadmin/login.html')


def sys_login(request):
    """用户登录"""

    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    #remember_me = request.POST.get('remember_me', '')

    user = authenticate(username=username, password=password)
    print user
    if user:
        #if remember_me == 'on':
        #    request.session.set_expiry(300)
        return HttpResponse('success')
    else:
        user = User.objects.filter(username=username)
        if user:
            return render(request, 'xadmin/login.html', {'error_message': '密码不正确!'})
        else:
            return render(request, 'xadmin/login.html', {'error_message': '用户名不存在!'})