# -*- coding:Utf-8 -*-

import threading
from datetime import datetime
from urllib2 import urlopen, URLError
from django.db import models
from mechanize import Browser
from utils import encoding_sucks, get_langue_from_html, format_site_from_url, clean_title


class RP(models.Model):
    title = models.CharField(max_length=119, null=True, blank=True)
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
            lang = get_langue_from_html(urlopen(self.url).read())
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

        site = format_site_from_url(self.url)

        try:
            result = []
            def process_website(result):
                browser = Browser()
                browser.set_handle_robots(False)
                browser.open(self.url, timeout=9.00)
                result.append(browser)
            thread = threading.Thread(target=process_website, args=(result,))
            thread.start()
            thread.join(timeout=10)
            if len(result) == 0:
                raise Exception("browser timedout or failed")
            browser = result[0]
            self.title = "[%s] %s" % (site.encode("Utf-8"), encoding_sucks(clean_title(browser.title())).lower().capitalize())
            self.langue = get_langue_from_html(browser.response().get_data())
            self.save()
            return self.title
        except Exception as e:
            print "Error: fail on %s: %s" % (self.url, e)
            self.title = "[%s] Error: couldn't fetch the title" % site
            self.save()
            return self.title
