from json import dumps
from django.conf.urls.defaults import patterns, url
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from models import RP
from feeds import RSS
from views import fill

class RPForm(ModelForm):
    class Meta:
        model = RP

def save(request):
    rp = get_object_or_404(RP, id=request.POST["id"])
    form = RPForm(request.POST, instance=rp)

    if form["published"].data:
        if not form.is_valid():
            print "errors"
            return HttpResponse(dumps(form.errors))
        else:
            form.save()
    else:
        rp.published = form["published"].data
        rp.save()

    return HttpResponse("ok")

def save_archives(request):
    ids = request.POST.getlist('ids[]')

    for id_archive in ids:
        rp = get_object_or_404(RP, id=id_archive)
        rp.published = False
        rp.save()

    return HttpResponse("ok")

def item_json(request, pk):
    item = get_object_or_404(RP, pk=pk)
    return HttpResponse(dumps({"title": item.get_title(), "langue": item.get_langue()}))

urlpatterns = patterns('rp.views',
    url(r'^fill/$', login_required(fill), name="fill"),
    url(r'^save/$', login_required(save), name="save"),
    url(r'^save_archives/$', login_required(save_archives), name="save_archives"),
    url(r'^$', login_required(ListView.as_view(queryset=RP.objects.filter(published=None).order_by('datetime'))), name="rp_list"),
    url(r'^published/$', login_required(ListView.as_view(queryset=RP.objects.filter(published=True).order_by('-published_date'))), name="rp_list_published"),
    url(r'^archived/$', login_required(ListView.as_view(queryset=RP.objects.filter(published=False).order_by('-datetime'))), name="rp_list_archived"),
    url(r'^rss.xml$', RSS(), name="rss"),
    url(r'^item_json/(?P<pk>\d+)/$', item_json, name="item_json"),
)
