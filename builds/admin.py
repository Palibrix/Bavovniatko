from django.contrib import admin

from builds.models import Drone
from galleries.admin.builds_admin import DroneGalleryInlineAdmin


@admin.register(Drone)
class DroneAdmin(admin.ModelAdmin):
    inlines = [DroneGalleryInlineAdmin, ]

    list_display = ('__str__', 'id', 'created_at', 'updated_at')

    list_filter = ('antenna', 'battery', 'camera', 'frame', 'motor',
                   'propeller', 'receiver', 'transmitter',
                   'flight_controller', 'speed_controller')

    empty_value_display = '???'
    readonly_fields = ('id', 'created_at', 'updated_at')
    search_fields = ('model', 'id', 'manufacturer',)
    list_display_links = ('__str__',)