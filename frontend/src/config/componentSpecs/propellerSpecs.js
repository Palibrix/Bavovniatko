import {
    faFan, faRuler, faWeightHanging,
    faAngleUp, faLayerGroup
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for propeller specifications
 */

// PROPELLERS
export const propellerKeySpecs = [
    {
        label: 'Size',
        path: 'size',
        icon: faRuler,
        unit: '\"'
    },
    {
        label: 'Pitch',
        path: 'pitch',
        icon: faAngleUp,
        unit: '\"'
    },
    {
        label: 'Size/Pitch',
        path: 'size_pitch',
        icon: faFan,
        formatter: (_, item) => `${item.size}×${item.pitch}`
    },
    {
        label: 'Blade Count',
        path: 'blade_count',
        icon: faLayerGroup,
        formatter: (value) => {
            const blades = {
                '2': '2 blades',
                '3': '3 blades',
                '4': '4 blades',
                '5': '5 blades',
                '6': '6 blades',
                '7': '7 blades',
                '8': '8 blades',
                'another': 'Other'
            };
            return blades[value] || value;
        }
    },
    {
        label: 'Weight',
        path: 'weight',
        icon: faWeightHanging,
        unit: 'g'
    }
];

// For propellers, key specs cover everything from the model
export const propellerSpecs = [
    ...propellerKeySpecs
];