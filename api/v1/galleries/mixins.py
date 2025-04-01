from django.conf import settings
from django.template.defaultfilters import filesizeformat
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_image_size(image):
    max_size = getattr(settings, 'MAX_GALLERY_IMAGE_SIZE', 5 * 1024 * 1024)
    if image.size > max_size:
        raise ValidationError(_(f'Image size must not exceed {filesizeformat(max_size)}'))


class BaseGalleryWriteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    image = Base64ImageField(validators=[validate_image_size], required=False)

    def validate(self, data):

        # Case 2: Existing image unchanged (id present, no image)
        if data.get('id') and 'image' not in data:
            return data

        # Case 3: New image (no id, image present)
        if not data.get('id') and 'image' in data:
            return data

        # If none of these cases match, raise validation error
        if data.get('id') and 'image' in data:
            raise serializers.ValidationError(
                _("Cannot provide both id and image - either keep existing image (id only) or upload new one (image only)"))

        if not data.get('id') and 'image' not in data:
            raise serializers.ValidationError(_("Either id or image must be provided"))

        return data

    def validate_id(self, value):
        if not value:
            return value

        # Skip validation during creation
        if not self.context.get('suggestion'):
            return value

        try:
            gallery = self.Meta.model.objects.get(id=value)
        except self.Meta.model.DoesNotExist:
            raise serializers.ValidationError(_("Gallery with this ID does not exist"))

        suggestion = self.context.get('suggestion')
        if gallery.suggestion != suggestion:
            raise serializers.ValidationError(_("Invalid gallery ID"))

        return value

class GalleryContextMixin:
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if not getattr(self, 'swagger_fake_view', False):
            if self.action in ['update', 'partial_update']:
                context['suggestion'] = self.get_object()
        return context
