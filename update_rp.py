from sys import stdout, stderr, exit
from time import sleep
from urllib2 import urlopen
from datetime import datetime

from rp.models import RP
from django.db import transaction

def fill():
    def get_urls(url):
        a = 0

        urls = ""
        tries = 0
        print "Fetching " + url
        while not urls:
            try:
                urls = urlopen(url).read()
            except Exception, e:
                print "Malheur !: " + e
                tries += 1
                if tries > 3:
                    stderr("Unable to get urls from %s\nAbort" % url)
                    exit(1)
                sleep(1)

        print "Processing urls"
        total_len = len(urls.split("\n"))
        for url in urls.split("\n"):
            if not url.strip():
                continue
            date, url = url.split(" ", 1)
            if not RP.objects.filter(url=url):
                RP.objects.create(url=url, datetime=datetime.fromtimestamp(int(date)))
            a += 1
            stdout.write("%s/%s\r" % (a, total_len))
            stdout.flush()
        stdout.write("%s/%s\r\n" % (total_len, total_len))

    with transaction.commit_on_success():
        get_urls("http://nurpa.be/log")
    #a += get_urls("http://nurpa.be/log-archive")

    print
    print "[done]"

if __name__ == "__main__":
    fill()
