import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faBorderAll, faCog, faMicrochip, faBatteryFull,
  faEye, faEdit, faPlus, faClock
} from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../../common/LoadingSpinner';
import ErrorMessage from '../../common/ErrorMessage';
import { ROUTES } from '../../../routes';

const DronesTab = ({ profileData }) => {
  const [drones, setDrones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Placeholder data for demonstration
  const demoDrones = [
    {
      id: 1,
      model: 'Racing Quad 5"',
      type: 'racing',
      completion: 70,
      missing_components: ['Camera', 'Battery'],
      frame: { manufacturer: 'TBS', model: 'Source One 5"' },
      motor: { manufacturer: 'Emax', model: 'Eco II 2306' },
      flight_controller: { manufacturer: 'Matek', model: 'F405 CTR' },
      images: [{ image: '/api/placeholder/300/200' }]
    },
    {
      id: 2,
      model: 'Photography Drone',
      type: 'photography',
      completion: 100,
      missing_components: [],
      frame: { manufacturer: 'XYZ', model: 'Frame' },
      camera: { manufacturer: 'HD', model: '4K 60fps' },
      battery: { type: '6S', capacity: 5200 },
      images: [{ image: '/api/placeholder/300/200' }]
    }
  ];

  useEffect(() => {
    // Simulate fetching drones data
    const fetchDrones = async () => {
      try {
        setLoading(true);
        // In real implementation, you would fetch from API
        // const response = await dronesApi.getUserDrones(profileData.id);

        // Using demo data for now
        setTimeout(() => {
          setDrones(demoDrones);
          setLoading(false);
        }, 500);
      } catch (err) {
        setError('Failed to load drones');
        setLoading(false);
      }
    };

    fetchDrones();
  }, [profileData.id]);

  const handleCreateDrone = () => {
    // This would navigate to create drone page
    alert('Create new drone functionality will be implemented in the future');
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-primary">Your Drones</h2>
        <button
          onClick={handleCreateDrone}
          className="px-4 py-2 bg-drone text-white rounded-lg hover:bg-opacity-90 transition-colors flex items-center gap-2"
        >
          <FontAwesomeIcon icon={faPlus} />
          Create New Drone
        </button>
      </div>

      {drones.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center shadow-sm">
          <div className="text-5xl text-gray-300 mb-6">
            <FontAwesomeIcon icon={faClock} />
          </div>
          <h3 className="text-xl font-semibold text-primary mb-2">No Drones Yet</h3>
          <p className="text-gray-500 mb-6 max-w-md mx-auto">
            Create your first drone build to keep track of components and visualize your setup.
          </p>
          <button
            onClick={handleCreateDrone}
            className="px-4 py-2 bg-drone text-white rounded-lg hover:bg-opacity-90 transition-colors"
          >
            Build Your First Drone
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {drones.map(drone => (
            <div key={drone.id} className="bg-white rounded-xl shadow-sm overflow-hidden border-t-4 border-t-drone transition-all hover:-translate-y-1 hover:shadow-md flex flex-col h-full">
              <div className="h-40 bg-gray-100 flex items-center justify-center overflow-hidden">
                <img
                  src={drone.images[0]?.image || '/api/placeholder/300/200'}
                  alt={drone.model}
                  className="max-w-full max-h-36 object-contain"
                />
              </div>
              <div className="p-5 flex-grow flex flex-col">
                <div className="mb-4">
                  <span className="inline-block px-3 py-1 text-xs font-semibold text-white bg-drone rounded-full mb-2">
                    {drone.type.charAt(0).toUpperCase() + drone.type.slice(1)}
                  </span>
                  <h3 className="text-lg font-semibold text-primary">{drone.model}</h3>
                </div>

                <div className="h-1.5 bg-gray-200 rounded-md overflow-hidden mb-1">
                  <div
                    className="h-full bg-drone rounded-md"
                    style={{ width: `${drone.completion}%` }}
                  ></div>
                </div>
                <div className="text-sm text-gray-500 mb-4">
                  Completion: {drone.completion}%
                  {drone.missing_components.length > 0 && (
                    <span>`(Needs: ${drone.missing_components.join(', ')})`</span>
                  )}
                </div>

                <div className="space-y-2 mb-5">
                  {drone.frame && (
                    <div className="flex items-center text-sm text-gray-600">
                      <FontAwesomeIcon icon={faBorderAll} className="w-4 text-center mr-3 text-drone" />
                      <span>Frame: {drone.frame.manufacturer} {drone.frame.model}</span>
                    </div>
                  )}
                  {drone.motor && (
                    <div className="flex items-center text-sm text-gray-600">
                      <FontAwesomeIcon icon={faCog} className="w-4 text-center mr-3 text-drone" />
                      <span>Motor: {drone.motor.manufacturer} {drone.motor.model}</span>
                    </div>
                  )}
                  {drone.flight_controller && (
                    <div className="flex items-center text-sm text-gray-600">
                      <FontAwesomeIcon icon={faMicrochip} className="w-4 text-center mr-3 text-drone" />
                      <span>FC: {drone.flight_controller.manufacturer} {drone.flight_controller.model}</span>
                    </div>
                  )}
                  {drone.battery && (
                    <div className="flex items-center text-sm text-gray-600">
                      <FontAwesomeIcon icon={faBatteryFull} className="w-4 text-center mr-3 text-drone" />
                      <span>Battery: {drone.battery.type} {drone.battery.capacity}mAh</span>
                    </div>
                  )}
                </div>

                <div className="flex gap-3 mt-auto">
                  <Link
                    to={`${ROUTES.BUILDS.DRONES.DETAIL.replace(':id', drone.id)}`}
                    className="flex-1 py-2 px-3 bg-drone text-white rounded-md hover:bg-drone-dark transition-colors text-sm font-medium flex items-center justify-center gap-2"
                  >
                    <FontAwesomeIcon icon={faEye} />
                    View
                  </Link>
                  <button className="flex-1 py-2 px-3 border border-drone text-drone rounded-md hover:bg-gray-50 transition-colors text-sm font-medium flex items-center justify-center gap-2">
                    <FontAwesomeIcon icon={faEdit} />
                    Edit
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

DronesTab.propTypes = {
  profileData: PropTypes.object.isRequired
};

export default DronesTab;