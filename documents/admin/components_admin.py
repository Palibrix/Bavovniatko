# flake8: noqa
from documents.mixins import BaseDocumentInlineAdminMixin
from documents.models import *


class AntennaDocumentInline(BaseDocumentInlineAdminMixin):
    model = AntennaDocument


class CameraDocumentInline(BaseDocumentInlineAdminMixin):
    model = CameraDocument


class FrameDocumentInline(BaseDocumentInlineAdminMixin):
    model = FrameDocument


class FlightControllerDocumentInline(BaseDocumentInlineAdminMixin):
    model = FlightControllerDocument


class MotorDocumentInline(BaseDocumentInlineAdminMixin):
    model = MotorDocument


class PropellerDocumentInline(BaseDocumentInlineAdminMixin):
    model = PropellerDocument


class ReceiverDocumentInline(BaseDocumentInlineAdminMixin):
    model = ReceiverDocument


class StackDocumentInline(BaseDocumentInlineAdminMixin):
    model = StackDocument


class SpeedControllerDocumentInline(BaseDocumentInlineAdminMixin):
    model = SpeedControllerDocument


class TransmitterDocumentInline(BaseDocumentInlineAdminMixin):
    model = TransmitterDocument
