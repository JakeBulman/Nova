"""
ASGI config for redepplan project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys
from django.core.asgi import get_asgi_application

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redepplan.settings_dev')
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'redepplan.settings')



application = get_asgi_application()
