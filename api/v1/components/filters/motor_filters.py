from django_filters import rest_framework as filters

from components.models import Motor


class MotorFilter(filters.FilterSet):
    max_power = filters.RangeFilter(field_name='details__max_power')
    kv_per_volt = filters.RangeFilter(field_name='details__kv_per_volt')
    peak_current = filters.RangeFilter(field_name='details__peak_current')
    idle_current = filters.RangeFilter(field_name='details__idle_current')
    weight = filters.RangeFilter(field_name='details__weight')

    class Meta:
        model = Motor
        fields = ['manufacturer', 'stator_diameter', 'stator_height',

                  'max_power', 'kv_per_volt',
                  'peak_current', 'idle_current',

                  'details__voltage__min_cells', 'details__voltage__max_cells',
                  'details__voltage__type',

                  'weight'
                  ]
