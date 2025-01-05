from rest_framework import serializers

from api.v1.components.serializers import AntennaConnectorSerializer, AntennaTypeSerializer, AntennaSerializer
from api.v1.documents.serializers import AntennaDocumentReadSerializer, AntennaDocumentWriteSerializer
from api.v1.galleries.serializers import AntennaGalleryReadSerializer, AntennaGalleryWriteSerializer
from api.v1.users.serializers import UserSerializer
from api.v1.utils import ReadOnlyModelSerializer
from components.models import AntennaType, AntennaConnector, Antenna
from galleries.models import AntennaGallery
from suggestions.models import AntennaSuggestion
from suggestions.models.antenna_suggestions import SuggestedAntennaDetailSuggestion
from drf_writable_nested.serializers import WritableNestedModelSerializer

class SuggestedAntennaDetailSuggestionSerializer(serializers.ModelSerializer):
    connector_type = AntennaConnectorSerializer(read_only=True)
    connector_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaConnector.objects.all(),
        write_only=True,
        source='connector_type',
        many=False,
    )

    class Meta:
        model = SuggestedAntennaDetailSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'suggestion', 'connector_type', 'related_instance']


class AntennaSuggestionReadSerializer(ReadOnlyModelSerializer):
    type = AntennaTypeSerializer(read_only=True)
    suggested_images = AntennaGalleryReadSerializer(many=True, read_only=True)
    suggested_documents = AntennaDocumentReadSerializer(many=True, read_only=True)
    suggested_details = SuggestedAntennaDetailSuggestionSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AntennaSuggestion
        fields = '__all__'


class AntennaSuggestionWriteSerializer(WritableNestedModelSerializer):
    type = AntennaTypeSerializer(read_only=True)
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=AntennaType.objects.all(),
        write_only=True,
        source='type',
    )
    # related_instance = AntennaSerializer(read_only=True)
    related_instance_id = serializers.PrimaryKeyRelatedField(
        queryset=Antenna.objects.all(),
        write_only=True,
        source='related_instance',
        required=False,
    )
    suggested_images = AntennaGalleryWriteSerializer(many=True)
    suggested_documents = AntennaDocumentWriteSerializer(many=True, required=False)
    suggested_details = SuggestedAntennaDetailSuggestionSerializer(many=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = AntennaSuggestion
        fields = '__all__'
        read_only_fields = ['id', 'related_instance', 'user', 'type', 'reviewed', 'accepted', 'admin_comment']

    def validate(self, attrs):
        antenna_suggestion = self.instance
        suggested_images = attrs.get('suggested_images')
        if suggested_images:
            for image in suggested_images:
                if image.get('id') and image['id'] not in antenna_suggestion.suggested_images.values_list('id', flat=True):
                    raise serializers.ValidationError(
                        f"Image with id {image['id']} does not belong to Suggestion with id {antenna_suggestion.id}")
        return attrs

    def update(self, instance, validated_data):
        validated_data['accepted'] = False
        validated_data['reviewed'] = False
        return super().update(instance, validated_data)

    # def update(self, instance, validated_data):
    #     self.update_instances(instance, validated_data.pop('suggested_images', None), 'suggested_images', AntennaGallery)
    #     self.update_instances(instance, validated_data.pop('suggested_documents', None), 'suggested_documents', AntennaDocument)
    #     self.update_instances(instance, validated_data.pop('suggested_details', None), 'suggested_details', SuggestedAntennaDetailSuggestion)
    #
    #     return super().update(instance, validated_data)
    #
    # def update_instances(self, instance, data, field_name, model_class):
    #     if data is not None:
    #         instances_dict = dict((i.id, i) for i in getattr(instance, field_name).all())
    #
    #         for item_data in data:
    #             if 'id' in item_data and item_data['id'] in instances_dict:
    #                 item_instance = instances_dict.pop(item_data['id'])
    #                 item_data.pop('id')
    #                 for key in item_data.keys():
    #                     setattr(item_instance, key, item_data[key])
    #                 item_instance.save()
    #             else:
    #                 if 'id' in item_data:
    #                     item_data.pop('id')
    #                 model_class.objects.create(suggestion=instance, **item_data)
    #
    #         for item in instances_dict.values():
    #             item.delete()
