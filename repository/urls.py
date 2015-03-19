from django.conf.urls import url, patterns
from views.view_repository import repository_list, add_repository

urlpatterns = patterns('',

    url(r'^repository_list/$', repository_list, name='repository_list'),
    url(r'^add_repository/$', add_repository, name='add_repository'),

)