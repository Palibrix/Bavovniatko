import React, {useEffect, useState} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faArrowLeft, faExclamationTriangle, faSave, faSpinner, faTrash} from '@fortawesome/free-solid-svg-icons';
import {ROUTES} from '../../routes';
import {compatibilityApi, componentsApi, dronesApi} from '../../services/api';
import ComponentCategoryPanel from '../droneBuilder/ComponentCategoryPanel';
import ComponentSelectionPanel from '../droneBuilder/ComponentSelectionPanel';
import DronePropertiesPanel from '../droneBuilder/DronePropertiesPanel';
import BatteryConfigModal from '../droneBuilder/BatteryConfigModal';
import BuildCompletionMeter from '../detail/BuildCompletionMeter';
import ConfirmationModal from '../common/ConfirmationModal';
import {getEntityThemeClass} from '../../utils/themeUtils';

/**
 * Template for creating a new drone
 */
const DroneCreateTemplate = ({isEditMode = false, initialDrone = null}) => {
    const navigate = useNavigate();
    const themeClass = getEntityThemeClass('drone');

    // State for battery saving
    const [batteryData, setBatteryData] = useState(null);
    const [batteryModalOpen, setBatteryModalOpen] = useState(false);
    const [isSavingBattery, setIsSavingBattery] = useState(false);
    const [batterySaveError, setBatterySaveError] = useState(null);

    // State for the drone being built
    const [droneData, setDroneData] = useState({
        model: isEditMode && initialDrone ? initialDrone.model : 'New Racing Drone',
        manufacturer: isEditMode && initialDrone ? initialDrone.manufacturer : '',
        description: isEditMode && initialDrone ? initialDrone.description : '',
        type: isEditMode && initialDrone ? initialDrone.type : 'photography',
        images: isEditMode && initialDrone && initialDrone.images ? initialDrone.images : [],
        documents: isEditMode && initialDrone && initialDrone.documents ? initialDrone.documents : [],
        // Properties
        total_weight: isEditMode && initialDrone ? initialDrone.total_weight : '',
        flight_duration: isEditMode && initialDrone ? initialDrone.flight_duration : '',
        max_speed: isEditMode && initialDrone ? initialDrone.max_speed : '',
        control_range: isEditMode && initialDrone ? initialDrone.control_range : '',
        max_altitude: isEditMode && initialDrone ? initialDrone.max_altitude : '',
        // Components
        frame: isEditMode && initialDrone ? initialDrone.frame : null,
        motor: isEditMode && initialDrone ? initialDrone.motor : null,
        propeller: isEditMode && initialDrone ? initialDrone.propeller : null,
        battery: isEditMode && initialDrone ? initialDrone.battery : null,
        flight_controller: isEditMode && initialDrone ? initialDrone.flight_controller : null,
        speed_controller: isEditMode && initialDrone ? initialDrone.speed_controller : null,
        receiver: isEditMode && initialDrone ? initialDrone.receiver : null,
        camera: isEditMode && initialDrone ? initialDrone.camera : null,
        transmitter: isEditMode && initialDrone ? initialDrone.transmitter : null,
        antenna_receiver: isEditMode && initialDrone ? initialDrone.antenna_receiver : null,
        antenna_transmitter: isEditMode && initialDrone ? initialDrone.antenna_transmitter : null
    });

    // UI state
    const [selectedCategory, setSelectedCategory] = useState(null);
    const [showBuildOverview, setShowBuildOverview] = useState(true);
    const [selectedComponent, setSelectedComponent] = useState(null);
    const [selectedComponentType, setSelectedComponentType] = useState(null);
    const [isSaving, setIsSaving] = useState(false);
    const [isDeleting, setIsDeleting] = useState(false);
    const [saveError, setSaveError] = useState(null);
    const [showDeleteConfirmation, setShowDeleteConfirmation] = useState(false);

    // Compatibility state (placeholders for now)
    const [componentCompatibility, setComponentCompatibility] = useState({});
    const [compatibilityIssues, setCompatibilityIssues] = useState([]);
    const [compatibilityResults, setCompatibilityResults] = useState(null);
    const [previousConfiguration, setPreviousConfiguration] = useState(null);
    const [isCheckingCompatibility, setIsCheckingCompatibility] = useState(false);

    const [persistentCompatibilityIssues, setPersistentCompatibilityIssues] = useState([]);
    const [dismissedIssues, setDismissedIssues] = useState([]);

    // Handle drone delete
    const handleDeleteDrone = async () => {
        if (!isEditMode || !initialDrone) return;

        setIsDeleting(true);
        setSaveError(null);

        try {
            await dronesApi.deleteDrone(initialDrone.id);
            navigate(ROUTES.BUILDS.DRONES.LIST);
        } catch (error) {
            console.error('Error deleting drone:', error);
            setSaveError(`Failed to delete drone: ${error.message || 'Unknown error'}`);
            setIsDeleting(false);
        }
    };

    // Check compatibility when components change
    const handleRestoreIssue = (issueId) => {
        // Remove from dismissed issues
        setDismissedIssues(prev => prev.filter(id => id !== issueId));
    };

// Update the compatibility checking function to handle recommendations
    const checkCompatibility = async () => {
        // Don't check if we have less than 2 components
        const selectedComponents = Object.entries(droneData)
            .filter(([key, value]) => !['model', 'manufacturer', 'description', 'type', 'images',
                'documents', 'total_weight', 'flight_duration', 'max_speed',
                'control_range', 'max_altitude'].includes(key) && value);

        if (selectedComponents.length < 2) {
            setCompatibilityIssues([]);
            setComponentCompatibility({});
            return;
        }

        setIsCheckingCompatibility(true);

        try {
            // Prepare configuration object with component IDs
            const configuration = {};
            selectedComponents.forEach(([key, component]) => {
                configuration[key] = component.id;
            });

            // Check compatibility with backend
            const results = await compatibilityApi.checkCompatibility(
                configuration,
                previousConfiguration,
                compatibilityResults
            );

            setCompatibilityResults(results);
            setPreviousConfiguration(configuration);

            // Extract issues, ensuring recommendations don't count as incompatibilities
            if (results.issues) {
                // For current display purposes
                setCompatibilityIssues(results.issues);

                // Process issues for persistence, adding IDs to recommendations for consistency
                setPersistentCompatibilityIssues(prevIssues => {
                    // Create a new array with existing issues
                    const updatedIssues = [...prevIssues];

                    // Add new issues if they don't already exist
                    results.issues.forEach(newIssue => {
                        // Create a unique key based on issue properties
                        const issueKey = `${newIssue.type}-${newIssue.message}-${(newIssue.component_refs || []).join('-')}`;

                        // Check if this issue already exists
                        const exists = updatedIssues.some(existingIssue => {
                            const existingKey = `${existingIssue.type}-${existingIssue.message}-${(existingIssue.component_refs || []).join('-')}`;
                            return existingKey === issueKey;
                        });

                        // If it doesn't exist, add it with a unique ID
                        if (!exists) {
                            updatedIssues.push({
                                ...newIssue,
                                // Add severity as 'recommendation' if not specified
                                severity: newIssue.severity || 'recommendation',
                                id: `issue-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
                            });
                        }
                    });

                    return updatedIssues;
                });
            }

            // Modify the component compatibility to not count recommendations as incompatibilities
            if (results.pair_results) {
                // Create a modified version that doesn't count recommendations as incompatibilities
                const modifiedPairResults = {};

                Object.entries(results.pair_results).forEach(([key, result]) => {
                    // Check if any issues are non-recommendations
                    const hasCriticalIssues = result.issues.some(issue =>
                        issue.severity !== 'recommendation' && issue.severity !== undefined);

                    // Only count as incompatible if there are critical issues
                    modifiedPairResults[key] = {
                        ...result,
                        is_compatible: !hasCriticalIssues
                    };
                });

                setComponentCompatibility(modifiedPairResults);
            }
        } catch (error) {
            console.error('Error checking compatibility:', error);
        } finally {
            setIsCheckingCompatibility(false);
        }
    };

    const handleDismissIssue = (issueId) => {
        // Add to dismissed issues
        setDismissedIssues(prev => [...prev, issueId]);
    };

    // Check compatibility when components change
    useEffect(() => {
        // Skip during initial render or when saving/deleting
        if (isSaving || isDeleting) return;

        const debouncedCheck = setTimeout(() => {
            checkCompatibility();
        }, 500);

        return () => clearTimeout(debouncedCheck);
    }, [
        droneData.frame,
        droneData.motor,
        droneData.propeller,
        droneData.flight_controller,
        droneData.speed_controller,
        droneData.receiver,
        droneData.transmitter,
        droneData.antenna_receiver,
        droneData.antenna_transmitter,
        droneData.camera,
        droneData.battery
    ]);

    // Get completion percentage and missing components
    const getCompletionData = () => {
        const requiredComponents = [
            'frame', 'motor', 'propeller', 'flight_controller',
            'speed_controller', 'receiver', 'transmitter',
            'antenna_receiver', 'antenna_transmitter', 'camera', 'battery'
        ];

        const presentComponents = requiredComponents.filter(comp => droneData[comp]);
        const completionPercentage = Math.round((presentComponents.length / requiredComponents.length) * 100);
        const missingComponents = requiredComponents.filter(comp => !droneData[comp]);

        return {completionPercentage, missingComponents};
    };

    const {completionPercentage, missingComponents} = getCompletionData();

    // Handle category selection
    const handleSelectCategory = (categoryId) => {
        if (categoryId === 'batteries') {
            // For batteries, open the battery configuration modal
            setBatteryModalOpen(true);
            return;
        }

        setSelectedCategory(categoryId);
        setSelectedComponent(null);
        setSelectedComponentType(null);
        setShowBuildOverview(false);
    };

    // Handle build overview toggle
    const handleBuildOverviewToggle = (componentType = null) => {
        if (componentType) {
            // If a component type is specified, select that category
            handleSelectCategory(componentType);
        } else {
            // Otherwise toggle between build overview and component selection
            setShowBuildOverview(!showBuildOverview);
        }
    };

    // Handle component selection
    const handleSelectComponent = async (component, category, componentKeyToRemove = null) => {
    // If componentKeyToRemove is provided, remove the component
    if (componentKeyToRemove) {
        // Special case for battery - we need to delete it completely
        if (componentKeyToRemove === 'battery' && droneData.battery?.id) {
            try {
                // Delete the battery from the API
                await componentsApi.deleteBattery(droneData.battery.id);
                console.log(`Battery ${droneData.battery.id} deleted`);
            } catch (error) {
                console.error('Error deleting battery:', error);
                // setSaveErrors(`Failed to delete battery: ${error.message || 'Unknown error'}`);
                return;
            }
        }

        // Clean up any associated compatibility issues when removing a component
        setPersistentCompatibilityIssues(prevIssues => {
            // Filter out issues that reference this component type
            return prevIssues.filter(issue => {
                // If issue has component_refs, check if it includes the removed component
                if (issue.component_refs && issue.component_refs.includes(componentKeyToRemove)) {
                    return false; // Remove this issue
                }
                return true; // Keep all other issues
            });
        });

        // Update the drone data
        setDroneData({
            ...droneData,
            [componentKeyToRemove]: null
        });
        return;
    }

    // Otherwise, map category ID to droneData property and add component
    const categoryMap = {
        frames: 'frame',
        motors: 'motor',
        propellers: 'propeller',
        flight_controllers: 'flight_controller',
        speed_controllers: 'speed_controller',
        receivers: 'receiver',
        cameras: 'camera',
        transmitters: 'transmitter',
        antennas_receiver: 'antenna_receiver',
        antennas_transmitter: 'antenna_transmitter'
    };

    const propertyName = categoryMap[category];

    if (propertyName) {
        // Update drone data with selected component
        setDroneData({
            ...droneData,
            [propertyName]: component
        });

        // Show build overview after component selection
        setShowBuildOverview(true);
    }
};

    // Handle battery save from modal
    const handleSaveBattery = async (batteryData) => {
        setIsSavingBattery(true);
        setBatterySaveError(null);

        try {
            // First create the battery
            const createdBattery = await componentsApi.createBattery(batteryData);

            // Update drone data with battery ID (not the full object)
            setDroneData({
                ...droneData,
                battery: createdBattery
            });

            // Close modal and show build overview
            setBatteryModalOpen(false);
            setShowBuildOverview(true);
        } catch (error) {
            console.error('Error saving battery:', error);
            setBatterySaveError(error.message || 'Error saving battery');
        } finally {
            setIsSavingBattery(false);
        }
    };

    // Handle image add/remove
    const handleImageAdd = (imageData) => {
        setDroneData({
            ...droneData,
            images: [...droneData.images, {image: imageData}]
        });
    };

    const handleImageRemove = (index) => {
        setDroneData({
            ...droneData,
            images: droneData.images.filter((_, i) => i !== index)
        });
    };

    // Handle drone data change
    const handleDroneDataChange = (newData) => {
        setDroneData(newData);
    };

    // Handle drone save
    const handleSaveDrone = async () => {
        // Validate required fields
        if (!droneData.model) {
            setSaveError('Drone name is required');
            return;
        }

        setIsSaving(true);
        setSaveError(null);

        try {
            // Prepare data for API
            const dronePayload = {
                model: droneData.model,
                manufacturer: droneData.manufacturer,
                description: droneData.description,
                type: droneData.type,
                // Include the component IDs for each component
                frame: droneData.frame?.id || null,
                motor: droneData.motor?.id || null,
                propeller: droneData.propeller?.id || null,
                flight_controller: droneData.flight_controller?.id || null,
                speed_controller: droneData.speed_controller?.id || null,
                receiver: droneData.receiver?.id || null,
                camera: droneData.camera?.id || null,
                transmitter: droneData.transmitter?.id || null,
                antenna_receiver: droneData.antenna_receiver?.id || null,
                antenna_transmitter: droneData.antenna_transmitter?.id || null,
                // Include battery ID if saved
                battery: droneData.battery?.id || null,
                // Include properties if provided
                ...(droneData.total_weight ? {total_weight: Number(droneData.total_weight)} : {}),
                ...(droneData.flight_duration ? {flight_duration: Number(droneData.flight_duration)} : {}),
                ...(droneData.max_speed ? {max_speed: Number(droneData.max_speed)} : {}),
                ...(droneData.control_range ? {control_range: Number(droneData.control_range)} : {}),
                ...(droneData.max_altitude ? {max_altitude: Number(droneData.max_altitude)} : {}),
                // Include images if present

                // ...(droneData.images.length > 0 ? { images: droneData.images } : {})
            };

            if (droneData.images && droneData.images.length > 0) {
                dronePayload.images = droneData.images.map(image => {
                    // If image has an ID, it's an existing image - just send the ID
                    if (typeof image === 'object' && image.id) {
                        return {id: image.id};
                    }
                    // If image is an object with image property (new base64 image)
                    else if (typeof image === 'object' && image.image) {
                        return {image: image.image};
                    }
                    // If image is directly a string (base64)
                    else if (typeof image === 'string') {
                        return {image};
                    }
                    // Return as is (fallback)
                    return image;
                });
            } else {
                dronePayload.images = []
            }

            let result;

            if (isEditMode && initialDrone) {
                // Update existing drone
                result = await dronesApi.updateDrone(initialDrone.id, dronePayload);
                console.log('Drone updated:', result);
            } else {
                // Create new drone
                result = await dronesApi.createDrone(dronePayload);
                console.log('Drone created:', result);
            }

            // Navigate to the drone detail page
            navigate(`${ROUTES.BUILDS.DRONES.LIST}/${result.id || initialDrone.id}`);
        } catch (error) {
            console.error('Error saving drone:', error);
            setSaveError(`Failed to ${isEditMode ? 'update' : 'save'} drone: ${error.message || 'Unknown error'}`);
        } finally {
            setIsSaving(false);
        }
    };

    return (
        <div className="w-[92%] max-w-[1400px] mx-auto px-4 py-8">
            {/* Back button */}
            <Link
                to={isEditMode ? `/drones/${initialDrone.id}` : ROUTES.BUILDS.DRONES.LIST}
                className="inline-flex items-center text-primary hover:text-gray-600 mb-6"
            >
                <FontAwesomeIcon icon={faArrowLeft} className="mr-2"/>
                {isEditMode ? 'Back to Drone Details' : 'Back to Builds'}
            </Link>

            {/* Drone header */}
            <div className="drone-header flex justify-between items-center mb-6">
                <div className="drone-title">
                    <input
                        type="text"
                        placeholder="Enter Drone Name"
                        value={droneData.model}
                        onChange={(e) => setDroneData({...droneData, model: e.target.value})}
                        className="text-2xl font-semibold py-2 px-3 border border-gray-300 rounded-lg w-80 focus:outline-none focus:ring-1 focus:ring-primary focus:border-primary"
                    />
                </div>

                <div className="flex items-center gap-3">
                    {/* Save error message */}
                    {saveError && (
                        <div className="text-red-600 bg-red-50 py-2 px-4 rounded-lg flex items-center">
                            <FontAwesomeIcon icon={faExclamationTriangle} className="mr-2"/>
                            {saveError}
                        </div>
                    )}

                    {/* Delete button - only in edit mode */}
                    {isEditMode && initialDrone && (
                        <button
                            className="bg-red-600 text-white px-5 py-3 rounded-lg font-semibold flex items-center gap-2 hover:bg-red-700 transition-opacity"
                            onClick={() => setShowDeleteConfirmation(true)}
                            disabled={isDeleting || isSaving}
                        >
                            {isDeleting ? (
                                <FontAwesomeIcon icon={faSpinner} className="animate-spin"/>
                            ) : (
                                <FontAwesomeIcon icon={faTrash}/>
                            )}
                            {isDeleting ? 'Deleting...' : 'Delete'}
                        </button>
                    )}

                    {/* Save button */}
                    <button
                        className={`save-button ${themeClass.bg} text-white px-5 py-3 rounded-lg font-semibold flex items-center gap-2 hover:opacity-90 transition-opacity ${isSaving ? 'opacity-70 cursor-not-allowed' : ''}`}
                        onClick={handleSaveDrone}
                        disabled={isSaving || isDeleting}
                    >
                        {isSaving ? (
                            <FontAwesomeIcon icon={faSpinner} className="animate-spin"/>
                        ) : (
                            <FontAwesomeIcon icon={faSave}/>
                        )}
                        {isSaving ? 'Saving...' : isEditMode ? 'Update Drone' : 'Save Drone'}
                    </button>
                </div>
            </div>

            {/* Main layout with three panels */}
            <div className="main-layout flex flex-col lg:flex-row gap-6">
                {/* Left panel - Component Categories */}
                <div className="w-full lg:w-1/5">
                    <ComponentCategoryPanel
                        selectedCategory={selectedCategory}
                        onSelectCategory={handleSelectCategory}
                        droneComponents={droneData}
                        completionPercentage={completionPercentage}
                    />
                </div>

                {/* Middle panel - Component Selection or Build Overview */}
                <div className="flex-1">
                    <ComponentSelectionPanel
                        selectedCategory={selectedCategory}
                        onSelectComponent={handleSelectComponent}
                        showBuildOverview={showBuildOverview}
                        droneComponents={droneData}
                        onBuildOverviewToggle={handleBuildOverviewToggle}
                        compatibilityIssues={compatibilityIssues}
                        persistentCompatibilityIssues={persistentCompatibilityIssues}
                        dismissedIssues={dismissedIssues}
                        onDismissIssue={handleDismissIssue}
                        onRestoreIssue={handleRestoreIssue}
                        missingComponents={missingComponents}
                        completionPercentage={completionPercentage}
                        componentCompatibility={componentCompatibility}
                    />
                </div>

                {/* Right panel - Drone Properties */}
                <div className="w-full lg:w-1/4">
                    {/* Build Completion Meter */}
                    <BuildCompletionMeter
                        percentage={completionPercentage}
                        missingComponents={missingComponents}
                        themeClass={themeClass}
                    />

                    <DronePropertiesPanel
                        droneData={droneData}
                        onChange={handleDroneDataChange}
                        onImageAdd={handleImageAdd}
                        onImageRemove={handleImageRemove}
                        selectedComponent={selectedComponent}
                        componentType={selectedComponentType}
                    />
                </div>
            </div>

            {/* Battery Configuration Modal */}
            <BatteryConfigModal
                isOpen={batteryModalOpen}
                onClose={() => setBatteryModalOpen(false)}
                onSave={handleSaveBattery}
                initialData={droneData.battery || {}}
                isSaving={isSavingBattery}
                saveError={batterySaveError}
            />

            {/* Delete Confirmation Modal */}
            <ConfirmationModal
                isOpen={showDeleteConfirmation}
                onClose={() => setShowDeleteConfirmation(false)}
                onConfirm={handleDeleteDrone}
                title="Delete Drone"
                message="Are you sure you want to delete this drone? This action cannot be undone."
                confirmText="Delete"
                cancelText="Cancel"
                type="danger"
            />
        </div>
    );
};

export default DroneCreateTemplate;