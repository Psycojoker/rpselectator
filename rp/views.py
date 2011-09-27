# Create your views here.

from django.http import HttpResponse

from models import RP

from urllib2 import urlopen

def fill(request):
    def get_urls(url):
        a = 0
        for url in urlopen(url):
            url = url[:-1]
            if not url.stip():
                continue
            if not RP.objects.filter(url=url):
                RP.objects.create(url=url)
                a += 1
        return a

    a = 0
    a += get_urls("http://nurpa.be/log")
    a += get_urls("http://nurpa.be/log-archive")
    return HttpResponse("%s new rp items" % a)
