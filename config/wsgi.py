import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

if os.environ.get('VERCEL'):
    from django.core.management import call_command
    call_command('migrate', '--noinput', verbosity=0)
