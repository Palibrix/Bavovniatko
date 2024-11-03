from django_filters import rest_framework as filters

from components.models import Receiver, AntennaConnector, ReceiverProtocolType


class ReceiverFilter(filters.FilterSet):
    frequency = filters.RangeFilter(field_name='details__frequency')
    telemetry_power = filters.RangeFilter(field_name='details__telemetry_power')
    weight = filters.RangeFilter(field_name='weight')

    antenna_connectors = filters.ModelMultipleChoiceFilter(
        field_name='antenna_connectors__type',
        to_field_name='type',
        queryset=AntennaConnector.objects.all(),
        conjoined=True,  # This ensures that all selected connectors must be present
    )

    protocols = filters.ModelMultipleChoiceFilter(
        field_name='protocols__type',
        to_field_name='type',
        queryset=ReceiverProtocolType.objects.all(),
        conjoined=True,
    )

    class Meta:
        model = Receiver
        fields = ['manufacturer', 'processor',
                  'antenna_connectors', 'protocols',
                  'frequency', 'telemetry_power', 'weight']
