from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = 'PRD/static'
    default_acl = 'private'


class PublicMediaStorage(S3Boto3Storage):
    location = 'PRD/media'
    default_acl = 'private'
    file_overwrite = False