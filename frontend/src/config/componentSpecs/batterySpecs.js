import {
    faBatteryFull, faLayerGroup, faBolt,
    faWeightHanging, faRuler, faPlug
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for battery specifications
 */

// BATTERIES
export const batteryKeySpecs = [
    {
        label: 'Configuration',
        path: 'series', // Just need a property to trigger formatter
        icon: faLayerGroup,
        formatter: (_, item) => item.series && item.parallels ? `${item.series}S${item.parallels}P` : 'N/A'
    },
    {
        label: 'Capacity',
        path: 'capacity',
        icon: faBatteryFull,
        unit: 'mAh'
    },
    {
        label: 'Voltage',
        path: 'voltage',
        icon: faBatteryFull,
        unit: 'V'
    },
    {
        label: 'Type',
        path: 'type',
        icon: faBatteryFull,
        formatter: (value) => {
            const types = {
                'LIPO': 'LiPo',
                'LI_ION': 'Li-Ion',
                'LIHV': 'LiHV',
                'ANOTHER': 'Other'
            };
            return types[value] || value;
        }
    },
    {
        label: 'Discharge',
        path: 'discharge_current',
        icon: faBolt,
        unit: 'A'
    }
];

export const batterySpecs = [
    ...batteryKeySpecs,

    {
        label: 'Charge Current',
        path: 'charge_current',
        icon: faBolt,
        unit: 'A'
    },
    {
        label: 'Weight',
        path: 'weight',
        icon: faWeightHanging,
        unit: 'g'
    },
    {
        label: 'Size',
        path: 'size',
        icon: faRuler
    },
    {
        label: 'Dimensions',
        path: 'dimensions',
        icon: faRuler,
        formatter: (_, item) => `${item.length}×${item.height}×${item.width}mm`
    },
    {
        label: 'Connector',
        path: 'connector_type',
        icon: faPlug
    },
    {
        label: 'Balancer',
        path: 'balancer',
        icon: faPlug
    }
];