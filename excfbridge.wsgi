import os
import sys

from gevent.wsgi import WSGIServer
from gevent.monkey import patch_all

path = ['/home/segfault/sites/excfbridge']
for i in path:
    if i not in sys.path:
        sys.path.append(i)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

patch_all()

WSGIServer(('', 8000), application).serve_forever()

