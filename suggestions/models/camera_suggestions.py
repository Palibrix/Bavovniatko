from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from components.mixins.base_camera_mixins import BaseCameraMixin, BaseVideoFormatMixin, BaseCameraDetailMixin
from components.models import Camera, CameraDetail, VideoFormat
from suggestions.mixins import BaseSuggestionMixin, SuggestionFilesDeletionMixin


class CameraSuggestion(SuggestionFilesDeletionMixin, BaseCameraMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.Camera', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()
        camera, created = Camera.objects.update_or_create(
            id=self.related_instance_id,
            defaults={
                'manufacturer': self.manufacturer,
                'model': self.model,
                'description': self.description,
                'tvl': self.tvl,
                'voltage_min': self.voltage_min,
                'voltage_max': self.voltage_max,
                'ratio': self.ratio,
                'fov': self.fov,
                'output_type': self.output_type,
                'light_sens': self.light_sens,
                'weight': self.weight,
            }
        )

        camera.full_clean()
        camera.save()
        camera.video_formats.set(self.video_formats.all())

        if created:
            self.related_instance = camera
            self.save()


        for suggested_image in self.suggested_images.all():
            if not suggested_image.object:
                suggested_image.object = camera
            suggested_image.save()

        for suggested_document in self.suggested_documents.all():
            if not suggested_document.object:
                suggested_document.object = camera
            suggested_document.save()

        for suggested_detail in self.suggested_details.all():
            camera_detail, created = CameraDetail.objects.update_or_create(
                id=suggested_detail.related_instance_id,
                camera=camera,
                defaults={
                    'height': suggested_detail.height,
                    'width': suggested_detail.width
                }
            )
            camera_detail.full_clean()
            camera_detail.save()

            if created:
                suggested_detail.related_instance = camera_detail
                suggested_detail.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_camera'

        verbose_name = _('Camera Suggestion')
        verbose_name_plural = _('Camera Suggestions')
        ordering = ['manufacturer', 'model', ]


class VideoFormatSuggestion(BaseVideoFormatMixin, BaseSuggestionMixin):
    related_instance = models.ForeignKey('components.VideoFormat', blank=True, null=True,
                                         related_name='submitted_suggestions',
                                         on_delete=models.CASCADE)

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()

        video_format, created = VideoFormat.objects.update_or_create(
            id=self.related_instance_id,
            defaults={
                'format': self.format,
            }
        )
        video_format.save()
        if created:
            self.related_instance = video_format
            self.save()

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

    @transaction.atomic
    def accept(self):
        self.reviewed = True
        self.accepted = True
        self.save()

        camera_detail, created = CameraDetail.objects.update_or_create(
            camera = self.camera,
            id = self.related_instance_id,
            defaults={
                'height': self.height,
                'width': self.width
            }
        )
        camera_detail.save()

        if created:
            self.related_instance = camera_detail
            self.save()

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_existing_camera_detail'

        verbose_name = _('Existing Camera Detail Suggestion')
        verbose_name_plural = _('Existing Camera Detail Suggestions')
        ordering = ['camera',]


class SuggestedCameraDetailSuggestion(BaseCameraDetailMixin):
    """ Add detail to suggested camera """
    suggestion = models.ForeignKey('suggestions.CameraSuggestion', on_delete=models.CASCADE, related_name='suggested_details', verbose_name='details')
    related_instance = models.ForeignKey('components.CameraDetail', on_delete=models.CASCADE, blank=True, null=True,
                                         related_name='submitted_suggestions', verbose_name='submitted_suggestions')

    class Meta:
        app_label = 'suggestions'
        db_table = 'suggestions_suggested_camera_detail'

        verbose_name = _('Suggested Camera Detail')
        verbose_name_plural = _('Suggested Camera Details')
        ordering = ['related_instance',]

    @transaction.atomic
    def delete(self, *args, **kwargs):
        if self.suggestion.suggested_details.count() > 1:
            super().delete(*args, **kwargs)
        else:
            raise models.ProtectedError(_("Cannot delete the only Detail for this object."), self)
