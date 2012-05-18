# -*- coding:Utf-8 -*-

from datetime import datetime
from urllib2 import urlopen, URLError
from django.db import models
from re import sub
from oice.langdet import langdet
from mechanize import Browser
from utils import encoding_sucks


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

    def get_langue(self):
        if self.langue is not None:
            return self.langue

        try:
            text = urlopen(self.url).read()
            text = sub("[^\w ]", lambda x: "", text)
            lang = langdet.LanguageDetector.detect(text).iso.upper()
            if lang in ('FR', 'EN', 'ES'):
                self.langue = lang
                self.save()
                return lang
        except URLError:
            self.langue = ""
            self.save()
            return self.langue

    def get_title(self):
        if self.title is not None:
            return self.title

        b = Browser()
        site = ".".join(map(lambda x: x.capitalize(), self.url.split("/")[2].replace("www.", "").split(".")[:-1]))
        try:
            b.open(self.url)
            return "[%s] %s" % (site.encode("Utf-8"), encoding_sucks(b.title()))
        except URLError:
            self.title = "[%s] Error: couldn't fetch the title" % site
            self.save()
            return self.title
