from django.contrib import admin

from components.mixins import BaseModelAdminMixin
from lists.models import List


@admin.register(List)
class ListAdmin(BaseModelAdminMixin):
    inlines = []

    list_display = ('name', 'id', 'owner', 'count_all', 'created_at', 'updated_at')
    list_filter = ('owner', )
    list_display_links = ('name', )
