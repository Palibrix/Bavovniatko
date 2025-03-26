import routesConfig from './routesConfig';
import { generateRoutesFromConfig } from './routeUtils';


// Export a function to generate routes from the configuration
export const getRoutes = () => generateRoutesFromConfig(routesConfig);

export { routesConfig };

// Export route paths as constants for easy reference throughout the app
export const ROUTES = {
  HOME: routesConfig.home.path,
  AUTH: routesConfig.auth.login.path,
  PROFILE: {
    CURRENT: routesConfig.profile.current.path,
    DETAIL: routesConfig.profile.detail.path,
  },
  COMPONENTS: {
    ANTENNAS: {
      LIST: routesConfig.components.antennas.list.path,
      DETAIL: routesConfig.components.antennas.detail.path,
    },
    // Add more component types here as needed
  },
  BUILDS: {
    DRONES: {
      LIST: routesConfig.builds.drones.list.path,
      DETAIL: routesConfig.builds.drones.detail.path,
    }
  }
};