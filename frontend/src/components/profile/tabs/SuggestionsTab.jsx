import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faWifi, faCamera, faMicrochip, faCalendarAlt,
  faTimesCircle, faCheckCircle, faEye, faEdit,
  faRedo, faPlus, faLightbulb
} from '@fortawesome/free-solid-svg-icons';
import LoadingSpinner from '../../common/LoadingSpinner';
import ErrorMessage from '../../common/ErrorMessage';

const SuggestionsTab = ({ profileData }) => {
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Placeholder data for demonstration
  const demoSuggestions = [
    {
      id: 1,
      component_name: 'TrueRC X-Air Antenna',
      component_type: 'antenna',
      status: 'pending',
      submitted_at: '2025-03-15T00:00:00Z',
      response_at: null,
      manufacturer: 'TrueRC',
      model: 'X-Air 5.8GHz'
    },
    {
      id: 2,
      component_name: 'Runcam Phoenix 2 Camera',
      component_type: 'camera',
      status: 'approved',
      submitted_at: '2025-03-05T00:00:00Z',
      response_at: '2025-03-08T00:00:00Z',
      manufacturer: 'Runcam',
      model: 'Phoenix 2 1000TVL'
    },
    {
      id: 3,
      component_name: 'HGLRC Zeus F722 FC',
      component_type: 'flight_controller',
      status: 'denied',
      submitted_at: '2025-02-28T00:00:00Z',
      response_at: '2025-03-03T00:00:00Z',
      manufacturer: 'HGLRC',
      model: 'Zeus F722 Mini'
    }
  ];

  useEffect(() => {
    // Simulate fetching suggestions data
    const fetchSuggestions = async () => {
      try {
        setLoading(true);
        // In real implementation, you would fetch from API
        // const response = await suggestionsApi.getUserSuggestions(profileData.id);

        // Using demo data for now
        setTimeout(() => {
          setSuggestions(demoSuggestions);
          setLoading(false);
        }, 500);
      } catch (err) {
        setError('Failed to load suggestions');
        setLoading(false);
      }
    };

    fetchSuggestions();
  }, [profileData.id]);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  };

  const getComponentIcon = (type) => {
    switch (type) {
      case 'antenna':
        return faWifi;
      case 'camera':
        return faCamera;
      case 'flight_controller':
        return faMicrochip;
      default:
        return faLightbulb;
    }
  };

  const getComponentColor = (type) => {
    switch (type) {
      case 'antenna':
        return 'antenna';
      case 'camera':
        return 'video';
      case 'flight_controller':
        return 'control';
      default:
        return 'primary';
    }
  };

  const getStatusBadgeClass = (status) => {
    switch (status) {
      case 'pending':
        return 'bg-warning-color text-yellow-900';
      case 'approved':
        return 'bg-success-color text-green-900';
      case 'denied':
        return 'bg-error-color text-white';
      default:
        return 'bg-gray-200 text-gray-800';
    }
  };

  const handleCreateSuggestion = () => {
    // This would navigate to create suggestion page
    alert('Create new suggestion functionality will be implemented in the future');
  };

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-primary">Your Suggestions</h2>
        <button
          onClick={handleCreateSuggestion}
          className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 transition-colors flex items-center gap-2"
        >
          <FontAwesomeIcon icon={faPlus} />
          Suggest Component
        </button>
      </div>

      {suggestions.length === 0 ? (
        <div className="bg-white rounded-xl p-12 text-center shadow-sm">
          <div className="text-5xl text-gray-300 mb-6">
            <FontAwesomeIcon icon={faLightbulb} />
          </div>
          <h3 className="text-xl font-semibold text-primary mb-2">No Suggestions Yet</h3>
          <p className="text-gray-500 mb-6 max-w-md mx-auto">
            Help improve our component database by suggesting new components that aren't listed yet.
          </p>
          <button
            onClick={handleCreateSuggestion}
            className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-opacity-90 transition-colors"
          >
            Suggest Your First Component
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {suggestions.map(suggestion => {
            const componentColor = getComponentColor(suggestion.component_type);
            const statusClass = getStatusBadgeClass(suggestion.status);

            return (
              <div key={suggestion.id} className="bg-white rounded-xl shadow-sm overflow-hidden p-6 transition-all hover:-translate-y-1 hover:shadow-md">
                <div className="flex justify-between items-start mb-4">
                  <h3 className="text-lg font-semibold text-primary pr-4">{suggestion.component_name}</h3>
                  <span className={`inline-block px-3 py-1 text-xs font-semibold rounded-full ${statusClass}`}>
                    {suggestion.status.charAt(0).toUpperCase() + suggestion.status.slice(1)}
                  </span>
                </div>

                <div className="space-y-2 mb-5">
                  <div className="flex items-center text-sm text-gray-500">
                    <FontAwesomeIcon icon={faCalendarAlt} className="w-4 text-center mr-3" />
                    <span>Submitted: {formatDate(suggestion.submitted_at)}</span>
                  </div>

                  {suggestion.status !== 'pending' && suggestion.response_at && (
                    <div className="flex items-center text-sm text-gray-500">
                      <FontAwesomeIcon
                        icon={suggestion.status === 'approved' ? faCheckCircle : faTimesCircle}
                        className={`w-4 text-center mr-3 ${suggestion.status === 'approved' ? 'text-success-color' : 'text-error-color'}`}
                      />
                      <span>
                        {suggestion.status === 'approved' ? 'Approved' : 'Denied'}: {formatDate(suggestion.response_at)}
                      </span>
                    </div>
                  )}
                </div>

                <div className={`flex items-center bg-gray-50 p-3 rounded-lg mb-5 border-l-4 border-${componentColor}`}>
                  <div className={`flex items-center justify-center w-10 h-10 rounded-lg bg-${componentColor} text-white mr-4`}>
                    <FontAwesomeIcon icon={getComponentIcon(suggestion.component_type)} />
                  </div>
                  <div>
                    <div className="text-xs text-gray-500 mb-1">
                      {suggestion.component_type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                    </div>
                    <div className="font-medium text-gray-800 truncate">
                      {suggestion.manufacturer} {suggestion.model}
                    </div>
                  </div>
                </div>

                <div className="flex gap-3">
                  <button className={`flex-1 py-2 px-3 bg-${componentColor} text-white rounded-md hover:bg-opacity-90 transition-colors text-sm font-medium flex items-center justify-center gap-2`}>
                    <FontAwesomeIcon icon={faEye} />
                    View Details
                  </button>

                  {suggestion.status === 'pending' && (
                    <button className={`flex-1 py-2 px-3 border border-${componentColor} text-${componentColor} rounded-md hover:bg-gray-50 transition-colors text-sm font-medium flex items-center justify-center gap-2`}>
                      <FontAwesomeIcon icon={faEdit} />
                      Edit
                    </button>
                  )}

                  {suggestion.status === 'denied' && (
                    <button className={`flex-1 py-2 px-3 border border-${componentColor} text-${componentColor} rounded-md hover:bg-gray-50 transition-colors text-sm font-medium flex items-center justify-center gap-2`}>
                      <FontAwesomeIcon icon={faRedo} />
                      Resubmit
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

SuggestionsTab.propTypes = {
  profileData: PropTypes.object.isRequired
};

export default SuggestionsTab;