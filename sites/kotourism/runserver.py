import os, sys
from os.path import abspath, dirname
from werkzeug import run_simple, DebuggedApplication
from django.views import debug
from django.core.handlers.wsgi import WSGIHandler

def null_technical_500_response(request, exc_type, exc_value, tb):
    raise exc_type, exc_value, tb
debug.technical_500_response = null_technical_500_response

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
path = os.path.abspath(dirname(dirname(abspath(__file__))))
sys.path.append(path)

if __name__ == '__main__':
    run_simple('localhost', 8000, DebuggedApplication(WSGIHandler(), True), True)
