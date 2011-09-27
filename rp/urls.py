from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('rp.views',
    url(r'^fill/$', 'fill', name="fill"),
)
