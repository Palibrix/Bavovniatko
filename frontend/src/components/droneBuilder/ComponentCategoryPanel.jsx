import React from 'react';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {
    faBatteryFull,
    faBorderAll,
    faBroadcastTower,
    faCamera,
    faCog,
    faFan,
    faMicrochip,
    faSatelliteDish,
    faTachometerAlt,
    faWifi
} from '@fortawesome/free-solid-svg-icons';
import {getEntityThemeClass} from '../../utils/themeUtils';

/**
 * Left panel with component categories for drone builder
 */
const ComponentCategoryPanel = ({
                                    selectedCategory,
                                    onSelectCategory,
                                    droneComponents,
                                    completionPercentage
                                }) => {
    // Configuration for component categories
    const categories = [
        {
            title: 'Propulsion',
            items: [
                {
                    id: 'motors',
                    label: 'Motors',
                    icon: faCog,
                    theme: 'propulsion',
                    selected: droneComponents.motor !== null
                },
                {
                    id: 'propellers',
                    label: 'Propellers',
                    icon: faFan,
                    theme: 'propulsion',
                    selected: droneComponents.propeller !== null
                },
                {
                    id: 'batteries',
                    label: 'Battery',
                    icon: faBatteryFull,
                    theme: 'propulsion',
                    selected: droneComponents.battery !== null
                }
            ]
        },
        {
            title: 'Control Systems',
            items: [
                {
                    id: 'flight_controllers',
                    label: 'Flight Controller',
                    icon: faMicrochip,
                    theme: 'control',
                    selected: droneComponents.flight_controller !== null
                },
                {
                    id: 'speed_controllers',
                    label: 'Speed Controller',
                    icon: faTachometerAlt,
                    theme: 'control',
                    selected: droneComponents.speed_controller !== null
                },
                {
                    id: 'receivers',
                    label: 'Receiver',
                    icon: faBroadcastTower,
                    theme: 'control',
                    selected: droneComponents.receiver !== null
                }
            ]
        },
        {
            title: 'Structure & Communications',
            items: [
                {
                    id: 'frames',
                    label: 'Frame',
                    icon: faBorderAll,
                    theme: 'frames',
                    selected: droneComponents.frame !== null
                },
                {
                    id: 'cameras',
                    label: 'Camera',
                    icon: faCamera,
                    theme: 'video',
                    selected: droneComponents.camera !== null
                },
                {
                    id: 'transmitters',
                    label: 'Video Transmitter',
                    icon: faSatelliteDish,
                    theme: 'video',
                    selected: droneComponents.transmitter !== null
                },
                {
                    id: 'antennas_receiver',
                    label: 'Receiver Antenna',
                    icon: faWifi,
                    theme: 'antennas',
                    selected: droneComponents.antenna_receiver !== null
                },
                {
                    id: 'antennas_transmitter',
                    label: 'Transmitter Antenna',
                    icon: faWifi,
                    theme: 'antennas',
                    selected: droneComponents.antenna_transmitter !== null
                }
            ]
        }
    ];

    // Calculate total weight of the drone
    const getTotalWeight = () => {
        let totalWeight = 0;

        // Add weight of each component if available
        Object.entries(droneComponents).forEach(([key, component]) => {
            if (component && component.weight) {
                totalWeight += component.weight;
            } else if (component && key === 'frame' && component.weight) {
                totalWeight += component.weight;
            } else if (component && key === 'motor' && component.details && component.details.length > 0) {
                // Motor weight is in details
                totalWeight += component.details[0].weight || 0;
            }
        });

        return totalWeight;
    };

    return (
        <div className="w-full bg-white rounded-3xl shadow-sm overflow-hidden">
            <div
                className="py-4 px-6 border-b border-gray-100 font-semibold text-primary flex justify-between items-center">
                <span>Components</span>
                <span className="bg-drone text-white text-xs font-bold py-1 px-3 rounded-full">
          {completionPercentage}%
        </span>
            </div>

            <div className="component-categories">
                {categories.map(category => (
                    <div key={category.title} className="category-group p-4">
                        <div className="group-title text-xs text-gray-500 uppercase mb-2 font-semibold">
                            {category.title}
                        </div>

                        {category.items.map(item => {
                            const themeClass = getEntityThemeClass(item.theme);

                            return (
                                <div
                                    key={item.id}
                                    className={`category-item flex items-center p-3 rounded-lg mb-2 cursor-pointer transition-all ${
                                        selectedCategory === item.id ? 'bg-gray-100' : 'hover:bg-gray-50'
                                    }`}
                                    onClick={() => onSelectCategory(item.id)}
                                >
                                    <div
                                        className={`category-icon w-8 h-8 rounded-full flex items-center justify-center mr-3 text-white ${themeClass.bg}`}>
                                        <FontAwesomeIcon icon={item.icon}/>
                                    </div>
                                    <div className="category-label flex-1">{item.label}</div>
                                    <div
                                        className={`category-status w-5 h-5 rounded-full flex items-center justify-center text-xs ${
                                            item.selected
                                                ? 'bg-green-600 text-white'
                                                : 'border-2 border-red-500 text-red-500'
                                        }`}>
                                        {item.selected ? '✓' : '+'}
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                ))}
            </div>

            {/* Weight calculation */}
            <div className="weight-calculator p-4 border-t border-gray-100">
                <div className="weight-title text-sm font-semibold mb-2">Weight Calculation</div>

                {Object.entries(droneComponents).map(([key, component]) => {
                    if (!component) return null;

                    let weight = 0;
                    let label = '';

                    // Extract weight based on component type
                    if (key === 'frame') {
                        weight = component.weight || 0;
                        label = 'Frame';
                    } else if (key === 'motor' && component.details && component.details.length > 0) {
                        weight = component.details[0].weight || 0;
                        label = 'Motor';
                    } else if (key === 'battery') {
                        weight = component.weight || 0;
                        label = 'Battery';
                    } else if (component.weight) {
                        weight = component.weight;

                        // Generate label from key
                        label = key.charAt(0).toUpperCase() + key.slice(1).replace('_', ' ');
                        if (key === 'antenna_receiver') label = 'Receiver Antenna';
                        if (key === 'antenna_transmitter') label = 'Transmitter Antenna';
                        if (key === 'flight_controller') label = 'Flight Controller';
                        if (key === 'speed_controller') label = 'Speed Controller';
                    }

                    if (weight > 0) {
                        return (
                            <div key={key} className="weight-row flex justify-between text-sm mb-1">
                                <span>{label}</span>
                                <span>{weight}g</span>
                            </div>
                        );
                    }

                    return null;
                })}

                <div
                    className="weight-row weight-total flex justify-between font-semibold border-t border-gray-100 mt-2 pt-2">
                    <span>Total Weight</span>
                    <span>{getTotalWeight()}g</span>
                </div>
            </div>
        </div>
    );
};

ComponentCategoryPanel.propTypes = {
    selectedCategory: PropTypes.string,
    onSelectCategory: PropTypes.func.isRequired,
    droneComponents: PropTypes.object.isRequired,
    completionPercentage: PropTypes.number.isRequired
};

export default ComponentCategoryPanel;