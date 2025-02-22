from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from api.v1.components.serializers import PropellerSerializer
from api.v1.documents.serializers import PropellerDocumentWriteSerializer
from api.v1.galleries.serializers import PropellerGalleryWriteSerializer
from api.v1.suggestions.mixins import BaseSuggestionSerializer
from api.v1.users.serializers import UserSerializer
from components.models import Propeller
from suggestions.models import PropellerSuggestion


class PropellerSuggestionSerializer(WritableNestedModelSerializer, BaseSuggestionSerializer):
    """Write serializer for propeller suggestions with nested data handling"""
    suggested_images = PropellerGalleryWriteSerializer(many=True)
    suggested_documents = PropellerDocumentWriteSerializer(many=True, required=False)
    related_instance = PropellerSerializer(read_only=True)

    class Meta(BaseSuggestionSerializer.Meta):
        model = PropellerSuggestion
        fields = '__all__'