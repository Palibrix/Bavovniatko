from django.utils.translation import gettext_lazy as _

from components.mixins import BaseComponentMixin, BaseModelMixin
from components.mixins.base_camera_mixins import BaseCameraMixin, BaseCameraDetailMixin, BaseVideoFormatMixin


class Camera(BaseComponentMixin, BaseCameraMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_camera'

        verbose_name = _('Camera')
        verbose_name_plural = _('Cameras')
        ordering = ['manufacturer', 'model']
        unique_together = (('manufacturer', 'model'),)


class CameraDetail(BaseModelMixin, BaseCameraDetailMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_camera_detail'

        verbose_name = _('Camera Detail')
        verbose_name_plural = _('Camera Details')
        unique_together = ['camera', 'height', 'width']


class VideoFormat(BaseModelMixin, BaseVideoFormatMixin):

    class Meta:
        app_label = 'components'
        db_table = 'components_video_format'

        verbose_name = _('Video Format')
        verbose_name_plural = _('Video Formats')
