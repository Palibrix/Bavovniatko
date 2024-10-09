from django.db import models
from django.utils.translation import gettext_lazy as _

from galleries.mixins import BaseImageMixin


class DroneGallery(BaseImageMixin):
    object = models.ForeignKey('builds.Drone', on_delete=models.CASCADE, related_name='images')

    class Meta:
        app_label = 'galleries'
        verbose_name = _('Drone Gallery')
        verbose_name_plural = _('Drone Galleries')
