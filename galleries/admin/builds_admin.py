from django.contrib import admin

from galleries.mixins import BaseGalleryInlineAdminMixin
from galleries.models import DroneGallery


class DroneGalleryInlineAdmin(BaseGalleryInlineAdminMixin):
    model = DroneGallery
