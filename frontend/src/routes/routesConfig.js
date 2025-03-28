import HomePage from '../pages/HomePage';
import {AntennaListPage, AntennaDetailPage} from '../pages/antenna';
import {CameraListPage, CameraDetailPage} from '../pages/camera';
import {DroneDetailPage, DroneListPage} from "../pages/drones";
import AuthPage from "../pages/auth/AuthPage";
import {ProfilePage} from "../pages/profile";
// import { CameraListPage, CameraDetailPage } from '../pages/camera';
// import { MotorListPage, MotorDetailPage } from '../pages/motor';

// Define routes configuration
const routesConfig = {
    // Home route
    home: {
        path: '/',
        element: HomePage,
    },

    auth: {
        login: {
            path: '/auth',
            element: AuthPage
        }
    },

    // User profile routes
    profile: {
        current: {
            path: '/profile',
            element: ProfilePage,
            protected: true,
        },
        detail: {
            path: '/profile/:id',
            element: ProfilePage,
        },
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
        cameras: {
            list: {
                path: '/components/cameras',
                element: CameraListPage,
            },
            detail: {
                path: '/components/cameras/:id',
                element: CameraDetailPage,
            }

        },

        // Add more component types here as needed
    },

    // Drone routes
    builds: {
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
    }

};

export default routesConfig;