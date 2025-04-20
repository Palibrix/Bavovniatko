from galleries.mixins import BaseGalleryInlineAdminMixin
from galleries.models import DroneGallery


class DroneGalleryInlineAdmin(BaseGalleryInlineAdminMixin):
    model = DroneGallery
    readonly_fields = ('object', 'created_at')
