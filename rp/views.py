from time import sleep
from re import sub
from urllib2 import urlopen, URLError
from datetime import datetime
from mechanize import Browser
from oice.langdet import langdet

from django.views.generic import UpdateView
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

def encoding_sucks(text):
    try:
        return text.encode("Utf-8")
    except UnicodeError:
        pass
    try:
        return text.decode("Utf-8")
    except UnicodeDecodeError:
        pass
    try:
        return text.encode("iso-8859-1")
    except:
        pass
    try:
        return text.decode("iso-8859-1")
    except:
        pass
    return "could not get the title :(, tell Bram that this website sucks"

class RPEdit(UpdateView):
    success_url="/"
    model=RP

    def get_form_kwargs(self, **kwargs):
        data = super(RPEdit, self).get_form_kwargs(**kwargs)

        if not data["instance"].title:
            data["initial"]["title"] = ""
            b = Browser()
            try:
                b.open(data["instance"].url)
                site = ".".join(map(lambda x: x.capitalize(), data["instance"].url.split("/")[2].replace("www.", "").split(".")[:-1]))
                data["initial"]["title"] = "[%s] %s" % (site.encode("Utf-8"), encoding_sucks(b.title()))
            except URLError:
                pass
        if not data["instance"].langue:
            data["initial"]["langue"] = ""
            try:
                text = urlopen(data["instance"].url).read()
                text = sub("[^\w ]", lambda x: "", text)
                lang = langdet.LanguageDetector.detect(text).iso.upper()
                if lang in ('FR', 'EN', 'ES'):
                    data["initial"]["langue"] = lang
            except URLError:
                pass
        return data
