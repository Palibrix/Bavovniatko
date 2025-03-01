from django.contrib import admin

from builds.forms import RequiredInlineFormSet
from components.mixins.admin.base_receiver_admin_mixins import ReceiverAdminMixin, ReceiverProtocolTypeAdminMixin
from components.models import Receiver, ReceiverDetail, ReceiverProtocolType
from documents.admin.components_admin import ReceiverDocumentInline
from galleries.admin.components_admin import ReceiverGalleryInline


class ReceiverDetailInline(admin.StackedInline):
    model = ReceiverDetail
    min_num = 1
    extra = 0
    formset = RequiredInlineFormSet
    fk_name = 'receiver'


@admin.register(Receiver)
class ReceiverAdmin(ReceiverAdminMixin):
    inlines = [ReceiverDetailInline, ReceiverGalleryInline, ReceiverDocumentInline]


@admin.register(ReceiverProtocolType)
class ReceiverProtocolTypeAdmin(ReceiverProtocolTypeAdminMixin):
    pass