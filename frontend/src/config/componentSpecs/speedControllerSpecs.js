import {
    faWeightHanging, faBatteryFull,
    faRuler, faWifi, faBolt, faExchangeAlt,
    faCode, faLayerGroup
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for speed controller (ESC) specifications
 */

// SPEED CONTROLLERS
export const speedControllerKeySpecs = [
    {
        label: 'Type',
        path: 'esc_type',
        icon: faLayerGroup,
        formatter: (value) => {
            const types = {
                'all': '4-in-1',
                'single': 'Single'
            };
            return types[value] || value;
        }
    },
    {
        label: 'Continuous Current',
        path: 'cont_current',
        icon: faBolt,
        unit: 'A'
    },
    {
        label: 'Burst Current',
        path: 'burst_current',
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
        label: 'Power Input',
        path: 'voltage.max_cells',
        icon: faBatteryFull,
        formatter: (_, item) => {
            if (!item.voltage) return 'N/A';
            return `${item.voltage.min_cells}-${item.voltage.max_cells}S ${item.voltage.type}`;
        }
    }
];

export const speedControllerSpecs = [
    ...speedControllerKeySpecs,

    {
        label: 'Mount Size',
        path: 'mount_dimensions',
        icon: faRuler,
        formatter: (_, item) => `${item.mount_length}×${item.mount_width}mm`
    },
    {
        label: 'Dimensions',
        path: 'dimensions',
        icon: faRuler,
        formatter: (_, item) => {
            if (item.height) {
                return `${item.length}×${item.height}×${item.width}mm`;
            }
            return `${item.length}×${item.width}mm`;
        }
    },
    {
        label: 'Wireless Config',
        path: 'is_wireless_conf',
        icon: faWifi,
        formatter: (value) => value ? 'Yes' : 'No'
    },
    {
        label: 'Protocols',
        path: 'protocols',
        icon: faExchangeAlt,
        formatter: (protocols) => {
            if (!protocols || !protocols.length) return 'N/A';
            return protocols.map(p => p.protocol).join(', ');
        }
    },
    {
        label: 'Firmwares',
        path: 'firmwares',
        icon: faCode,
        formatter: (firmwares) => {
            if (!firmwares || !firmwares.length) return 'N/A';
            return firmwares.map(f => f.firmware).join(', ');
        }
    }
];