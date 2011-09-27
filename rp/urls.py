from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView, UpdateView

from models import RP

from feeds import RSS

urlpatterns = patterns('rp.views',
    url(r'^fill/$', 'fill', name="fill"),
    url(r'^edit/(?P<pk>[0-9]+)/$', UpdateView.as_view(model=RP, success_url="/"), name="edit_rp"),
    url(r'^$', ListView.as_view(queryset=RP.objects.order_by('-id')), name="rp_list"),
    url(r'^rss.xml$', RSS(), name="rss"),
)
