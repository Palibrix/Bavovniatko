import routesConfig from './routesConfig';
import { generateRoutesFromConfig } from './routeUtils';

// Export the routes configuration
export { routesConfig };

// Export a function to generate routes from the configuration
export const getRoutes = () => generateRoutesFromConfig(routesConfig);

// Export route paths as constants for easy reference throughout the app
export const ROUTES = {
  HOME: routesConfig.home.path,
  COMPONENTS: {
    ANTENNAS: {
      LIST: routesConfig.components.antennas.list.path,
      DETAIL: routesConfig.components.antennas.detail.path,
    },
    // CAMERAS: {
    //   LIST: routesConfig.components.cameras.list.path,
    //   DETAIL: routesConfig.components.cameras.detail.path,
    // },
    // MOTORS: {
    //   LIST: routesConfig.components.motors.list.path,
    //   DETAIL: routesConfig.components.motors.detail.path,
    // },
    // Add more component types here as needed
  }
};

// Helper function to get a detail route for a specific item
export const getDetailRoute = (type, id) => {
  // Normalize type to match our route structure
  const normalizedType = type.toLowerCase();
  
  // Get the appropriate detail route pattern
  const routePattern = ROUTES.COMPONENTS[normalizedType.toUpperCase()]?.DETAIL;
  
  if (!routePattern) {
    console.error(`No detail route found for component type: ${type}`);
    return '/';
  }
  
  // Replace :id with the actual ID
  return routePattern.replace(':id', id);
};
