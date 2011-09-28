from re import sub
from urllib2 import urlopen
from mechanize import Browser
from oice.langdet import langdet

from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, UpdateView

from models import RP

from feeds import RSS

def encode_sucks(text):
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
            b = Browser()
            b.open(data["instance"].url)
            site = ".".join(map(lambda x: x.capitalize(), data["instance"].url.split("/")[2].replace("www.", "").split(".")[:-1]))
            data["initial"]["title"] = "[%s] %s" % (site.encode("Utf-8"), encode_sucks(b.title()))
        if not data["instance"].langue:
            text = urlopen(data["instance"].url).read()
            text = sub("[^\w ]", lambda x: "", text)
            lang = langdet.LanguageDetector.detect(text).iso.upper()
            if lang in ('FR', 'EN', 'ES'):
                data["initial"]["langue"] = lang
        return data

urlpatterns = patterns('rp.views',
    url(r'^fill/$', 'fill', name="fill"),
    url(r'^edit/(?P<pk>[0-9]+)/$', RPEdit.as_view(), name="edit_rp"),
    url(r'^$', ListView.as_view(queryset=RP.objects.order_by('-id')), name="rp_list"),
    url(r'^rss.xml$', RSS(), name="rss"),
)
