import {
    faMicrochip, faWeightHanging, faBatteryFull,
    faRuler, faWifi, faServer,
    faCode, faPlug, faCompass
} from '@fortawesome/free-solid-svg-icons';

import {faBluetoothB} from '@fortawesome/free-brands-svg-icons';

/**
 * Configuration for flight controller specifications
 */

// FLIGHT CONTROLLERS
export const flightControllerKeySpecs = [
    {
        label: 'Microcontroller',
        path: 'microcontroller',
        icon: faMicrochip
    },
    {
        label: 'Gyro',
        path: 'gyro.imu',
        icon: faCompass
    },
    {
        label: 'Mount Size',
        path: 'mount_dimensions',
        icon: faRuler,
        formatter: (_, item) => `${item.mount_length}×${item.mount_width}mm`
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

export const flightControllerSpecs = [
    ...flightControllerKeySpecs,

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
        label: 'OSD Chip',
        path: 'osd',
        icon: faServer
    },
    {
        label: 'Bluetooth',
        path: 'bluetooth',
        icon: faBluetoothB,
        formatter: (value) => value ? 'Yes' : 'No'
    },
    {
        label: 'WiFi',
        path: 'wifi',
        icon: faWifi,
        formatter: (value) => value ? 'Yes' : 'No'
    },
    {
        label: 'Barometer',
        path: 'barometer',
        icon: faCompass,
        formatter: (value) => value ? 'Yes' : 'No'
    },
    {
        label: 'Connector Type',
        path: 'connector_type',
        icon: faPlug,
        formatter: (value) => {
            const connectors = {
                'micro': 'Micro-USB',
                'c': 'Type C',
                'another': 'Other'
            };
            return connectors[value] || value;
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