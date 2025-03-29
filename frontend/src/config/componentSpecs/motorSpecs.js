import {
    faCog, faRuler, faWeightHanging,
    faBolt, faTachometerAlt, faChartLine,
    faDatabase, faBatteryFull
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for motor specifications
 */

// MOTORS
export const motorKeySpecs = [
    {
        label: 'Stator Size',
        path: 'stator_size',
        icon: faRuler,
        formatter: (_, item) => `${item.stator_diameter}${item.stator_height}`
    },
    {
        label: 'KV Rating',
        path: 'details',
        icon: faTachometerAlt,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return `${details[0].kv_per_volt} KV`;
        }
    },
    {
        label: 'Weight',
        path: 'details',
        icon: faWeightHanging,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return `${details[0].weight}g`;
        }
    },
    {
        label: 'Mount',
        path: 'mount_dimensions',
        icon: faCog,
        formatter: (_, item) => `${item.mount_width}×${item.mount_height}mm`
    },
    {
        label: 'Configuration',
        path: 'configuration',
        icon: faDatabase
    }
];

export const motorSpecs = [
    ...motorKeySpecs,

    {
        label: 'Max Power',
        path: 'details',
        icon: faBolt,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return `${details[0].max_power}W`;
        }
    },
    {
        label: 'Peak Current',
        path: 'details',
        icon: faChartLine,
        formatter: (details) => {
            if (!details || !details.length || !details[0].peak_current) return 'N/A';
            return `${details[0].peak_current}A`;
        }
    },
    {
        label: 'Idle Current',
        path: 'details',
        icon: faChartLine,
        formatter: (details) => {
            if (!details || !details.length || !details[0].idle_current) return 'N/A';
            return `${details[0].idle_current}A`;
        }
    },
    {
        label: 'Resistance',
        path: 'details',
        icon: faChartLine,
        formatter: (details) => {
            if (!details || !details.length || !details[0].resistance) return 'N/A';
            return `${details[0].resistance}mΩ`;
        }
    },
    {
        label: 'Voltage Range',
        path: 'details',
        icon: faBatteryFull,
        formatter: (details) => {
            if (!details || !details.length || !details[0].voltage) return 'N/A';
            return `${details[0].voltage.min_cells}-${details[0].voltage.max_cells}S ${details[0].voltage.type}`;
        }
    }
];