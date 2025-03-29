import {
    faBroadcastTower, faMicrochip, faBatteryFull,
    faWeightHanging, faWifi, faExchangeAlt,
    faSignal
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for receiver specifications
 */

// RECEIVERS
export const receiverKeySpecs = [
    {
        label: 'Processor',
        path: 'processor',
        icon: faMicrochip
    },
    {
        label: 'Protocols',
        path: 'protocols',
        icon: faExchangeAlt,
        formatter: (protocols) => {
            if (!protocols || !protocols.length) return 'N/A';
            return protocols.map(p => p.type).join(', ');
        }
    },
    {
        label: 'Frequency',
        path: 'details',
        icon: faBroadcastTower,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return `${details[0].frequency}MHz`;
        }
    },
    {
        label: 'Voltage',
        path: 'voltage',
        icon: faBatteryFull,
        formatter: (_, item) => {
            if (!item.voltage_max) return `${item.voltage_min}V`;
            return `${item.voltage_min}-${item.voltage_max}V`;
        }
    }
];

export const receiverSpecs = [
    ...receiverKeySpecs,

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
        label: 'Telemetry Power',
        path: 'details',
        icon: faSignal,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return `${details[0].telemetry_power}dBm`;
        }
    },
    {
        label: 'RF Chip',
        path: 'details',
        icon: faMicrochip,
        formatter: (details) => {
            if (!details || !details.length || !details[0].rf_chip) return 'N/A';
            return details[0].rf_chip;
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