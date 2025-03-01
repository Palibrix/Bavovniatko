from components.mixins import BaseModelAdminMixin


class CameraAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'output_type', 'tvl', 'get_voltage', 'light_sens', 'ratio', 'fov')
    list_filter = ('manufacturer', 'light_sens', 'output_type', 'ratio')
    sortable_by = ('weight',)
    search_fields = ('model', 'manufacturer', 'id', 'tvl')


class VideoFormatAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__',)
    list_filter = ('format',)
    search_fields = ('format',)