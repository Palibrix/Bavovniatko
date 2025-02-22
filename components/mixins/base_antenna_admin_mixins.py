from components.mixins import BaseModelAdminMixin


class AntennaAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'type', 'center_frequency', 'get_bandwidth', 'swr', 'radiation')
    sortable_by = ('swr', 'radiation',)
    list_filter = ('manufacturer', 'type', 'center_frequency', 'swr')
    search_fields = ('manufacturer', 'model', 'id',)


class AntennaTypeAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__',)
    list_filter = ('direction', 'polarization',)
    search_fields = ('type',)


class AntennaConnectorAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', )
    list_filter = ('type', )
    search_fields = ('type',)