import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mbco.conference.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

