from rest_framework import serializers

from api.v1.users.serializers import UserSerializer


class BaseSuggestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        abstract = True
        read_only_fields = ['id', 'user', 'status', 'admin_comment']


class ValidateSuggestionNestedFieldsMixin:
    def validate(self, attrs):
        suggestion = self.instance
        suggested_images = attrs.get('suggested_images')
        suggested_documents = attrs.get('suggested_documents')
        suggested_details = attrs.get('suggested_details')
        if suggested_images:
            for image in suggested_images:
                if image.get('id') and image['id'] not in suggestion.suggested_images.values_list('id', flat=True):
                    raise serializers.ValidationError(
                        f"Image with id {image['id']} does not belong to Suggestion with id {suggestion.id}")
        if suggested_documents:
            for document in suggested_documents:
                if document.get('id') and document['id'] not in attrs.get('suggested_documents').values_list('id', flat=True):
                    raise serializers.ValidationError(
                        f"Document with id {document['id']} does not belong to Suggestion with id {suggestion.id}"
                    )
        if suggested_details:
            for detail in suggested_details:
                if detail.get('id') and detail['id'] not in attrs.get('suggested_details').values_list('id', flat=True):
                    raise serializers.ValidationError(
                        f"Detail with id {detail['id']} does not belong to Suggestion with id {suggestion.id}"
                    )
        return super().validate(attrs)