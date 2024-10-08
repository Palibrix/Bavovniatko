from django.db import models
from imagekit.models import ProcessedImageField

def upload_to_gallery(instance, filename):
    return f"images/{instance.__class__.__name__}/{filename}"

class BaseImageMixin(models.Model):
    image = ProcessedImageField(upload_to=upload_to_gallery, options={'quality': 75}, format='WEBP')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['order', '-created_at']
        unique_together = ('object', 'order')

    @classmethod
    def _check_fields(cls, **kwargs):
        cls._meta.get_field('object')
        return super()._check_fields(**kwargs)