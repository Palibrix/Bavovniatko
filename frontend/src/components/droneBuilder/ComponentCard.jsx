import React from 'react';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle, faInfoCircle} from '@fortawesome/free-solid-svg-icons';
import Tippy from '@tippyjs/react';

import {getKeySpecsForComponentType} from '../../config/componentSpecs';

/**
 * Grid view card for component selection
 */
const ComponentCard = ({
    component,
    categoryType,
    isCompatible,
    themeClass,
    onSelect,
    compatibilityIssues = [],
    isDismissed = false,
    hasRecommendations = false  // New prop
}) => {

    const criticalIssues = compatibilityIssues.filter(issue =>
      issue.severity !== 'recommendation' && issue.severity !== undefined);
    const recommendations = compatibilityIssues.filter(issue =>
      issue.severity === 'recommendation');

    const tooltipContent = (
        <div className="bg-white border border-gray-200 shadow-lg rounded-md p-3 w-64 text-left">
            {criticalIssues.length > 0 && (
                <>
                    <div className="text-red-600 font-medium mb-1">
                        Compatibility Issues:
                        {isDismissed && (
                            <span className="text-gray-500 text-xs ml-2">(dismissed)</span>
                        )}
                    </div>
                    {criticalIssues.map((issue, idx) => (
                        <div key={idx} className="text-sm text-gray-700 mb-1">
                            {issue.message}
                        </div>
                    ))}
                </>
            )}

            {recommendations.length > 0 && (
                <>
                    <div className="text-blue-600 font-medium mb-1 mt-2">
                        Recommendations:
                    </div>
                    {recommendations.map((rec, idx) => (
                        <div key={idx} className="text-sm text-gray-700 mb-1">
                            {rec.message}
                        </div>
                    ))}
                </>
            )}

            {criticalIssues.length === 0 && recommendations.length === 0 && (
                <div className="text-sm text-gray-700">
                    Incompatible with current configuration
                    {isDismissed && (
                        <div className="text-gray-500 text-xs mt-1">(issue dismissed)</div>
                    )}
                </div>
            )}
        </div>
    );

    // Determine which icon to show based on issue type
    let issueIcon = faExclamationTriangle;
    let issueIconClass = "absolute top-2 right-2 w-7 h-7 bg-red-500 rounded-full flex items-center justify-center text-white text-xs cursor-help";

    if (criticalIssues.length === 0 && recommendations.length > 0) {
        // Only recommendations
        issueIcon = faInfoCircle;
        issueIconClass = "absolute top-2 right-2 w-7 h-7 bg-blue-500 rounded-full flex items-center justify-center text-white text-xs cursor-help";
    }

    if (isDismissed) {
        // Gray for dismissed issues
        issueIconClass = "absolute top-2 right-2 w-7 h-7 bg-gray-500 rounded-full flex items-center justify-center text-white text-xs cursor-help";
    }

    return (
        <div
            className={`relative border rounded-xl transition-all hover:-translate-y-1 hover:shadow-md ${
                !isCompatible ? 'opacity-60' : ''
            }`}
        >
            {/* Show critical issues icon */}
            {(!isCompatible || recommendations.length > 0) && (
                <Tippy
                    content={tooltipContent}
                    placement="left-end"
                    interactive={false}
                    allowHTML={true}
                    offset={[0, 8]}
                >
                    <div className={issueIconClass}>
                        <FontAwesomeIcon icon={issueIcon}/>
                    </div>
                </Tippy>
            )}

            <div className="p-3 bg-gray-50 border-b">
                <h3 className="font-medium mb-1">{component.model}</h3>
                <div className="text-sm text-gray-500">{component.manufacturer}</div>
            </div>

            <div className="p-3">
                {renderComponentSpecs(component, categoryType)}
            </div>

            <div className="p-3 bg-gray-50 border-t flex justify-between items-center">
                <button className="text-sm text-gray-500 hover:text-primary">Details</button>
                <button
                    className={`${themeClass.text} font-medium text-sm hover:underline`}
                    onClick={onSelect}
                >
                    Add
                </button>
            </div>
        </div>
    );
};

function renderComponentSpecs(component, categoryType) {
    const specs = getKeySpecsForComponentType(categoryType === 'antennas_receiver' ||
    categoryType === 'antennas_transmitter' ?
        'antennas' : categoryType);
    const displaySpecs = specs.slice(0, 3);
    return displaySpecs.map((spec, index) => {
        const value = extractSpecValue(component, spec);
        return (
            <div key={index} className="flex justify-between text-sm mb-1.5">
                <span className="text-gray-500">{spec.label}</span>
                <span className="font-medium">{value}</span>
            </div>
        );
    });
}

function extractSpecValue(component, spec) {
    let value = null;
    try {
        value = spec.path.split('.').reduce((obj, key) =>
            obj && obj[key] !== undefined ? obj[key] : null, component);

        if (spec.formatter) {
            return spec.formatter(value, component);
        } else if (spec.unit && value !== null) {
            return `${value} ${spec.unit}`;
        } else if (value !== null) {
            return value.toString();
        }
    } catch (error) {
        console.error(`Error extracting spec value: ${error.message}`);
    }
    return 'N/A';
}


ComponentCard.propTypes = {
    component: PropTypes.object.isRequired,
    categoryType: PropTypes.string.isRequired,
    isCompatible: PropTypes.bool.isRequired,
    themeClass: PropTypes.object.isRequired,
    onSelect: PropTypes.func.isRequired,
    compatibilityIssues: PropTypes.array,
    isDismissed: PropTypes.bool,
    hasRecommendations: PropTypes.bool
};

export default ComponentCard;