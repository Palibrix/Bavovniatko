import React from 'react';
import ComponentListTemplate from '../components/templates/ComponentListTemplate';
import ComponentDetailTemplate from '../components/templates/ComponentDetailTemplate';

/**
 * Creates a component list page for a specific component type
 * 
 * @param {string} componentType - The type of component (antennas, cameras, etc.)
 * @param {string} title - The title for the page
 * @param {Function} fetchDataFn - The API function to fetch the list data
 * @param {Function} renderItemFn - Optional custom render function for list items
 * @returns {Function} - The component list page component
 */
export function createComponentListPage(componentType, title, fetchDataFn, renderItemFn) {
  return function ComponentListPage() {
    return (
      <ComponentListTemplate
        title={title}
        componentType={componentType}
        fetchData={fetchDataFn}
        renderItem={renderItemFn}
      />
    );
  };
}

/**
 * Creates a component detail page for a specific component type
 * 
 * @param {string} componentType - The type of component (antennas, cameras, etc.)
 * @param {Function} fetchDataFn - The API function to fetch the component details
 * @param {Function} renderDetailsFn - Function to render component-specific details
 * @returns {Function} - The component detail page component
 */
export function createComponentDetailPage(componentType, fetchDataFn, renderDetailsFn) {
  return function ComponentDetailPage() {
    return (
      <ComponentDetailTemplate
        componentType={componentType}
        fetchData={fetchDataFn}
        renderDetails={renderDetailsFn}
      />
    );
  };
}
