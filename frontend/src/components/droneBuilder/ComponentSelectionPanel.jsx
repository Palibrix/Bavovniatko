import React, {useEffect, useState} from 'react';
import PropTypes from 'prop-types';
import {useSearchParams} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {
    faBatteryFull,
    faBorderAll,
    faBroadcastTower,
    faCamera,
    faCog,
    faFan,
    faFilter,
    faMicrochip,
    faSatelliteDish,
    faTachometerAlt,
    faWifi
} from '@fortawesome/free-solid-svg-icons';
import {getEntityThemeClass} from '../../utils/themeUtils';
import {compatibilityApi, componentsApi} from '../../services/api';
import ComponentList from './ComponentList';
import BuildOverview from './BuildOverview';
import {FilterSidebar} from '../../components/filters';


/**
 * Middle panel for component selection in drone builder
 */
const ComponentSelectionPanel = ({
    selectedCategory,
    onSelectComponent,
    showBuildOverview,
    droneComponents,
    onBuildOverviewToggle,
    compatibilityIssues = [],
    persistentCompatibilityIssues = [],
    dismissedIssues = [],
    onDismissIssue,
    onRestoreIssue,
    missingComponents = [],
    completionPercentage,
    componentCompatibility = {}
}) => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [components, setComponents] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [showOnlyCompatible, setShowOnlyCompatible] = useState(true);
    const [showFilters, setShowFilters] = useState(false);

    // Get current component mapping
    const currentMapping = selectedCategory ? COMPONENT_MAPPING[selectedCategory] : null;
    const themeClass = currentMapping ? getEntityThemeClass(currentMapping.theme) : getEntityThemeClass('primary');

    // Fetch components for the selected category
    useEffect(() => {
        if (!selectedCategory || showBuildOverview) return;

        const fetchComponents = async () => {
            setLoading(true);
            setError(null);

            try {
                // Get the API type from the mapping
                const apiType = COMPONENT_MAPPING[selectedCategory].theme;
                const apiDroneComponent = COMPONENT_MAPPING[selectedCategory].droneProperty;

                // Extract filter params from URL
                const filterParams = {};
                searchParams.forEach((value, key) => {
                    if (key !== 'page' && key !== 'sort') {
                        filterParams[key] = value;
                    }
                });

                // Prepare current component configuration for compatibility check
                const configuration = {};
                Object.entries(droneComponents).forEach(([key, component]) => {
                    if (component && typeof component === 'object' && component.id && !key.startsWith('total_') &&
                        !['model', 'manufacturer', 'description', 'type', 'images', 'documents',
                            'flight_duration', 'max_speed', 'control_range', 'max_altitude'].includes(key)) {
                        configuration[key] = component.id;
                    }
                });

                let result;

                // If we have components selected and there's a defined compatibility relationship
                if (Object.keys(configuration).length > 0) {
                    try {
                        // Get components with compatibility information and pass filter parameters
                        result = await compatibilityApi.getCompatibleComponents(
                            COMPONENT_MAPPING[selectedCategory].droneProperty,
                            configuration,
                            filterParams
                        );
                    } catch (compatError) {
                        console.warn('Compatibility check failed, falling back to regular fetch:', compatError);
                        // Fall back to regular fetch if compatibility check fails
                        result = await componentsApi.getComponentList(apiType, filterParams);
                    }
                } else {
                    // Regular fetch if no components selected yet
                    result = await componentsApi.getComponentList(apiType, filterParams);
                }

                setComponents(result.results || result);
            } catch (err) {
                console.error(`Error fetching ${selectedCategory}:`, err);
                setError(`Failed to load components. Please try again.`);
            } finally {
                setLoading(false);
            }
        };

        fetchComponents();
    }, [selectedCategory, showBuildOverview, searchParams, droneComponents]);

    // Handle filter changes
    const handleFilterChange = (newParams) => {
        setSearchParams(newParams);
    };

    // Handle component selection
    const handleComponentSelect = (component) => {
        if (!currentMapping) return;
        onSelectComponent(component, selectedCategory);
    };

    // Handle component removal
    const handleComponentRemove = (componentKey) => {
        onSelectComponent(null, null, componentKey);
    };

    return (
        <div className="flex-1 bg-white rounded-3xl shadow-sm overflow-hidden flex flex-col">
            <div
                className="py-4 px-6 border-b border-gray-100 font-semibold text-primary flex justify-between items-center">
                <span>{showBuildOverview ? 'Build Overview' : `Select ${currentMapping?.displayName || 'Component'}`}</span>
                <div className="flex items-center gap-2">
                    {!showBuildOverview && selectedCategory && (
                        <button
                            className="text-sm px-3 py-1.5 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors flex items-center gap-1.5"
                            onClick={() => setShowFilters(!showFilters)}
                        >
                            <FontAwesomeIcon icon={faFilter}/>
                            {showFilters ? 'Hide Filters' : 'Show Filters'}
                        </button>
                    )}
                    <button
                        className="text-sm px-3 py-1.5 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
                        onClick={() => onBuildOverviewToggle()}
                    >
                        {showBuildOverview ? 'Select Components' : 'Build Overview'}
                    </button>
                </div>
            </div>

            {showBuildOverview ? (
                <BuildOverview
                    droneComponents={droneComponents}
                    compatibilityIssues={compatibilityIssues}
                    persistentCompatibilityIssues={persistentCompatibilityIssues}
                    dismissedIssues={dismissedIssues}
                    onDismissIssue={onDismissIssue}
                    onRestoreIssue={onRestoreIssue}
                    missingComponents={missingComponents}
                    onComponentAdd={onBuildOverviewToggle}
                    onComponentRemove={handleComponentRemove}
                />
            ) : (
                <div className="flex flex-1 overflow-hidden">
                    {showFilters && (
                        <div className="w-64 border-r border-gray-100 p-3 overflow-y-auto">
                            <FilterSidebar
                                componentType={currentMapping?.theme || 'primary'}
                                setSearchParamsWithReplace={handleFilterChange}
                            />
                        </div>
                    )}
                    <div className="flex-1">
                        <ComponentList
                            components={components}
                            loading={loading}
                            error={error}
                            selectedCategory={selectedCategory}
                            onSelectComponent={handleComponentSelect}
                            showOnlyCompatible={showOnlyCompatible}
                            setShowOnlyCompatible={setShowOnlyCompatible}
                            gridColumns={showFilters ? 2 : 3}
                            droneComponents={droneComponents}
                            componentCompatibility={componentCompatibility}
                            dismissedIssues={dismissedIssues}
                            persistentIssues={persistentCompatibilityIssues}
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

// Component mapping
const COMPONENT_MAPPING = {
    frames: {
        displayName: 'Frame',
        icon: faBorderAll,
        theme: 'frames',
        droneProperty: 'frame'
    },
    motors: {
        displayName: 'Motors',
        icon: faCog,
        theme: 'motors',
        droneProperty: 'motor'
    },
    propellers: {
        displayName: 'Propellers',
        icon: faFan,
        theme: 'propellers',
        droneProperty: 'propeller'
    },
    batteries: {
        displayName: 'Battery',
        icon: faBatteryFull,
        theme: 'batteries',
        droneProperty: 'battery'
    },
    flight_controllers: {
        displayName: 'Flight Controller',
        icon: faMicrochip,
        theme: 'flight_controllers',
        droneProperty: 'flight_controller'
    },
    speed_controllers: {
        displayName: 'Speed Controller',
        icon: faTachometerAlt,
        theme: 'speed_controllers',
        droneProperty: 'speed_controller'
    },
    receivers: {
        displayName: 'Receiver',
        icon: faBroadcastTower,
        theme: 'receivers',
        droneProperty: 'receiver'
    },
    cameras: {
        displayName: 'Camera',
        icon: faCamera,
        theme: 'cameras',
        droneProperty: 'camera'
    },
    transmitters: {
        displayName: 'Video Transmitter',
        icon: faSatelliteDish,
        theme: 'transmitters',
        droneProperty: 'transmitter'
    },
    antennas_receiver: {
        displayName: 'Receiver Antenna',
        icon: faWifi,
        theme: 'antennas',
        droneProperty: 'antenna_receiver'
    },
    antennas_transmitter: {
        displayName: 'Transmitter Antenna',
        icon: faWifi,
        theme: 'antennas',
        droneProperty: 'antenna_transmitter'
    }
};

ComponentSelectionPanel.propTypes = {
    selectedCategory: PropTypes.string,
    onSelectComponent: PropTypes.func.isRequired,
    showBuildOverview: PropTypes.bool.isRequired,
    droneComponents: PropTypes.object.isRequired,
    onBuildOverviewToggle: PropTypes.func.isRequired,
    compatibilityIssues: PropTypes.array,
    persistentCompatibilityIssues: PropTypes.array,
    dismissedIssues: PropTypes.array,
    onDismissIssue: PropTypes.func,
    onRestoreIssue: PropTypes.func,
    missingComponents: PropTypes.array,
    completionPercentage: PropTypes.number.isRequired,
    componentCompatibility: PropTypes.object
};

export default ComponentSelectionPanel;