from django.contrib import admin

from galleries.models import DroneGallery


class DroneGalleryInlineAdmin(admin.StackedInline):
    model = DroneGallery
