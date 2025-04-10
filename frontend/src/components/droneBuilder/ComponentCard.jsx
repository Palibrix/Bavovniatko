import React from 'react';
import PropTypes from 'prop-types';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faExclamationTriangle} from '@fortawesome/free-solid-svg-icons';
import Tippy from '@tippyjs/react';

import {getKeySpecsForComponentType} from '../../config/componentSpecs';

/**
 * Grid view card for component selection
 */
const ComponentCard = ({component, categoryType, isCompatible, themeClass, onSelect, compatibilityIssues = []}) => {

    const tooltipContent = (
        <div className="bg-white border border-gray-200 shadow-lg rounded-md p-3 w-64 text-left">
            {compatibilityIssues.length > 0 ? (
                <>
                    <div className="text-red-600 font-medium mb-1">Compatibility Issues:</div>
                    {compatibilityIssues.map((issue, idx) => (
                        <div key={idx} className="text-sm text-gray-700 mb-1">
                            {issue.message}
                        </div>
                    ))}
                </>
            ) : (
                <div className="text-sm text-gray-700">
                    Incompatible with current configuration
                </div>
            )}
        </div>
    );

    return (
        <div
            className={`relative border rounded-xl transition-all hover:-translate-y-1 hover:shadow-md ${
                !isCompatible ? 'opacity-60' : ''
            }`}
        >
            {!isCompatible && (
                <Tippy
                    content={tooltipContent}
                    placement="left-end"
                    interactive={false}
                    allowHTML={true}
                    offset={[0, 8]}
                >
                    <div
                        className="absolute top-2 right-2 w-7 h-7 bg-red-500 rounded-full flex items-center justify-center text-white text-xs cursor-help"
                    >
                        <FontAwesomeIcon icon={faExclamationTriangle}/>
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
    compatibilityIssues: PropTypes.array
};

export default ComponentCard;