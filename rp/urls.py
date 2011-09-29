from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from models import RP

from feeds import RSS

from views import RPEdit

urlpatterns = patterns('rp.views',
    url(r'^fill/$', 'fill', name="fill"),
    url(r'^edit/(?P<pk>[0-9]+)/$', RPEdit.as_view(), name="rp_edit"),
    url(r'^$', ListView.as_view(queryset=RP.objects.filter(published=None).order_by('-id')), name="rp_list"),
    url(r'^published/$', ListView.as_view(queryset=RP.objects.filter(published=True).order_by('-id')), name="rp_list_published"),
    url(r'^archived/$', ListView.as_view(queryset=RP.objects.filter(published=False).order_by('-id')), name="rp_list_archived"),
    url(r'^rss.xml$', RSS(), name="rss"),
)
