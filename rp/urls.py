from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from models import RP

from feeds import RSS

from views import RPEdit

urlpatterns = patterns('rp.views',
    url(r'^fill/$', 'fill', name="fill"),
    url(r'^edit/(?P<pk>[0-9]+)/$', RPEdit.as_view(), name="edit_rp"),
    url(r'^$', ListView.as_view(queryset=RP.objects.order_by('-id')), name="rp_list"),
    url(r'^published/$', ListView.as_view(queryset=RP.objects.filter(published=True).order_by('-id')), name="rp_list_published"),
    url(r'^rss.xml$', RSS(), name="rss"),
)
