from django.conf import settings
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from documents.mixins import Base64ValidatedFileField


def validate_file_size(file):
    max_size = getattr(settings, 'MAX_DOCUMENT_FILE_SIZE', 25 * 1024 * 1024)
    if file.size > max_size:
        raise ValidationError(_(f'File size must not exceed {filesizeformat(max_size)}'))


class BaseDocumentWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    file = Base64ValidatedFileField(validators=[validate_file_size])

    def validate_id(self, value):
        if not value:
            return value

        # Skip validation during creation
        if not self.context.get('suggestion'):
            return value

        try:
            document = self.Meta.model.objects.get(id=value)
        except self.Meta.model.DoesNotExist:
            raise serializers.ValidationError(_("Document with this ID does not exist"))

        suggestion = self.context.get('suggestion')
        if document.suggestion != suggestion:
            raise serializers.ValidationError(_("Invalid document ID"))

        return value


class DocumentContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action in ['update', 'partial_update']:
            context['suggestion'] = self.get_object()
        return context