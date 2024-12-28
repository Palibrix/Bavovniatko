from django.contrib import admin

from builds.models import Drone
from components.mixins import BaseModelAdminMixin
from documents.admin.builds_admin import DroneDocumentInlineAdmin
from galleries.admin.builds_admin import DroneGalleryInlineAdmin


@admin.register(Drone)
class DroneAdmin(BaseModelAdminMixin):
    inlines = [DroneGalleryInlineAdmin, DroneDocumentInlineAdmin]

    list_display = ('__str__', 'id', 'created_at', 'updated_at')

    list_filter = ('antenna', 'battery', 'camera', 'frame', 'motor',
                   'propeller', 'receiver', 'transmitter',
                   'flight_controller', 'speed_controller')

    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('model', 'id', 'manufacturer',)
