# Create your views here.

from django.http import HttpResponse

from models import RP

from urllib2 import urlopen

def fill(request):
    a = 0
    for url in urlopen("http://nurpa.be/log"):
        url = url[:-1]
        if not RP.objects.filter(url=url):
            RP.objects.create(url=url)
            a += 1
    return HttpResponse("%s new rp items" % a)
