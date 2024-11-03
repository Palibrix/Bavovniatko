import os
from urllib.parse import urljoin
from uuid import uuid4

from django.core.files.storage import FileSystemStorage

from core import settings

def generate_unique_filename(filename):
    ext = filename.split('.')[-1]
    filename = uuid4().hex
    return f"{filename}.{ext}"

class CkFileStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        name = generate_unique_filename(name)
        return super().save(name, content, max_length)

    location = os.path.join(settings.MEDIA_ROOT, "ckeditor")
    base_url = urljoin(settings.MEDIA_URL, "ckeditor/")
