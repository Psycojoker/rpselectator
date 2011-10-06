# -*- coding:Utf-8 -*-

from datetime import datetime

from django.db import models

class RP(models.Model):
    title = models.CharField(max_length=90, null=True, blank=True)
    url = models.URLField(unique=True)
    published = models.NullBooleanField(default=None, null=True)
    langue = models.CharField(max_length=2, null=True, blank=True)
    datetime = models.DateTimeField(editable=False)
    published_date = models.DateTimeField(default=None, null=True, editable=False)

    def __unicode__(self):
        return "%s - %s" % (self.title if self.title else "No title", self.url)

    def save(self, *args, **kwargs):
        if self.published and not self.published_date:
            self.published_date = datetime.now()
        super(RP, self).save(*args, **kwargs)
