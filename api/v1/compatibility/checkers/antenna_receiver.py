from django.db.models import Q

from api.v1.compatibility.checkers import register_checker
from api.v1.compatibility.checkers.base import BaseCompatibilityChecker


class AntennaReceiverCompatibilityChecker(BaseCompatibilityChecker):
    """
    Checker for compatibility between antenna and receiver components.
    Checks:
    1. Frequency compatibility - antenna bandwidth must include receiver frequency
    2. Connector compatibility - antenna and receiver must have matching connectors
    """

    def check_compatibility(self, antenna, receiver):
        """
        Check if antenna is compatible with receiver.

        Args:
            antenna: Antenna instance
            receiver: Receiver instance

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
                'component_refs': ['antenna_receiver']
            })
        elif not receiver.details.exists():
            issues.append({
                'type': 'missing_receiver_details',
                'severity': 'critical',
                'message': 'Receiver is missing detail information including frequency',
                'component_refs': ['receiver']
            })
        else:
            # Check frequency compatibility for each receiver detail
            frequency_compatible = False
            receiver_frequencies = []

            for detail in receiver.details.all():
                receiver_frequencies.append(detail.frequency)
                if antenna.bandwidth_min <= detail.frequency <= antenna.bandwidth_max:
                    frequency_compatible = True
                    break

            if not frequency_compatible:
                issues.append({
                    'type': 'frequency_mismatch',
                    'severity': 'critical',
                    'message': f"Antenna frequency range ({antenna.bandwidth_min}-{antenna.bandwidth_max}) doesn't support receiver frequencies {receiver_frequencies}",
                    'component_refs': ['antenna_receiver', 'receiver']
                })

        # Check 2: Connector compatibility
        if not antenna.details.exists():
            issues.append({
                'type': 'missing_antenna_details',
                'severity': 'critical',
                'message': 'Antenna is missing connector information',
                'component_refs': ['antenna_receiver']
            })
        elif not receiver.antenna_connectors.exists():
            issues.append({
                'type': 'missing_receiver_connectors',
                'severity': 'critical',
                'message': 'Receiver is missing antenna connector information',
                'component_refs': ['receiver']
            })
        else:
            connector_compatible = False
            for antenna_detail in antenna.details.all():
                connector_id = antenna_detail.connector_type.id
                if receiver.antenna_connectors.filter(id=connector_id).exists():
                    connector_compatible = True
                    break

            if not connector_compatible:
                issues.append({
                    'type': 'connector_mismatch',
                    'severity': 'critical',
                    'message': 'Antenna connector type is incompatible with receiver',
                    'component_refs': ['antenna_receiver', 'receiver']
                })

        # Check 3: Polarization recommendation (optional)
        if hasattr(antenna, 'type') and antenna.type and hasattr(antenna.type, 'polarization'):
            polarization = antenna.type.polarization
            if polarization == 'linear':
                issues.append({
                    'type': 'polarization_recommendation',
                    'severity': 'recommendation',
                    'message': 'Consider using circular polarized antennas for better reception',
                    'component_refs': ['antenna_receiver']
                })

        return {
            'is_compatible': len([issue for issue in issues if issue['severity'] == 'critical']) == 0,
            'issues': issues
        }

    def get_filter_params(self, component_type, other_component):
        """
        Get filter parameters for efficient component filtering.

        Args:
            component_type: Either 'antenna_receiver' or 'receiver'
            other_component: The other component to filter against

        Returns:
            dict: Filter parameters for efficient querying
        """
        if component_type == 'antenna_receiver' and hasattr(other_component, 'antenna_connectors'):
            # Filtering antennas based on receiver
            receiver = other_component
            if receiver.antenna_connectors.exists():
                connector_ids = list(receiver.antenna_connectors.values_list('id', flat=True))

                # Also get frequency range if available
                freq_q = Q()
                if receiver.details.exists():
                    for detail in receiver.details.all():
                        freq_q |= Q(bandwidth_min__lte=detail.frequency, bandwidth_max__gte=detail.frequency)

                return {
                    'connector_ids': connector_ids,
                    'frequency_q': freq_q if freq_q else None
                }

        elif component_type == 'receiver' and hasattr(other_component, 'details'):
            # Filtering receivers based on antenna
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
            component_type: Either 'antenna_receiver' or 'receiver'
            queryset: Base queryset to filter
            filter_params: Filter parameters from get_filter_params

        Returns:
            QuerySet: Filtered queryset
        """
        if component_type == 'antenna_receiver':
            # Filtering antennas
            if 'connector_ids' in filter_params and filter_params['connector_ids']:
                queryset = queryset.filter(details__connector_type__id__in=filter_params['connector_ids'])

            if 'frequency_q' in filter_params and filter_params['frequency_q']:
                queryset = queryset.filter(filter_params['frequency_q'])

        elif component_type == 'receiver':
            # Filtering receivers
            if 'connector_ids' in filter_params and filter_params['connector_ids']:
                queryset = queryset.filter(antenna_connectors__id__in=filter_params['connector_ids'])

            if 'frequency_range' in filter_params and filter_params['frequency_range']:
                min_freq, max_freq = filter_params['frequency_range']
                queryset = queryset.filter(details__frequency__gte=min_freq, details__frequency__lte=max_freq)

        return queryset.distinct()


# Register this checker with the registry
register_checker('antenna_receiver', 'receiver', AntennaReceiverCompatibilityChecker)