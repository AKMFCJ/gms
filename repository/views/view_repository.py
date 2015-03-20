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
from gms.utils import get_current_time


def repository_list(request):
    """all repository list"""

    repositories = [(index+1, item) for index, item in enumerate(Repository.objects.filter(active=True).order_by('-created_date'))]
    return render(request, 'repository/repository_page.html',
        {'repositories': repositories})


def repository_main(request, repo_id):
    """显示仓库目录信息"""

    repository = Repository.objects.get(id=repo_id)

    return render(request, 'repository/repository.html', {'repository': repository})


def add_repository(request):
    """create new repository"""

    repository_name = request.POST.get('repository_name', '')
    repository_description = request.POST.get('repository_description', '')

    repository_path = os.path.join(GIT_REPOSITORIES, repository_name)
    if not repository_path.endswith('.git'):
        repository_path = ''.join([repository_path, '.git'])
    os.makedirs(repository_path)
    repo = Repo.init(repository_path, bare=True)

    repository = Repository(name=repository_name, path=repository_path, created_date=get_current_time(), description=repository_description)
    repository.save()

    return HttpResponseRedirect('/repository/repository_list/')