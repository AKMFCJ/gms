#-*- encoding:utf-8 -*-
__author__ = 'changjie.fan' '15-3-14'

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.contrib.auth import authenticate, logout as user_logout, login as user_login
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
    if user:
        user_login(request, user)
        print username
        return render(request, 'xadmin/index.html', {'username': username})
    else:
        user = User.objects.filter(username=username)
        if user:
            return render(request, 'xadmin/login.html', {'error_message': '密码不正确!'})
        else:
            return render(request, 'xadmin/login.html', {'error_message': '用户名不存在!'})


def sys_logout(request):
    """注销系统"""

    user_logout(request)
    return render(request, 'xadmin/login.html')


def sys_setting_page(request):
    """系统设置页面"""

    return render(request, 'xadmin/setting.html')