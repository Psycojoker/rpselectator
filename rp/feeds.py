from django.contrib.syndication.views import Feed
from models import RP

class RSS(Feed):
    title = "NURPA RP RSS"
    link = "http://nurpa.be"
    description = "Last items published in our rp"

    def items(self):
        return RP.objects.filter(published=True).exclude(title__isnull=True).exclude(langue__isnull=True).order_by('-published_date')[:20]

    def item_title(self, item):
        title = item.title if item.title else "No title yet"
        return title

    def item_link(self, item):
        return item.url

    def item_guid(self, item):
        return str(item.id)

    def item_pubdate(self, item):
        return item.published_date
