from components.mixins import BaseModelAdminMixin


class FrameAdminMixin(BaseModelAdminMixin):
    list_display = ('__str__', 'id', 'prop_size', 'size',  'material', 'configuration')
    list_filter = ('manufacturer', 'material', 'configuration')
    sortable_by = ('weight', )
    search_fields = ('model', 'id', 'prop_size', 'size')