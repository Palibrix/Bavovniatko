import React from 'react';
import PropTypes from 'prop-types';

/**
 * Reusable container for tab content with consistent styling
 *
 * @param {Object} props Component properties
 * @param {string} props.title Section title
 * @param {React.ReactNode} props.children Content to display
 * @param {string} props.themeColor Theme color for styling
 * @param {React.ReactNode} props.headerActions Optional actions to display in the header
 */
const TabSection = ({ title, children, themeColor, headerActions }) => {
  return (
    <div className="bg-white rounded-3xl shadow-sm overflow-hidden mb-6">
      <div className="px-6 py-4 border-b border-gray-100 font-semibold text-primary relative flex justify-between items-center">
        <div className={`absolute top-0 left-0 bottom-0 w-1 bg-${themeColor}`}></div>
        <h2 className="text-xl">{title}</h2>
        {headerActions && (
          <div className="header-actions">
            {headerActions}
          </div>
        )}
      </div>
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};

TabSection.propTypes = {
  title: PropTypes.string.isRequired,
  children: PropTypes.node.isRequired,
  themeColor: PropTypes.string.isRequired,
  headerActions: PropTypes.node,
};

export default TabSection;