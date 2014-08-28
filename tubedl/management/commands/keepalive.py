import os
import urllib2
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Pings os.environ["HOSTNAME"] to keep dyno alive.'

    def handle_noargs(self, **options):
        hostname = os.environ.get("HOSTNAME")
        if hostname:
            self.stdout.write('ping "%s"' % hostname)
        else:
            self.stdout.write("Couldn't keep alive, HOSTNAME not set")
