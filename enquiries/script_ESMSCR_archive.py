import sys
import os
import django

if os.getenv('DJANGO_DEVELOPMENT') == 'true':
    print('UAT')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings'
elif os.getenv('DJANGO_PRODUCTION') == 'true':
    print('PRD')
    path = os.path.join('C:\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_prod'
else:
    print('DEV')
    path = os.path.join('C:\\Users\\bulmaj\\OneDrive - Cambridge\\Desktop\\Dev\\Nova')
    sys.path.append(path)
    os.environ['DJANGO_SETTINGS_MODULE'] = 'redepplan.settings_dev'

django.setup()

from enquiries.models import EsmscrDownloads

def run_algo():
    for task in EsmscrDownloads.objects.filter(archive_count=0):
        document = EsmscrDownloads.objects.get(pk=task.pk).document
        file_name = EsmscrDownloads.objects.get(pk=task.pk).file_name
        new_file_name = "\\\\filestorage\cie\Operations\Results Team\Enquiries About Results\\0.Nova Downloads\Script Request CSV\\" + file_name
        print(document)
        with open(new_file_name, 'wb') as actual_file:
            actual_file.write(document.read())
        archives = int(EsmscrDownloads.objects.get(pk=task.pk).archive_count) + 1
        EsmscrDownloads.objects.filter(pk=task.pk).update(archive_count = str(archives))

run_algo()