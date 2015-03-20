#-*- encoding:utf-8 -*-
#
#create date: 2015-03-17
#author: roy
#git repository manager database model
#

from django.db import models


class Repository(models.Model):

    name = models.CharField(max_length=300)
    path = models.CharField(max_length=500)
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField()
    description = models.CharField(max_length=500)

    def __unicode__(self):
        return u"%s" % self.name

    class Meta:
        db_table = 'repository_repository'
