import React from 'react';
import PropTypes from 'prop-types';
import TabSection from '../TabSection';

/**
 * Description tab content for component detail page
 */
const DescriptionTab = ({ item, componentType }) => {
  return (
    <TabSection title="Description" componentType={componentType}>
      {item.description ? (
        <div
          className="prose prose-lg max-w-none"
          dangerouslySetInnerHTML={{ __html: item.description }}
        />
      ) : (
        <p className="text-gray-500 italic">No description available for this component.</p>
      )}
    </TabSection>
  );
};

DescriptionTab.propTypes = {
  item: PropTypes.object.isRequired,
  componentType: PropTypes.string.isRequired
};

export default DescriptionTab;