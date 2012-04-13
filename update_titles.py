# -*- coding:Utf-8 -*-
import mechanize
import urllib2
from rp.models import RP
from rp.views import encoding_sucks

b = mechanize.Browser()
for rp in RP.objects.filter(title=None, published=None):
    choose_biggest = lambda choices: max(choices, key=lambda x: len(x))
    try:
        b.open(rp.url)
        site = ".".join(map(lambda x: x.capitalize(), rp.url.split("/")[2].replace("www.", "").split(".")[:-1]))
        title = encoding_sucks(b.title())
        title = choose_biggest(title.split(" - "))
        title = choose_biggest(title.split(" | "))
        title = choose_biggest(title.split(" ["))
        title = choose_biggest(title.split(u" « "))
        title = choose_biggest(title.split(u" – "))
        rp.title = "[%s] %s" % (site.encode("Utf-8"), title)
        rp.save()
        print rp.title
    except (urllib2.URLError, mechanize._mechanize.BrowserStateError):
        continue
