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
  },
  DRONES: {
    LIST: routesConfig.drones.list.path,
    DETAIL: routesConfig.drones.detail.path,
  }
};
