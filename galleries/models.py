from django.db import models

from galleries.mixins import BaseImageMixin


class AntennaGallery(BaseImageMixin):
    object = models.ForeignKey('components.Antenna', on_delete=models.CASCADE, related_name='images')


class CameraGallery(BaseImageMixin):
    object = models.ForeignKey('components.Camera', on_delete=models.CASCADE, related_name='images')