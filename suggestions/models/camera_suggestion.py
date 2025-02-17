from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_camera_mixins import BaseCameraMixin, BaseVideoFormatMixin, BaseCameraDetailMixin
from components.models import Camera, CameraDetail, VideoFormat
from components.validators import validate_fov_length
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin, MediaHandlerMixin


class CameraSuggestion(SuggestionFilesDeletionMixin, MediaHandlerMixin, BaseCameraMixin, BaseSuggestionMixin):

    related_instance = models.ForeignKey('components.Camera', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _handle_post_accept(self, instance):
        self._handle_media(instance)
        self._handle_details(instance)

    def _handle_details(self, instance):
        for suggested_detail in self.suggested_details.all():
            defaults = {
                field: getattr(suggested_detail, field)
                for field in BaseCameraDetailMixin.DETAIL_FIELDS
                if getattr(suggested_detail, field) is not None
            }

            camera_detail = CameraDetail.objects.create(
                camera=instance,
                **defaults
            )
            camera_detail.full_clean()
            camera_detail.save()

            suggested_detail.related_instance = camera_detail
            suggested_detail.save()

    def _create_instance(self):
        # Create new instance with all fields
        instance = Camera.objects.create(
            **{field: getattr(self, field)
               for field in self.CAMERA_FIELDS}
        )

        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()

        if hasattr(self, 'video_formats') and self.video_formats.exists():
            instance.video_formats.set(self.video_formats.all())

        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_camera'

        verbose_name = _('Camera Suggestion')
        verbose_name_plural = _('Camera Suggestions')
        ordering = ['manufacturer', 'model', ]


class VideoFormatSuggestion(BaseVideoFormatMixin, BaseSuggestionMixin):
    VIDEO_FORMAT_FIELDS = ['format']

    related_instance = models.ForeignKey('components.VideoFormat', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    def _create_instance(self):
        instance = VideoFormat.objects.create(
            **{field: getattr(self, field)
               for field in self.VIDEO_FORMAT_FIELDS}
        )

        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_video_format'
        verbose_name = _('Video Format Suggestion')
        verbose_name_plural = _('Video Format Suggestions')
        ordering = ['format']


class ExistingCameraDetailSuggestion(BaseCameraDetailMixin, BaseSuggestionMixin):
    """ Suggest new detail to existing camera """
    camera = models.ForeignKey('components.Camera', on_delete=models.CASCADE, related_name='suggested_details',
                                verbose_name='Camera')
    related_instance = models.ForeignKey('components.CameraDetail', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='suggested_details')

    def _create_instance(self):
        instance = CameraDetail.objects.create(
            camera=self.camera,
            **{field: getattr(self, field)
               for field in BaseCameraDetailMixin.DETAIL_FIELDS}
        )

        instance.full_clean()
        instance.save()

        self.related_instance = instance
        self.save()
        return instance

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_camera_detail'
        verbose_name = _('Existing Camera Detail Suggestion')
        verbose_name_plural = _('Existing Camera Detail Suggestions')
        ordering = ['camera']


class SuggestedCameraDetailSuggestion(BaseCameraDetailMixin):
    """ Add detail to suggested camera """
    suggestion = models.ForeignKey('suggestions.CameraSuggestion', on_delete=models.CASCADE,
                                   related_name='suggested_details',
                                   verbose_name='details')
    related_instance = models.ForeignKey('components.CameraDetail', on_delete=models.CASCADE,
                                         blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         verbose_name='submitted_suggestions')

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Detail for this object."), self)

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_camera_detail'
        verbose_name = _('Suggested Camera Detail')
        verbose_name_plural = _('Suggested Camera Details')
        ordering = ['related_instance']
