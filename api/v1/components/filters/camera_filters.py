from django_filters import rest_framework as filters

from components.models import VideoFormat, Camera


class CameraFilter(filters.FilterSet):
    fov = filters.RangeFilter(field_name='fov')
    weight = filters.RangeFilter(field_name='weight')

    formats = filters.ModelMultipleChoiceFilter(
        field_name='video_formats__format',
        to_field_name='format',
        queryset=VideoFormat.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = Camera
        fields = ['manufacturer', 'voltage_min', 'voltage_max',
                  'ratio', 'output_type', 'formats', 'light_sens',
                  'fov', 'weight']
