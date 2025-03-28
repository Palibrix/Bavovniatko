import {
    faBroadcastTower, faArrowsAltH, faSignal,
    faTags, faCompass, faSyncAlt, faWaveSquare,
    faChartPie
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for component specifications to display in list and detail views
 * Each component type has configurations for:
 * - keySpecs: Shown in the sidebar key specs panel (4-6 most important specs)
 * - fullSpecs: All specifications shown in the specifications tab
 */

// ANTENNAS
export const antennaKeySpecs = [
    {
        label: 'Center Frequency',
        path: 'center_frequency',
        icon: faBroadcastTower,
        unit: 'MHz'
    },
    {
        label: 'Gain',
        path: 'gain',
        icon: faSignal,
        unit: 'dBi'
    },
    {
        label: 'Polarization',
        path: 'type.polarization',
        icon: faSyncAlt
    },
    {
        label: 'Type',
        path: 'type.type',
        icon: faTags
    },
    {
        label: 'Bandwidth',
        path: 'bandwidth',
        icon: faArrowsAltH,
        // Special formatter to combine bandwidth_min and bandwidth_max
        formatter: (_, item) => `${item.bandwidth_min} - ${item.bandwidth_max} MHz`
    },
];

export const antennaSpecs = [
    ...antennaKeySpecs,

    {
        label: 'Direction',
        path: 'type.direction',
        icon: faCompass
    },
    {
        label: 'SWR',
        path: 'swr',
        icon: faWaveSquare
    },
    {
        label: 'Radiation Efficiency',
        path: 'radiation',
        icon: faChartPie,
        unit: '%'
    }
];