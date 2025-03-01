from django.db import models
from django.utils.translation import gettext_lazy as _

from documents.mixins import BaseDocumentMixin


class AntennaDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Antenna', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.AntennaSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_antenna'
        verbose_name = _('Antenna Document')
        verbose_name_plural = _('Antenna Documents')
        ordering = ['object',  '-created_at']


class CameraDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Camera', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.CameraSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_camera'
        verbose_name = _('Camera Document')
        verbose_name_plural = _('Camera Documents')
        ordering = ['object',  '-created_at']


class FrameDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Frame', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.FrameSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_frame'
        verbose_name = _('Frame Document')
        verbose_name_plural = _('Frame Documents')
        ordering = ['object',  '-created_at']


class FlightControllerDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.FlightController', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.FlightControllerSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_flight_controller'
        verbose_name = _('Flight Controller Document')
        verbose_name_plural = _('Flight Controller Documents')
        ordering = ['object',  '-created_at']


class MotorDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Motor', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.MotorSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_motor'
        verbose_name = _('Motor Document')
        verbose_name_plural = _('Motor Documents')
        ordering = ['object',  '-created_at']


class PropellerDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Propeller', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.PropellerSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_propeller'
        verbose_name = _('Propeller Document')
        verbose_name_plural = _('Propeller Documents')
        ordering = ['object',  '-created_at']


class ReceiverDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Receiver', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.ReceiverSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_receiver'
        verbose_name = _('Receiver Document')
        verbose_name_plural = _('Receiver Documents')
        ordering = ['object',  '-created_at']


class StackDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Stack', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.StackSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_stack'
        verbose_name = _('Stack Document')
        verbose_name_plural = _('Stack Documents')
        ordering = ['object',  '-created_at']


class SpeedControllerDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.SpeedController', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.SpeedControllerSuggestion', blank=True, null=True, on_delete=models.SET_NULL,
                                   related_name='suggested_documents')

    class Meta:
        db_table = 'documents_speed_controller'
        verbose_name = _('Speed Controller Document')
        verbose_name_plural = _('Speed Controller Documents')
        ordering = ['object',  '-created_at']


class TransmitterDocument(BaseDocumentMixin):
    object = models.ForeignKey('components.Transmitter', blank=True, null=True, on_delete=models.CASCADE, related_name='documents')
    suggestion = models.ForeignKey('suggestions.TransmitterSuggestion', blank=True, null=True,
                                   on_delete=models.SET_NULL, related_name='suggested_documents')

    class Meta:
        db_table = 'documents_transmitter'
        verbose_name = _('Transmitter Document')
        verbose_name_plural = _('Transmitter Documents')
        ordering = ['object',  '-created_at']
