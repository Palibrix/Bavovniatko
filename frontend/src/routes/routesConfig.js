import HomePage from '../pages/HomePage';
import { AntennaListPage, AntennaDetailPage } from '../pages/antenna';
import {DroneDetailPage, DroneListPage} from "../pages/drones";
// import { CameraListPage, CameraDetailPage } from '../pages/camera';
// import { MotorListPage, MotorDetailPage } from '../pages/motor';

// Define routes configuration
const routesConfig = {
  // Home route
  home: {
    path: '/',
    element: HomePage,
  },
  
  // Component routes grouped by component type
  components: {
    // Antenna routes
    antennas: {
      list: {
        path: '/components/antennas',
        element: AntennaListPage,
      },
      detail: {
        path: '/components/antennas/:id',
        element: AntennaDetailPage,
      }
    },
    
    // Camera routes
    // cameras: {
    //   list: {
    //     path: '/components/cameras',
    //     element: CameraListPage,
    //   },
    //   detail: {
    //     path: '/components/cameras/:id',
    //     element: CameraDetailPage,
    //   }
    // },
    //
    // // Motor routes
    // motors: {
    //   list: {
    //     path: '/components/motors',
    //     element: MotorListPage,
    //   },
    //   detail: {
    //     path: '/components/motors/:id',
    //     element: MotorDetailPage,
    //   }
    // },
    
    // Add more component types here as needed
  },

    // Drone routes
  drones: {
    list: {
      path: '/drones',
      element: DroneListPage,
    },
    detail: {
      path: '/drones/:id',
      element: DroneDetailPage,
    }
  }
};

export default routesConfig;
