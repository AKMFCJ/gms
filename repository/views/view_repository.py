#-*- encoding:utf-8 -*-
#
#create date: 2015-03-17
#author: roy
#git repository manager view
#
import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from git import *

from ..models import Repository
from gms.settings import GIT_REPOSITORIES


def repository_list(request):
    """all repository list"""

    return render(request, 'repository/repository_page.html',
        {'repositories': list(Repository.objects.filter(active=True).order_by('-created_date'))})


def add_repository(request):
    """create new repository"""

    repository_name = request.POST.get('repository_name', '')
    repository_description = request.POST.get('repository_description', '')

    repository_path = os.path.join(GIT_REPOSITORIES, repository_name)
    if not repository_path.endswith('.git'):
        repository_path = ''.join([repository_path, '.git'])
    os.makedirs(repository_path)
    repo = Repo.init(repository_path, bare=True)


    return HttpResponseRedirect('/repository/repository_list/')