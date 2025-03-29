import {
    faBorderAll, faRuler, faWeightHanging,
    faLayerGroup, faCubes, faExpand,
    faCamera, faCog, faSatelliteDish
} from '@fortawesome/free-solid-svg-icons';

/**
 * Configuration for frame specifications
 */

// FRAMES
export const frameKeySpecs = [
    {
        label: 'Size',
        path: 'size',
        icon: faRuler,
        unit: 'mm'
    },
    {
        label: 'Prop Size',
        path: 'prop_size',
        icon: faExpand,
        unit: '\"'
    },
    {
        label: 'Weight',
        path: 'weight',
        icon: faWeightHanging,
        unit: 'g'
    },
    {
        label: 'Material',
        path: 'material',
        icon: faCubes,
        formatter: (value) => {
            const materials = {
                'aluminum': 'Aluminium',
                'fibre': 'Carbon Fibre',
                'another': 'Other'
            };
            return materials[value] || value;
        }
    },
    {
        label: 'Configuration',
        path: 'configuration',
        icon: faBorderAll,
        formatter: (value) => {
            const configs = {
                'h': 'H Frame',
                'x': 'X Frame',
                'hybrid': 'Hybrid-X',
                'box': 'Box',
                'another': 'Other'
            };
            return configs[value] || value;
        }
    },
];

export const frameSpecs = [
    ...frameKeySpecs,

    {
        label: 'Camera Mount',
        path: 'camera_details',
        icon: faCamera,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return details.map(d => `${d.camera_mount_height}×${d.camera_mount_width}mm`).join(', ');
        }
    },
    {
        label: 'Motor Mount',
        path: 'motor_details',
        icon: faCog,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return details.map(d => `${d.motor_mount_height}×${d.motor_mount_width}mm`).join(', ');
        }
    },
    {
        label: 'VTX Mount',
        path: 'vtx_details',
        icon: faSatelliteDish,
        formatter: (details) => {
            if (!details || !details.length) return 'N/A';
            return details.map(d => `${d.vtx_mount_height}×${d.vtx_mount_width}mm`).join(', ');
        }
    }
];