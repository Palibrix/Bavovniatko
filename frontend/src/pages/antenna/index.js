import React from 'react';
import { Link } from 'react-router-dom';
import { componentsApi } from '../../services/api';
import { createComponentPages } from '../../utils/componentFactory';
import { getDetailRoute } from '../../routes';

// Render function for antenna-specific details
const renderAntennaDetails = (antenna) => (
  <div className="space-y-4">
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h3 className="text-lg font-medium text-gray-800 mb-2">General Specifications</h3>
        <dl className="space-y-2">
          <div>
            <dt className="text-sm font-medium text-gray-500">Center Frequency</dt>
            <dd className="mt-1">{antenna.center_frequency} MHz</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-gray-500">Bandwidth</dt>
            <dd className="mt-1">{antenna.bandwidth_min} - {antenna.bandwidth_max} MHz</dd>
          </div>
          {antenna.swr && (
            <div>
              <dt className="text-sm font-medium text-gray-500">SWR</dt>
              <dd className="mt-1">{antenna.swr}</dd>
            </div>
          )}
          {antenna.gain && (
            <div>
              <dt className="text-sm font-medium text-gray-500">Gain</dt>
              <dd className="mt-1">{antenna.gain} dBi</dd>
            </div>
          )}
          {antenna.radiation && (
            <div>
              <dt className="text-sm font-medium text-gray-500">Radiation Efficiency</dt>
              <dd className="mt-1">{antenna.radiation}%</dd>
            </div>
          )}
        </dl>
      </div>

      <div>
        <h3 className="text-lg font-medium text-gray-800 mb-2">Antenna Type</h3>
        {antenna.type && (
          <dl className="space-y-2">
            <div>
              <dt className="text-sm font-medium text-gray-500">Type</dt>
              <dd className="mt-1">{antenna.type.type}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Direction</dt>
              <dd className="mt-1">{antenna.type.direction}</dd>
            </div>
            <div>
              <dt className="text-sm font-medium text-gray-500">Polarization</dt>
              <dd className="mt-1">{antenna.type.polarization}</dd>
            </div>
          </dl>
        )}
      </div>
    </div>

    <div>
      <h3 className="text-lg font-medium text-gray-800 mb-2">Details</h3>
      {antenna.details && antenna.details.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Connector</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Weight</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Angle Type</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {antenna.details.map((detail, index) => (
                <tr key={index}>
                  <td className="px-6 py-4 whitespace-nowrap">{detail.connector_type.type}</td>
                  <td className="px-6 py-4 whitespace-nowrap">{detail.weight}g</td>
                  <td className="px-6 py-4 whitespace-nowrap">{detail.angle_type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <p className="text-gray-500">No detailed specifications available</p>
      )}
    </div>
  </div>
);

// Custom render function for antenna list items
const renderAntennaListItem = (antenna) => (
  <li key={antenna.id} className="py-3 px-4 hover:bg-gray-100 flex items-center justify-between">
    <div>
      <Link
        to={getDetailRoute('antennas', antenna.id)}
        className="text-primary hover:text-primary-dark font-medium"
      >
        <span>{antenna.manufacturer} {antenna.model}</span>
      </Link>
      {antenna.type && (
        <span className="text-sm text-gray-500 ml-2">
          {antenna.type.type}, {antenna.center_frequency} MHz
        </span>
      )}
    </div>
    <span className="text-sm bg-antenna-light text-antenna-dark px-2 py-1 rounded-full">
      Antenna
    </span>
  </li>
);

// Create antenna list and detail page components using the improved component factory
const { ListPage, DetailPage } = createComponentPages({
  type: 'antennas',
  title: 'Antennas',
  fetchList: componentsApi.getAntennas,
  fetchDetail: componentsApi.getAntennaById,
  renderListItem: renderAntennaListItem,
  renderDetailContent: renderAntennaDetails
});

export const AntennaListPage = ListPage;
export const AntennaDetailPage = DetailPage;