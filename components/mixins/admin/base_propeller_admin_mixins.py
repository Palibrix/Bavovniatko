from components.mixins import BaseModelAdminMixin


class PropellerAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'size', 'pitch', 'blade_count')
    list_filter = ('manufacturer', 'blade_count', 'weight')
    search_fields = ('manufacturer', 'model', 'id', 'size', 'pitch',)
    sortable_by = ('manufacturer', 'weight')