import os

import requests
from django.core.management.base import NoArgsCommand


class Command(NoArgsCommand):
    """
    Usage example:
    HOSTNAME=tubedl.herokuapp.com python manage.py keepalive
    """
    help = 'Pings os.environ["HOSTNAME"] to keep dyno alive.'

    def handle_noargs(self, **options):
        hostname = os.environ.get("HOSTNAME")
        if hostname:
            self.stdout.write('ping "%s"' % hostname)
            url = "http://" + hostname
            requests.get(url)
        else:
            self.stdout.write("Couldn't keep alive, HOSTNAME not set")
