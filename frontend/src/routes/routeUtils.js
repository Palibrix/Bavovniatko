import React from 'react';
import { Route } from 'react-router-dom';

/**
 * Recursively flatten nested route configuration into an array of route objects
 * 
 * @param {Object} routesConfig - The nested routes configuration object
 * @returns {Array} - Flattened array of route objects with path and element
 */
export function flattenRoutes(routesConfig) {
  const routes = [];
  
  /**
   * Recursive function to process nested route objects
   * 
   * @param {Object} config - Current route config object
   */
  function processRoutes(config) {
    // Process each key in the config object
    Object.keys(config).forEach(key => {
      const route = config[key];
      
      // If this has path and element properties, it's a route definition
      if (route.path && route.element) {
        routes.push({
          path: route.path,
          element: route.element
        });
      }
      
      // If it's an object without path/element, it's a group - recurse into it
      if (typeof route === 'object' && !route.path) {
        processRoutes(route);
      }
    });
  }
  
  processRoutes(routesConfig);
  return routes;
}

/**
 * Generate Route components from flattened routes array
 * 
 * @param {Array} routes - Flattened routes array with path and element properties
 * @returns {Array} - Array of Route components
 */
export function generateRouteComponents(routes) {
  return routes.map((route, index) => {
    const RouteComponent = route.element;
    return <Route key={index} path={route.path} element={<RouteComponent />} />;
  });
}

/**
 * Generate Route components directly from a nested routes configuration
 * 
 * @param {Object} routesConfig - The nested routes configuration object
 * @returns {Array} - Array of Route components
 */
export function generateRoutesFromConfig(routesConfig) {
  const flattenedRoutes = flattenRoutes(routesConfig);
  return generateRouteComponents(flattenedRoutes);
}
