# -*- coding: utf-8 -*-

from django.contrib.auth.models import Group
from django.db import models


class Resources(models.Model):
    name = models.CharField(max_length=255, null=True)
    uuid = models.CharField(max_length=255, null=True)
    size = models.BigIntegerField(default=0)
    uploaded = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
