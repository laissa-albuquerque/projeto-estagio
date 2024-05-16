import os
import shutil
from django.conf import settings

class ClearMediaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.clear_media_folder()
        response = self.get_response(request)
        return response

    def clear_media_folder(self):
        media_folder = settings.MEDIA_ROOT
        if os.path.exists(media_folder):
            for filename in os.listdir(media_folder):
                file_path = os.path.join(media_folder, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
