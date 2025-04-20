from documents.mixins import BaseDocumentInlineAdminMixin
from documents.models import DroneDocument


class DroneDocumentInlineAdmin(BaseDocumentInlineAdminMixin):
    model = DroneDocument
    readonly_fields = ('object', 'created_at')
