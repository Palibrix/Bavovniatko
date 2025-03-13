import { componentsApi } from '../../services/api';
import { createComponentListPage, createComponentDetailPage } from '../../utils/componentFactory';
import { Link } from 'react-router-dom';
import { getDetailRoute } from '../../routes';

// Render function for antenna-specific details
const renderAntennaDetails = (antenna) => (
  <div className="antenna-specific-details">
    <p><strong>Center Frequency:</strong> {antenna.center_frequency} MHz</p>
    <p><strong>Bandwidth:</strong> {antenna.bandwidth_min} - {antenna.bandwidth_max} MHz</p>
    {antenna.swr && <p><strong>SWR:</strong> {antenna.swr}</p>}
    {antenna.gain && <p><strong>Gain:</strong> {antenna.gain} dBi</p>}
    {antenna.radiation && <p><strong>Radiation Efficiency:</strong> {antenna.radiation}%</p>}

    <h3>Type</h3>
    {antenna.type && (
      <p>
        {antenna.type.type}, {antenna.type.direction}, {antenna.type.polarization}
      </p>
    )}

    <h3>Details</h3>
    {antenna.details && antenna.details.length > 0 ? (
      <ul>
        {antenna.details.map((detail, index) => (
          <li key={index}>
            Connector: {detail.connector_type.type},
            Weight: {detail.weight}g,
            Angle: {detail.angle_type}
          </li>
        ))}
      </ul>
    ) : (
      <p>No detailed specifications available</p>
    )}
  </div>
);

// Custom render function for antenna list items
const renderAntennaListItem = (antenna) => (
  <li key={antenna.id} className="antenna-list-item">
    <Link to={getDetailRoute('antennas', antenna.id)}>
      <strong>{antenna.manufacturer} {antenna.model}</strong>
      {antenna.type && <span> - {antenna.type.type}</span>}
      {antenna.center_frequency && <span> ({antenna.center_frequency} MHz)</span>}
    </Link>
  </li>
);

// Create antenna list and detail page components
export const AntennaListPage = createComponentListPage(
  'antennas',
  'Antennas',
  componentsApi.getAntennas,
  renderAntennaListItem
);

export const AntennaDetailPage = createComponentDetailPage(
  'antennas',
  componentsApi.getAntennaById,
  renderAntennaDetails
);