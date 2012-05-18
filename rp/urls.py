from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from models import RP
from feeds import RSS
from views import fill

urlpatterns = patterns('rp.views',
    url(r'^fill/$', login_required(fill), name="fill"),
    url(r'^$', login_required(ListView.as_view(queryset=RP.objects.filter(published=None).order_by('-id'))), name="rp_list"),
    url(r'^published/$', login_required(ListView.as_view(queryset=RP.objects.filter(published=True).order_by('-id'))), name="rp_list_published"),
    url(r'^archived/$', login_required(ListView.as_view(queryset=RP.objects.filter(published=False).order_by('-id'))), name="rp_list_archived"),
    url(r'^rss.xml$', RSS(), name="rss"),
)
