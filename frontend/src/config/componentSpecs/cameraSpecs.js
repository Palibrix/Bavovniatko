import {
    faArrowsAltH, faBatteryFull, faCamera,
    faPlug, faRuler, faSignal, faWeightHanging
} from "@fortawesome/free-solid-svg-icons";

export const cameraKeySpecs = [
  {
    label: 'Resolution',
    path: 'tvl',
    icon: faCamera,
    unit: 'TVL'
  },
  {
    label: 'Voltage',
    path: 'voltage',
    icon: faBatteryFull,
    formatter: (_, item) => `${item.voltage_min} - ${item.voltage_max}V`
  },
  {
    label: 'FOV',
    path: 'fov',
    icon: faArrowsAltH,
    unit: '°'
  },
  {
    label: 'Aspect Ratio',
    path: 'ratio',
    icon: faRuler
  }
];

export const cameraSpecs = [
  ...cameraKeySpecs,
  {
    label: 'Output Type',
    path: 'output_type',
    icon: faPlug,
    formatter: (value) => value === 'A' ? 'Analog' : value === 'D' ? 'Digital' : value
  },
  {
    label: 'Light Sensitivity',
    path: 'light_sens',
    icon: faSignal
  },
  {
    label: 'Weight',
    path: 'weight',
    icon: faWeightHanging,
    unit: 'g'
  }
];