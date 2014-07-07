import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'tekhnoland.settings_prod'

#SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
#sys.path.append(os.path.join(SITE_ROOT, 'sites'))
#sys.path.append(os.path.join(SITE_ROOT, 'apps'))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
