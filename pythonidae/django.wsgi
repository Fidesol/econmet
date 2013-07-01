# This file is used to deploy the app into Apache server
# see https://docs.djangoproject.com/en/1.4/howto/deployment/wsgi/

import os
import sys

path = '/path/to'
if path not in sys.path:
    sys.path.append(path)

path = '/path/to/project'
if path not in sys.path:
    sys.path.append(path)


os.environ['DJANGO_SETTINGS_MODULE'] = 'pythonidae.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
