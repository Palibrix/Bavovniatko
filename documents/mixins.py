import filetype
from django.contrib import admin
from django.db import models
from drf_extra_fields.fields import Base64FileField
from rest_framework.exceptions import ValidationError


def upload_to_filestorage(instance, filename):
    _object = instance.object or instance.suggestion
    _object_type = _object.__class__._meta.app_label
    if _object.pk:
        filepath = f"documents/{_object_type}/{_object.__class__._meta.verbose_name_plural}/{_object.id}/{filename}"
    else:
        filepath = f"documents/{_object_type}/Unknown/{filename}"
    return filepath


class BaseDocumentMixin(models.Model):

    file = models.FileField(upload_to=upload_to_filestorage)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.clean()
        if self.object and not self.accepted:
            self.accepted = True
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
        app_label = 'documents'

    @classmethod
    def _check_fields(cls, **kwargs):
        cls._meta.get_field('object')
        ### TODO: uncomment row when all suggestion models will be added
        # cls._meta.get_field('suggestion')
        return super()._check_fields(**kwargs)


class BaseDocumentInlineAdminMixin(admin.StackedInline):
    extra = 0
    max_num = 10
    readonly_fields = ('created_at',)
    ### TODO: uncomment row when all suggestion models will be added
    # readonly_fields = ('object', 'suggestion', 'accepted', 'created_at')


class Base64ValidatedFileField(Base64FileField):
    ALLOWED_TYPES = ['pdf', 'png', 'doc', 'docx']

    def get_file_extension(self, filename, decoded_file):
        kind = filetype.guess(decoded_file)
        if kind.extension in self.ALLOWED_TYPES:
            return kind.extension