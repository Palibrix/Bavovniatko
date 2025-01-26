from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_frame_mixins import (
    BaseFrameMixin,
    BaseFrameCameraDetailMixin,
    BaseFrameMotorDetailMixin,
    BaseFrameVTXDetailMixin
)
from components.models import Frame, FrameCameraDetail, FrameMotorDetail, FrameVTXDetail
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin


class FrameSuggestion(SuggestionFilesDeletionMixin, BaseFrameMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Frame', blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)
        self._handle_details(instance)

    def _handle_media(self, frame):
        for suggested_image in self.suggested_images.all():
            if not suggested_image.object:
                suggested_image.object = frame
            suggested_image.save()

        for suggested_document in self.suggested_documents.all():
            if not suggested_document.object:
                suggested_document.object = frame
            suggested_document.save()

    def _handle_details(self, frame):
        # Handle camera mount details
        for suggested_detail in self.suggested_camera_details.all():
            camera_detail = FrameCameraDetail.objects.create(
                frame=frame,
                **{field: getattr(suggested_detail, field)
                   for field in BaseFrameCameraDetailMixin.CAMERA_DETAIL_FIELDS}
            )
            camera_detail.full_clean()
            camera_detail.save()
            suggested_detail.related_instance = camera_detail
            suggested_detail.save()

        # Handle motor mount details
        for suggested_detail in self.suggested_motor_details.all():
            motor_detail = FrameMotorDetail.objects.create(
                frame=frame,
                **{field: getattr(suggested_detail, field)
                   for field in BaseFrameMotorDetailMixin.MOTOR_DETAIL_FIELDS}
            )
            motor_detail.full_clean()
            motor_detail.save()
            suggested_detail.related_instance = motor_detail
            suggested_detail.save()

        # Handle VTX mount details
        for suggested_detail in self.suggested_vtx_details.all():
            vtx_detail = FrameVTXDetail.objects.create(
                frame=frame,
                **{field: getattr(suggested_detail, field)
                   for field in BaseFrameVTXDetailMixin.VTX_DETAIL_FIELDS}
            )
            vtx_detail.full_clean()
            vtx_detail.save()
            suggested_detail.related_instance = vtx_detail
            suggested_detail.save()

    def _create_instance(self):
        frame = Frame.objects.create(
            **{field: getattr(self, field)
               for field in self.FRAME_FIELDS}
        )
        frame.full_clean()
        frame.save()

        self.related_instance = frame
        self.save()
        return frame


class SuggestedFrameCameraDetailSuggestion(BaseFrameCameraDetailMixin):
    suggestion = models.ForeignKey('suggestions.FrameSuggestion', on_delete=models.CASCADE,
                                 related_name='suggested_camera_details',
                                 verbose_name='details')
    related_instance = models.ForeignKey('components.FrameCameraDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       verbose_name='submitted_suggestions')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_camera_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Camera Detail for this Frame."), self)

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_frame_camera_detail'
        verbose_name = _('Suggested Frame Camera Detail')
        verbose_name_plural = _('Suggested Frame Camera Details')
        ordering = ['related_instance']


class SuggestedFrameMotorDetailSuggestion(BaseFrameMotorDetailMixin):
    suggestion = models.ForeignKey('suggestions.FrameSuggestion', on_delete=models.CASCADE,
                                 related_name='suggested_motor_details',
                                 verbose_name='details')
    related_instance = models.ForeignKey('components.FrameMotorDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       verbose_name='submitted_suggestions')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_motor_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Motor Detail for this Frame."), self)

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_frame_motor_detail'
        verbose_name = _('Suggested Frame Motor Detail')
        verbose_name_plural = _('Suggested Frame Motor Details')
        ordering = ['related_instance']


class SuggestedFrameVTXDetailSuggestion(BaseFrameVTXDetailMixin):
    suggestion = models.ForeignKey('suggestions.FrameSuggestion', on_delete=models.CASCADE,
                                 related_name='suggested_vtx_details',
                                 verbose_name='details')
    related_instance = models.ForeignKey('components.FrameVTXDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='submitted_suggestions',
                                       verbose_name='submitted_suggestions')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_vtx_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only VTX Detail for this Frame."), self)

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_frame_vtx_detail'
        verbose_name = _('Suggested Frame VTX Detail')
        verbose_name_plural = _('Suggested Frame VTX Details')
        ordering = ['related_instance']


class ExistingFrameCameraDetailSuggestion(BaseFrameCameraDetailMixin, BaseSuggestionMixin):
    frame = models.ForeignKey('components.Frame', on_delete=models.CASCADE,
                           related_name='suggested_camera_details',
                           verbose_name='Frame')
    related_instance = models.ForeignKey('components.FrameCameraDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='suggested_details')

    def _create_instance(self):
        instance = FrameCameraDetail.objects.create(
            frame=self.frame,
            **{field: getattr(self, field)
               for field in self.CAMERA_DETAIL_FIELDS}
        )
        instance.full_clean()
        instance.save()
        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_frame_camera_detail'
        verbose_name = _('Existing Frame Camera Detail Suggestion')
        verbose_name_plural = _('Existing Frame Camera Detail Suggestions')
        ordering = ['frame']


class ExistingFrameMotorDetailSuggestion(BaseFrameMotorDetailMixin, BaseSuggestionMixin):
    frame = models.ForeignKey('components.Frame', on_delete=models.CASCADE,
                           related_name='suggested_motor_details',
                           verbose_name='Frame')
    related_instance = models.ForeignKey('components.FrameMotorDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='suggested_details')

    def _create_instance(self):
        instance = FrameMotorDetail.objects.create(
            frame=self.frame,
            **{field: getattr(self, field)
               for field in self.MOTOR_DETAIL_FIELDS}
        )
        instance.full_clean()
        instance.save()
        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_frame_motor_detail'
        verbose_name = _('Existing Frame Motor Detail Suggestion')
        verbose_name_plural = _('Existing Frame Motor Detail Suggestions')
        ordering = ['frame']


class ExistingFrameVTXDetailSuggestion(BaseFrameVTXDetailMixin, BaseSuggestionMixin):
    frame = models.ForeignKey('components.Frame', on_delete=models.CASCADE,
                           related_name='suggested_vtx_details',
                           verbose_name='Frame')
    related_instance = models.ForeignKey('components.FrameVTXDetail', on_delete=models.CASCADE,
                                       blank=True, null=True,
                                       related_name='suggested_details')

    def _create_instance(self):
        instance = FrameVTXDetail.objects.create(
            frame=self.frame,
            **{field: getattr(self, field)
               for field in self.VTX_DETAIL_FIELDS}
        )
        instance.full_clean()
        instance.save()
        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_frame_vtx_detail'
        verbose_name = _('Existing Frame VTX Detail Suggestion')
        verbose_name_plural = _('Existing Frame VTX Detail Suggestions')
        ordering = ['frame']