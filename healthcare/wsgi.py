import sys
import os

path = '/home/dipak13/AI-Healthcare-Chat-Bot-Assistance'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'healthcare.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()