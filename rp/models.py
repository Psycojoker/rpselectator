# -*- coding:Utf-8 -*-

from django.db import models

class RP(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    url = models.URLField(unique=True)
    published = models.BooleanField(default=False)
    langue = models.IntegerField(max_length=2, choices=(('en', 'English'), ('fr', 'Français')), null=True)

    def __unicode__(self):
        return "%s - %s" % (self.title if self.title else "No title", self.url)
