from uuid import uuid4

from django.db import models

def upload_to_filestorage(instance, filename):
    _object = instance.object
    if _object.pk:
        filepath = f"documents/components/{_object.__class__._meta.verbose_name_plural}/{_object.id}/{filename}"
    else:
        filepath = f"documents/components/Unknown/{filename}"
    return filepath

class BaseFileModelMixin(models.Model):

    file = models.FileField(upload_to=upload_to_filestorage)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        app_label = 'documents'
