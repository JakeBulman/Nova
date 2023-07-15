import sys
import os
import django

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'
else:
    sys.path.append('C:/Dev/redepplan')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'

django.setup()


from enquiries.models import EarServerSettings


# EarServerSettings.objects.create(
#             session_id_list = "ABC",
#             enquiry_id_list = "DEF",
#         )