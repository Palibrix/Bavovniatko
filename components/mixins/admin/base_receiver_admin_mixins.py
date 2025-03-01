from components.mixins import BaseModelAdminMixin


class ReceiverAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'processor', 'get_voltage')
    list_filter = ('manufacturer',)
    search_fields = ('model', 'id', 'processor', 'manufacturer')
    sortable_by = ('manufacturer', 'voltage_min', 'voltage_max')


class ReceiverProtocolTypeAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id')
    search_fields = ('type',)