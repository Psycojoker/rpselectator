from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView

from models import RP

urlpatterns = patterns('rp.views',
    url(r'^fill/$', 'fill', name="fill"),
    url(r'^$',ListView.as_view(model=RP), name="rp_list"),
)
