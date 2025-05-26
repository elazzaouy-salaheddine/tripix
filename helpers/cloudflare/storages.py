from storages.backends.s3 import S3Storage
from django.conf import settings


class StaticFilesStorage(S3Storage):
    """
    Custom storage class for static files using Cloudflare R2.
    helpers.cloudflare.storages.StaticFilesStorage
    This class is used to store static files in a Cloudflare R2 bucket.
    """
    location = "static"

class MediaFilesStorage(S3Storage):
    """
    Custom storage class for media files using Cloudflare R2.
    helpers.cloudflare.storages.MediaFilesStorage
    This class is used to store media files in a Cloudflare R2 bucket.
    """
    location = 'media'