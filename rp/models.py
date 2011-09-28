# -*- coding:Utf-8 -*-

from django.db import models

class RP(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(unique=True)
    published = models.BooleanField(default=False)
    langue = models.CharField(max_length=3, null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.title if self.title else "No title", self.url)
