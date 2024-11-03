from documents.mixins import BaseDocumentInlineAdminMixin
from documents.models import DroneDocument


class DroneDocumentInlineAdmin(BaseDocumentInlineAdminMixin):
    model = DroneDocument
