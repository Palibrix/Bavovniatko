from galleries.mixins import BaseGalleryInlineAdminMixin
from galleries.models import AntennaGallery


class AntennaGalleryInline(BaseGalleryInlineAdminMixin):
    model = AntennaGallery
