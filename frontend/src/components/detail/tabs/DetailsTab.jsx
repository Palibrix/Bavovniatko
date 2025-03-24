import React, { useState } from 'react';
import PropTypes from 'prop-types';
import TabSection from '../TabSection';
import { getEntityThemeClass } from '../../../utils/themeUtils';

/**
 * Details tab content for component detail page
 * Supports multiple detail blocks for components like frames
 */
const DetailsTab = ({ item, componentType, inPanel = false }) => {
  // Setup state for selected variants (used for components with multiple connectors, etc.)
  const [selectedVariantIndex, setSelectedVariantIndex] = useState(0);
  const themeClass = getEntityThemeClass(componentType);

  // Get the appropriate details based on component type
  const getDetails = () => {
    switch (componentType) {
      case 'antennas':
        return item.details || [];
      case 'cameras':
        return item.details || [];
      case 'motors':
        return item.details || [];
      case 'receivers':
        return item.details || [];
      case 'frames':
        // For frames, we have 3 types of details
        const details = [];
        if (item.camera_details?.length) {
          details.push({
            type: 'camera',
            label: 'Camera Mount',
            items: item.camera_details
          });
        }
        if (item.motor_details?.length) {
          details.push({
            type: 'motor',
            label: 'Motor Mount',
            items: item.motor_details
          });
        }
        if (item.vtx_details?.length) {
          details.push({
            type: 'vtx',
            label: 'VTX Mount',
            items: item.vtx_details
          });
        }
        return details;
      default:
        return [];
    }
  };

  const details = getDetails();

  // If no details available, show a message
  if (!details.length) {
    const message = (
      <p className="text-gray-500 italic">No additional details available for this component.</p>
    );

    return inPanel ? message : (
      <TabSection title="Details" componentType={componentType}>
        {message}
      </TabSection>
    );
  }

  // For frames, show multiple detail blocks
  if (componentType === 'frames') {
    const frameContent = (
      <>
        {details.map((detailGroup, groupIndex) => (
          <div key={groupIndex} className="mb-8 last:mb-0">
            <h3 className={`text-lg font-semibold ${themeClass.text} mb-4`}>
              {detailGroup.label}
            </h3>
            <div className="bg-gray-50 rounded-xl p-6">
              <table className="w-full">
                <tbody>
                  {detailGroup.type === 'camera' && detailGroup.items.map((detail, idx) => (
                    <React.Fragment key={idx}>
                      <tr>
                        <th className="text-left py-3 text-gray-500 w-1/3">Height</th>
                        <td className="py-3 font-medium">{detail.camera_mount_height} mm</td>
                      </tr>
                      <tr>
                        <th className="text-left py-3 text-gray-500 w-1/3">Width</th>
                        <td className="py-3 font-medium">{detail.camera_mount_width} mm</td>
                      </tr>
                    </React.Fragment>
                  ))}

                  {detailGroup.type === 'motor' && detailGroup.items.map((detail, idx) => (
                    <React.Fragment key={idx}>
                      <tr>
                        <th className="text-left py-3 text-gray-500 w-1/3">Height</th>
                        <td className="py-3 font-medium">{detail.motor_mount_height} mm</td>
                      </tr>
                      <tr>
                        <th className="text-left py-3 text-gray-500 w-1/3">Width</th>
                        <td className="py-3 font-medium">{detail.motor_mount_width} mm</td>
                      </tr>
                    </React.Fragment>
                  ))}

                  {detailGroup.type === 'vtx' && detailGroup.items.map((detail, idx) => (
                    <React.Fragment key={idx}>
                      <tr>
                        <th className="text-left py-3 text-gray-500 w-1/3">Height</th>
                        <td className="py-3 font-medium">{detail.vtx_mount_height} mm</td>
                      </tr>
                      <tr>
                        <th className="text-left py-3 text-gray-500 w-1/3">Width</th>
                        <td className="py-3 font-medium">{detail.vtx_mount_width} mm</td>
                      </tr>
                    </React.Fragment>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        ))}
      </>
    );

    return inPanel ? frameContent : (
      <TabSection title="Details" componentType={componentType}>
        {frameContent}
      </TabSection>
    );
  }

  // For other components with variants (like antennas)
  const variantContent = (
    <>
      {details.length > 1 ? (
        <div className="mb-6 bg-gray-50 rounded-lg flex overflow-hidden">
          {details.map((detail, index) => {
            // Create label based on connector type or other distinguishing feature
            let variantLabel = '';

            if (componentType === 'antennas' && detail.connector_type) {
              variantLabel = `${detail.connector_type.type} ${detail.angle_type || ''}`;
            } else {
              variantLabel = `Variant ${index + 1}`;
            }

            return (
              <button
                key={index}
                className={`py-3 px-4 font-medium transition-colors flex-1 ${
                  selectedVariantIndex === index
                    ? `${themeClass.bgOpacity[10]} ${themeClass.text} border-b-2 ${themeClass.border}`
                    : 'text-gray-600 hover:bg-gray-100'
                }`}
                onClick={() => setSelectedVariantIndex(index)}
              >
                {variantLabel}
              </button>
            );
          })}
        </div>
      ) : null}

      {details.length > 0 && (
        <div className="bg-gray-50 rounded-xl p-6">
          <table className="w-full">
            <tbody>
              {componentType === 'antennas' && (
                <>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">Connector Type</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.connector_type?.type || 'N/A'}
                    </td>
                  </tr>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">Angle Type</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.angle_type || 'N/A'}
                    </td>
                  </tr>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">Weight</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.weight ? `${details[selectedVariantIndex].weight}g` : 'N/A'}
                    </td>
                  </tr>
                </>
              )}

              {componentType === 'motors' && (
                <>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">Weight</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.weight ? `${details[selectedVariantIndex].weight}g` : 'N/A'}
                    </td>
                  </tr>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">Max Power</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.max_power ? `${details[selectedVariantIndex].max_power}W` : 'N/A'}
                    </td>
                  </tr>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">KV per Volt</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.kv_per_volt || 'N/A'}
                    </td>
                  </tr>
                  <tr>
                    <th className="text-left py-3 text-gray-500 w-1/3">Voltage</th>
                    <td className="py-3 font-medium">
                      {details[selectedVariantIndex]?.voltage ?
                        `${details[selectedVariantIndex].voltage.min_cells}-${details[selectedVariantIndex].voltage.max_cells}S ${details[selectedVariantIndex].voltage.type}` :
                        'N/A'
                      }
                    </td>
                  </tr>
                </>
              )}

              {/* Add more component types as needed */}
            </tbody>
          </table>
        </div>
      )}
    </>
  );

  return inPanel ? variantContent : (
    <TabSection title="Details" componentType={componentType}>
      {variantContent}
    </TabSection>
  );
};

DetailsTab.propTypes = {
  item: PropTypes.object.isRequired,
  componentType: PropTypes.string.isRequired,
  inPanel: PropTypes.bool
};

export default DetailsTab;