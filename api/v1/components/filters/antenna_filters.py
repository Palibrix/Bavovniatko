from django_filters import rest_framework as filters

from components.models import Antenna, AntennaConnector


class AntennaFilter(filters.FilterSet):
    center_frequency = filters.RangeFilter(field_name='center_frequency')
    swr = filters.RangeFilter(field_name='swr',)
    gain = filters.RangeFilter(field_name='gain')
    radiation = filters.RangeFilter(field_name='radiation')
    weight = filters.RangeFilter(field_name='details__weight')

    class Meta:
        model = Antenna
        fields = ['manufacturer', 'center_frequency', 'bandwidth_min', 'bandwidth_max',
                  'swr', 'gain', 'radiation',
                  'type__type', 'type__direction', 'type__polarization',
                  'details__connector_type__type', 'details__angle_type',

                  'weight']
