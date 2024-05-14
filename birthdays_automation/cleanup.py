import os
import atexit
from django.conf import settings
import shutil

def cleanup_media():
    media_root = settings.MEDIA_ROOT
    if os.path.exists(media_root):
        shutil.rmtree(media_root)
        os.makedirs(media_root)

atexit.register(cleanup_media)
