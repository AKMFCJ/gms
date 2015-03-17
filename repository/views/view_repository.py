#-*- encoding:utf-8 -*-
#
#create date: 2015-03-17
#author: roy
#git repository manager view
#

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from ..models import Repository


def repository_list(request):
    """all repository list"""

    return render(request, 'repository/repository_page.html',
        {'repositories': list(Repository.objects.filter(active=True).order_by('-created_date'))})
