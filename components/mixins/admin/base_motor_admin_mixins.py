from components.mixins import BaseModelAdminMixin


class MotorAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'configuration', 'get_stator_size', 'get_mount_dimensions')
    list_filter = ('manufacturer', 'configuration')
    search_fields = ('manufacturer', 'model')


class RatedVoltageAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'get_cells', 'type')
    list_filter = ('type', 'min_cells', 'max_cells')
    sortable_by = ('min_cells', 'max_cells')