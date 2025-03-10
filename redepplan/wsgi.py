import os
import sys
import site


sys.path.append('/var/www/redepplan')

if os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PROD')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'

elif os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('UAT - Check')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

else:
    print('DEV')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
