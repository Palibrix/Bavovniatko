from django.db import models
from django.utils.translation import gettext_lazy as _

from galleries.mixins import BaseImageMixin


class AntennaGallery(BaseImageMixin):
    object = models.ForeignKey('components.Antenna', blank=True, null=True, on_delete=models.CASCADE, related_name='images')
    suggestion = models.ForeignKey('suggestions.AntennaSuggestion', blank=True, null=True, on_delete=models.SET_NULL, related_name='suggested_images')

    class Meta:
        db_table = 'galleries_antenna'
        verbose_name = _('Antenna Gallery')
        verbose_name_plural = _('Antenna Galleries')
        ordering = ['object', 'order', '-created_at']


class CameraGallery(BaseImageMixin):
    object = models.ForeignKey('components.Camera', blank=True, null=True, on_delete=models.CASCADE, related_name='images')
    suggestion = models.ForeignKey('suggestions.CameraSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_images')

    class Meta:
        db_table = 'galleries_camera'
        verbose_name = _('Camera Gallery')
        verbose_name_plural = _('Camera Galleries')
        ordering = ['object', 'order', '-created_at']


class FrameGallery(BaseImageMixin):
    object = models.ForeignKey('components.Frame', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_frame'
        verbose_name = _('Frame Gallery')
        verbose_name_plural = _('Frame Galleries')
        ordering = ['object', 'order', '-created_at']


class FlightControllerGallery(BaseImageMixin):
    object = models.ForeignKey('components.FlightController', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_flight_controller'
        verbose_name = _('Flight Controller Gallery')
        verbose_name_plural = _('Flight Controller Galleries')
        ordering = ['object', 'order', '-created_at']


class MotorGallery(BaseImageMixin):
    object = models.ForeignKey('components.Motor', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_motor'
        verbose_name = _('Motor Gallery')
        verbose_name_plural = _('Motor Galleries')
        ordering = ['object', 'order', '-created_at']


class PropellerGallery(BaseImageMixin):
    object = models.ForeignKey('components.Propeller', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_propeller'
        verbose_name = _('Propeller Gallery')
        verbose_name_plural = _('Propeller Galleries')
        ordering = ['object', 'order', '-created_at']


class ReceiverGallery(BaseImageMixin):
    object = models.ForeignKey('components.Receiver', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_receiver'
        verbose_name = _('Receiver Gallery')
        verbose_name_plural = _('Receiver Galleries')
        ordering = ['object', 'order', '-created_at']


class StackGallery(BaseImageMixin):
    object = models.ForeignKey('components.Stack', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_stack'
        verbose_name = _('Stack Gallery')
        verbose_name_plural = _('Stack Galleries')
        ordering = ['object', 'order', '-created_at']


class SpeedControllerGallery(BaseImageMixin):
    object = models.ForeignKey('components.SpeedController', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_speed_controller'
        verbose_name = _('Speed Controller Gallery')
        verbose_name_plural = _('Speed Controller Galleries')
        ordering = ['object', 'order', '-created_at']


class TransmitterGallery(BaseImageMixin):
    object = models.ForeignKey('components.Transmitter', on_delete=models.CASCADE, related_name='images')

    class Meta:
        db_table = 'galleries_transmitter'
        verbose_name = _('Transmitter Gallery')
        verbose_name_plural = _('Transmitter Galleries')
        ordering = ['object', 'order', '-created_at']
