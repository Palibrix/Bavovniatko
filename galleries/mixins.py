from uuid import uuid4

from django.contrib import admin
from django.db import models
from imagekit.models import ProcessedImageField

from builds.forms import RequiredInlineFormSet


def upload_to_gallery(instance, filename):
    ext = filename.split('.')[-1]
    _object = instance.object
    _object_type = _object.__class__._meta.app_label
    if _object.pk:
        filename = f'{_object.__class__.__name__}_{instance.object.pk}_{instance.order}.{ext}'
        filepath = f"images/{_object_type}/{_object.__class__._meta.verbose_name_plural}/{_object.id}/{filename}"
    else:
        filename = f'{uuid4().hex}.{ext}'
        filepath = f"images/{_object_type}/Unknown/{filename}"
    return filepath


class BaseImageMixin(models.Model):
    image = ProcessedImageField(upload_to=upload_to_gallery, options={'quality': 75}, format='WEBP')
    order = models.PositiveIntegerField(default=0, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        app_label = 'galleries'

    @classmethod
    def _check_fields(cls, **kwargs):
        cls._meta.get_field('object')
        return super()._check_fields(**kwargs)


class BaseGalleryInlineAdminMixin(admin.StackedInline):
    extra = 0
    max_num = 10
    formset = RequiredInlineFormSet
    readonly_fields = ('created_at',)
