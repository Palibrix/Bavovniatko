from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins import BaseModelAdminMixin
from components.mixins.base_antenna_admin_mixins import AntennaAdminMixin, AntennaTypeAdminMixin, \
    AntennaConnectorAdminMixin
from components.models import Antenna, AntennaDetail, AntennaType, AntennaConnector
from documents.admin.components_admin import AntennaDocumentInline
from galleries.admin.components_admin import AntennaGalleryInline


class AntennaDetailInline(admin.StackedInline):
    model = AntennaDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'antenna'


@admin.register(Antenna)
class AntennaAdmin(AntennaAdminMixin):
    inlines = [AntennaDetailInline, AntennaGalleryInline, AntennaDocumentInline]


@admin.register(AntennaType)
class AntennaTypeAdmin(AntennaTypeAdminMixin):
    pass


@admin.register(AntennaConnector)
class AntennaConnectorAdmin(AntennaConnectorAdminMixin):
    pass
