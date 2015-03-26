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
from repository.lib.repo_options import RepoOptions


def repository_list(request):
    """all repository list"""

    repositories = [(index+1, item) for index, item in enumerate(Repository.objects.filter(active=True).order_by('-created_date'))]
    return render(request, 'repository/repository_page.html',
        {'repositories': repositories})


def repository_main(request, repo_id, reference_name):
    """显示仓库目录信息"""

    repository = Repository.objects.get(id=repo_id)
    repo_option = RepoOptions(repository.path)
    repo = repo_option.repo
    result = []
    last_commit = ''

    if not reference_name:
        if repo.references:
            reference_name = repo.references[0].name

    if reference_name:
        last_commit = repo.commit(reference_name)
        file_list = [tmp.split('\t') for tmp in repo_option.show(reference_name, '/').split('\n') if tmp]

        for file_info in file_list:
            record = {}
            tmp = file_info[0].split(' ')
            record['name'] = file_info[1]
            record['type'] = tmp[1]
            record['object_id'] = tmp[2]
            record['path'] = ''
            log_info = repo_option.file_log(reference_name, record['name']).split('$$')
            if log_info:
                print log_info
                record['committed_date'] = log_info[0]
                record['message'] = log_info[1]
            else:
                record['committed_date'] = ''
                record['message'] = ''
            result.append(record)


    print reference_name
    return render(request, 'repository/repository.html', {'repository': repository, 'references': repo.references,
        'current_reference': reference_name, 'last_commit': last_commit, 'file_list': result})


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