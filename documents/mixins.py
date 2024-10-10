from django.contrib import admin
from django.db import models


def upload_to_filestorage(instance, filename):
    _object = instance.object
    _object_type = _object.__class__._meta.app_label
    if _object.pk:
        filepath = f"documents/{_object_type}/{_object.__class__._meta.verbose_name_plural}/{_object.id}/{filename}"
    else:
        filepath = f"documents/{_object_type}/Unknown/{filename}"
    return filepath


class BaseDocumentMixin(models.Model):

    file = models.FileField(upload_to=upload_to_filestorage)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        app_label = 'documents'

    @classmethod
    def _check_fields(cls, **kwargs):
        cls._meta.get_field('object')
        return super()._check_fields(**kwargs)


class BaseDocumentInlineAdminMixin(admin.StackedInline):
    extra = 0
    max_num = 10
    readonly_fields = ('created_at',)
