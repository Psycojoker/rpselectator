from time import sleep
from urllib2 import urlopen
from datetime import datetime
from django.http import HttpResponse

from models import RP

def fill(request):
    def get_urls(url):
        a = 0

        urls = ""
        tries = 0
        while not urls:
            try:
                urls = urlopen(url).read()
            except Exception, e:
                print "Malheur !: " + e
                tries += 1
                if tries > 3:
                    return 0
                sleep(1)

        for url in urls.split("\n"):
            if not url.strip():
                continue
            date, url = url.split(" ", 1)
            if not RP.objects.filter(url=url):
                RP.objects.create(url=url, datetime=datetime.fromtimestamp(int(date)))
                a += 1
        return a

    a = 0
    a += get_urls("http://nurpa.be/log")
    #a += get_urls("http://nurpa.be/log-archive")
    return HttpResponse("%s new rp items" % a)
