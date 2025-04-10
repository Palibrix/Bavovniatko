from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class AntennaTransmitterCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between antenna and transmitter components.
    Checks:
    1. Frequency range compatibility - antenna bandwidth must overlap with transmitter frequency range
    2. Connector compatibility - antenna and transmitter must have matching connectors
    """

    def check_compatibility(self, antenna, transmitter):
        """
        Check if antenna is compatible with transmitter.

        Args:
            antenna: Antenna instance
            transmitter: Transmitter instance

        Returns:
            dict: Compatibility result with 'is_compatible' flag and 'issues' list
        """
        issues = []

        # Check 1: Frequency compatibility
        if not antenna.bandwidth_min or not antenna.bandwidth_max:
            issues.append({
                'type': 'missing_frequency_range',
                'severity': 'critical',
                'message': 'Antenna is missing frequency range information',
                'component_refs': ['antenna_transmitter']
            })
        elif not hasattr(transmitter, 'input_voltage_min') or not hasattr(transmitter, 'input_voltage_max'):
            # Transmitter may not have explicit frequency range fields, but we need to check
            # For now, mark as compatible as we don't have enough information
            pass
        else:
            # Check for frequency range overlap
            # Note: We're checking if the antenna bandwidth overlaps with any of the
            # transmitter's frequency ranges, which are not explicitly defined in the model
            # This is a placeholder and should be adjusted based on actual model structure
            transmitter_min_freq = getattr(transmitter, 'frequency_min', None)
            transmitter_max_freq = getattr(transmitter, 'frequency_max', None)

            if transmitter_min_freq is not None and transmitter_max_freq is not None:
                # Check if ranges overlap
                if not (
                        antenna.bandwidth_max >= transmitter_min_freq and antenna.bandwidth_min <= transmitter_max_freq):
                    issues.append({
                        'type': 'frequency_range_mismatch',
                        'severity': 'critical',
                        'message': f"Antenna frequency range ({antenna.bandwidth_min}-{antenna.bandwidth_max}) doesn't overlap with transmitter range ({transmitter_min_freq}-{transmitter_max_freq})",
                        'component_refs': ['antenna_transmitter', 'transmitter']
                    })

        # Check 2: Connector compatibility
        if not antenna.details.exists():
            issues.append({
                'type': 'missing_antenna_details',
                'severity': 'critical',
                'message': 'Antenna is missing connector information',
                'component_refs': ['antenna_transmitter']
            })
        elif not transmitter.antenna_connectors.exists():
            issues.append({
                'type': 'missing_transmitter_connectors',
                'severity': 'critical',
                'message': 'Transmitter is missing antenna connector information',
                'component_refs': ['transmitter']
            })
        else:
            connector_compatible = False
            for antenna_detail in antenna.details.all():
                connector_id = antenna_detail.connector_type.id
                if transmitter.antenna_connectors.filter(id=connector_id).exists():
                    connector_compatible = True
                    break

            if not connector_compatible:
                issues.append({
                    'type': 'connector_mismatch',
                    'severity': 'critical',
                    'message': 'Antenna connector type is incompatible with transmitter',
                    'component_refs': ['antenna_transmitter', 'transmitter']
                })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'antenna_transmitter' or 'transmitter'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'antenna_transmitter' and hasattr(other_component, 'antenna_connectors'):
            # Filtering antennas based on transmitter
            transmitter = other_component
            if transmitter.antenna_connectors.exists():
                connector_ids = list(transmitter.antenna_connectors.values_list('id', flat=True))

                # Also get frequency range if available
                freq_range = None
                if hasattr(transmitter, 'frequency_min') and hasattr(transmitter, 'frequency_max'):
                    freq_min = getattr(transmitter, 'frequency_min')
                    freq_max = getattr(transmitter, 'frequency_max')
                    if freq_min is not None and freq_max is not None:
                        freq_range = (freq_min, freq_max)

                return {
                    'connector_ids': connector_ids,
                    'frequency_range': freq_range
                }

        elif component_type == 'transmitter' and hasattr(other_component, 'details'):
            # Filtering transmitters based on antenna
            antenna = other_component
            if antenna.details.exists():
                # Get all antenna connector types
                connector_ids = []
                for detail in antenna.details.all():
                    if detail.connector_type:
                        connector_ids.append(detail.connector_type.id)

                # Get antenna frequency range
                freq_range = None
                if antenna.bandwidth_min is not None and antenna.bandwidth_max is not None:
                    freq_range = (antenna.bandwidth_min, antenna.bandwidth_max)

                return {
                    'connector_ids': connector_ids,
                    'frequency_range': freq_range
                }

        return {}

    def apply_filters(self, component_type, queryset, filter_params):
        """
        Apply filter parameters to queryset.

        Args:
            component_type: Either 'antenna_transmitter' or 'transmitter'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'antenna_transmitter':
            # Filtering antennas
            if 'connector_ids' in filter_params and filter_params['connector_ids']:
                queryset = queryset.filter(details__connector_type__id__in=filter_params['connector_ids'])

            if 'frequency_range' in filter_params and filter_params['frequency_range']:
                min_freq, max_freq = filter_params['frequency_range']
                # Check for overlap: not (antenna.max < tx.min or antenna.min > tx.max)
                queryset = queryset.exclude(
                    Q(bandwidth_max__lt=min_freq) | Q(bandwidth_min__gt=max_freq)
                )

        elif component_type == 'transmitter':
            # Filtering transmitters
            if 'connector_ids' in filter_params and filter_params['connector_ids']:
                queryset = queryset.filter(antenna_connectors__id__in=filter_params['connector_ids'])

            if 'frequency_range' in filter_params and filter_params['frequency_range']:
                min_freq, max_freq = filter_params['frequency_range']
                # Check for overlap with transmitter frequency range (if those fields exist)
                if hasattr(queryset.model, 'frequency_min') and hasattr(queryset.model, 'frequency_max'):
                    queryset = queryset.exclude(
                        Q(frequency_max__lt=min_freq) | Q(frequency_min__gt=max_freq)
                    )

        return queryset.distinct()


# Register this checker with the registry
register_checker('antenna_transmitter', 'transmitter', AntennaTransmitterCompatibilityChecker)