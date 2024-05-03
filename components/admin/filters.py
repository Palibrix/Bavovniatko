from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class IsPublicFilter(admin.SimpleListFilter):
    title = _('Public status')
    parameter_name = 'is_public'

    def lookups(self, request, model_admin):
        return (
            ('true', _('Public')),
            ('false', _('Private')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'true':
            return queryset.filter(user__isnull=True)
        if self.value() == 'false':
            return queryset.filter(user__isnull=False)
        return queryset
