from django.conf.urls import url, patterns
from views.view_repository import repository_list

urlpatterns = patterns('',

    url(r'^repository_list/$', repository_list, name='repository_list'),

)