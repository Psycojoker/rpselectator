from django.contrib.syndication.views import Feed
from models import RP

class RSS(Feed):
    title = "NURPA RP RSS"
    link = "http://nurpa.be"
    description = "Last items published in our rp"

    def items(self):
        return RP.objects.filter(published=True)[:20]

    def item_title(self, item):
        return item.title if item.title else "No title yet"

    def item_link(self, item):
        return item.url
