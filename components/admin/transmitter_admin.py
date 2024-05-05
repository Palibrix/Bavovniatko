from django.contrib import admin

from components.mixins import IsPublicMixin
from components.models.transmitter import TransmitterDetail, Transmitter


class TransmitterDetailInline(admin.StackedInline):
    model = TransmitterDetail
    min_num = 1
    extra = 0


@admin.register(Transmitter)
class TransmitterAdmin(admin.ModelAdmin, IsPublicMixin):
    inlines = [TransmitterDetailInline, ]
    list_display = ('model', 'id', 'get_input_voltage', 'output_voltage',
                    'output', 'get_params', 'is_public')
    list_filter = ('manufacturer', 'antenna_connector', 'video_format', 'microphone')
    search_fields = ('model', 'id', 'manufacturer')
