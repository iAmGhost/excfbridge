import os
import sys

path = ['/home/segfault/sites/excfbridge']
for i in path:
    if i not in sys.path:
        sys.path.append(i)

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
