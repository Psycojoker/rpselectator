# -*- coding:Utf-8 -*-
import mechanize
import urllib2
from rp.models import RP
from rp.utils import clean_title, format_site_from_url, get_langue_from_html

browser = mechanize.Browser()
for rp in RP.objects.filter(title=None, published=None):
    try:
        browser.open(rp.url)
        site = format_site_from_url(rp.url)
        title = clean_title(browser.title())
        rp.langue = get_langue_from_html(browser.response().get_data())
        rp.title = "[%s] %s" % (site.encode("Utf-8"), title)
        rp.save()
        print rp.title
    except (urllib2.URLError, mechanize._mechanize.BrowserStateError), e:
        print "Error on:", rp.url, ":", e
