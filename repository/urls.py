from django.conf.urls import url, patterns
from views.view_repository import *

urlpatterns = patterns('',

    url(r'^repository_list/$', repository_list, name='repository_list'),
    url(r'^add_repository/$', add_repository, name='add_repository'),
    url(r'^repository_main/(?P<repo_id>\d+)$', repository_main, name='repository_main'),
    url(r'^repository_file_content/(?P<repo_id>\d+)$', repository_file_content, name='repository_file_content'),
)