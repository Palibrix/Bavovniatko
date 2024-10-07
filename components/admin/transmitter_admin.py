from django.contrib import admin

from components.mixins import BaseModelAdminMixin
from components.models.transmitter import OutputPower, Transmitter


@admin.register(Transmitter)
class TransmitterAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'get_input_voltage', 'output_voltage',
                    'output', 'get_dimensions', 'max_power',
                    'microphone')
    list_filter = ('manufacturer', 'output',
                   'antenna_connectors', 'video_formats', 'output_powers',
                   'microphone')
    search_fields = ('model', 'id', 'manufacturer', 'max_power')
    sortable_by = ('channels_quantity', 'max_power')


@admin.register(OutputPower)
class OutputPowerAdmin(BaseModelAdminMixin):
    list_display = ('__str__', 'id')
