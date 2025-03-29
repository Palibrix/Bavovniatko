import {
    faBroadcastTower, faWeightHanging, faBatteryFull,
    faRuler, faWifi, faBolt, faVideo, faVolumeUp, faNetworkWired
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for video transmitter specifications
 */

// TRANSMITTERS
export const transmitterKeySpecs = [
    {
        label: 'Output Type',
        path: 'output',
        icon: faVideo,
        formatter: (value) => value === 'A' ? 'Analog' : value === 'D' ? 'Digital' : value
    },
    {
        label: 'Max Power',
        path: 'max_power',
        icon: faBolt,
        unit: 'mW'
    },
    {
        label: 'Channels',
        path: 'channels_quantity',
        icon: faNetworkWired
    },
    {
        label: 'Input Voltage',
        path: 'input_voltage',
        icon: faBatteryFull,
        formatter: (_, item) => `${item.input_voltage_min}-${item.input_voltage_max}V`
    },
    {
        label: 'Output Voltage',
        path: 'output_voltage',
        icon: faBolt,
        unit: 'V'
    }
];

export const transmitterSpecs = [
    ...transmitterKeySpecs,

    {
        label: 'Dimensions',
        path: 'dimensions',
        icon: faRuler,
        formatter: (_, item) => `${item.length}×${item.height}×${item.thickness}mm`
    },
    {
        label: 'Weight',
        path: 'weight',
        icon: faWeightHanging,
        unit: 'g'
    },
    {
        label: 'Microphone',
        path: 'microphone',
        icon: faVolumeUp,
        formatter: (value) => value ? 'Yes' : 'No'
    },
    {
        label: 'Video Formats',
        path: 'video_formats',
        icon: faVideo,
        formatter: (formats) => {
            if (!formats || !formats.length) return 'N/A';
            return formats.map(f => f.format).join(', ');
        }
    },
    {
        label: 'Output Powers',
        path: 'output_powers',
        icon: faBroadcastTower,
        formatter: (powers) => {
            if (!powers || !powers.length) return 'N/A';
            return powers.map(p => `${p.output_power}mW`).join(', ');
        }
    },
    {
        label: 'Antenna Connectors',
        path: 'antenna_connectors',
        icon: faWifi,
        formatter: (connectors) => {
            if (!connectors || !connectors.length) return 'N/A';
            return connectors.map(c => c.type).join(', ');
        }
    }
];