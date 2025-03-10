# activate_this = 'C:/Users/bulmaj/Envs/redepplan/Scripts/activate_this.py'
# exec(open(activate_this).read(),dict(__file__=activate_this))

import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
# site.addsitedir('C:/Users/bulmaj/Envs/redepplan/Lib/site-packages')

# Add the app's directory to the PYTHONPATH

print(os.getenv('DJANGO_PRODUCTION'))
print(os.getenv('DJANGO_DEVELOPMENT'))
if os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PROD')
    sys.path.append('C:/Dev/nova')
    sys.path.append('C:/Dev/nova/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redepplan.settings_prod")
elif os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('UAT - Check')
    sys.path.append('C:/Dev/nova')
    sys.path.append('C:/Dev/nova/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redepplan.settings")
else:
    print('DEV')
    sys.path.append('/var/www/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "redepplan.settings_dev")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# import django.core.handlers.wsgi
# application = django.core.handlers.wsgi.WSGIHandler()