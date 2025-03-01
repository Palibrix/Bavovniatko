from django.contrib import admin

from components.mixins.admin.base_propeller_admin_mixins import PropellerAdminMixin
from components.models import Propeller
from documents.admin.components_admin import PropellerDocumentInline
from galleries.admin.components_admin import PropellerGalleryInline


@admin.register(Propeller)
class PropellerAdmin(PropellerAdminMixin):
    inlines = [PropellerGalleryInline, PropellerDocumentInline]