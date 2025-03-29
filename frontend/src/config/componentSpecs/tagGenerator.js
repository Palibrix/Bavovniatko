export const generateComponentTags = (componentType, item) => {
  if (!item) return [];

  switch(componentType) {
    case 'antennas':
      const antennaTags = [];

      // Add type and polarization
      if (item.type) {
        if (item.type.type) antennaTags.push(item.type.type);
        if (item.type.polarization) {
          const polarization = {
            'linear': 'LP',
            'left_circular': 'LHCP',
            'right_circular': 'RHCP'
          }[item.type.polarization] || item.type.polarization;
          antennaTags.push(polarization);
        }
      }

      // Add frequency range
      if (item.center_frequency) {
        antennaTags.push(`${item.center_frequency}MHz`);
      }

      // Add connector types from details
      if (item.details && item.details.length > 0) {
        item.details.forEach(detail => {
          if (detail.connector_type && detail.connector_type.type) {
            antennaTags.push(detail.connector_type.type);
          }
          if (detail.angle_type) {
            antennaTags.push(detail.angle_type);
          }
        });
      }

      return antennaTags;

    case 'cameras':
      return [
        item.output_type === 'A' ? 'Analog' : 'Digital',
        item.ratio,
        `${item.tvl}TVL`,
        item.fov ? `${item.fov}° FOV` : null
      ].filter(Boolean);

    case 'frames':
      return [
        item.material === 'fibre' ? 'Carbon Fiber' :
        item.material === 'aluminum' ? 'Aluminum' : item.material,
        item.configuration === 'h' ? 'H Frame' :
        item.configuration === 'x' ? 'X Frame' :
        item.configuration === 'hybrid' ? 'Hybrid-X' :
        item.configuration === 'box' ? 'Box' : item.configuration,
        item.prop_size,
        item.size ? `${item.size}mm` : null
      ].filter(Boolean);

    case 'motors':
      const motorTags = [
        `${item.stator_diameter}${item.stator_height}`,
        item.configuration
      ];

      if (item.details && item.details.length > 0) {
        const detail = item.details[0];
        motorTags.push(`${detail.kv_per_volt}KV`);

        if (detail.voltage) {
          motorTags.push(`${detail.voltage.max_cells}S`);
        }
      }

      return motorTags.filter(Boolean);

    case 'propellers':
      return [
        `${item.size}×${item.pitch}`,
        item.blade_count === '2' ? '2-blade' :
        item.blade_count === '3' ? '3-blade' :
        item.blade_count === '4' ? '4-blade' :
        item.blade_count === '5' ? '5-blade' : item.blade_count
      ].filter(Boolean);

    case 'receivers':
      const rxTags = [];

      if (item.protocols && item.protocols.length > 0) {
        // Get up to 2 protocols
        item.protocols.slice(0, 2).forEach(protocol => {
          rxTags.push(protocol.type);
        });
      }

      if (item.details && item.details.length > 0) {
        rxTags.push(`${item.details[0].frequency}MHz`);
      }

      if (item.voltage_min) {
        rxTags.push(`${item.voltage_min}${item.voltage_max ? '-' + item.voltage_max : ''}V`);
      }

      return rxTags;

    case 'flight_controllers':
      return [
        item.microcontroller,
        item.gyro ? item.gyro.imu : null,
        item.connector_type === 'micro' ? 'Micro-USB' :
        item.connector_type === 'c' ? 'USB-C' : item.connector_type,
        item.voltage ? `${item.voltage.max_cells}S` : null
      ].filter(Boolean);

    case 'speed_controllers':
      return [
        item.esc_type === 'all' ? '4-in-1' : 'Single',
        `${item.cont_current}A/${item.burst_current}A`,
        item.voltage ? `${item.voltage.max_cells}S` : null,
        item.protocols && item.protocols.length > 0 ? item.protocols[0].protocol : null
      ].filter(Boolean);

    case 'transmitters':
      return [
        item.output === 'A' ? 'Analog' : 'Digital',
        `${item.max_power}mW`,
        `${item.channels_quantity}ch`,
        item.microphone ? 'Mic' : null
      ].filter(Boolean);

    default:
      return [];
  }
};

export default generateComponentTags;