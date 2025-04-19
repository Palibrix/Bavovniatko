import HomePage from '../pages/HomePage';
import {AntennaDetailPage, AntennaListPage} from '../pages/components/antenna';
import {CameraDetailPage, CameraListPage} from '../pages/components/camera';
import {FrameDetailPage, FrameListPage} from '../pages/components/frame';
import {MotorDetailPage, MotorListPage} from '../pages/components/motor';
import {PropellerDetailPage, PropellerListPage} from '../pages/components/propeller';
import {ReceiverDetailPage, ReceiverListPage} from '../pages/components/receiver';
import {FlightControllerDetailPage, FlightControllerListPage} from '../pages/components/flightController';
import {SpeedControllerDetailPage, SpeedControllerListPage} from '../pages/components/speedController';
import {TransmitterDetailPage, TransmitterListPage} from '../pages/components/transmitter';
import {DroneDetailPage, DroneListPage} from "../pages/drones";
import DroneCreatePage from "../pages/drones/DroneCreatePage";
import AuthPage from "../pages/auth/AuthPage";
import {ProfilePage} from "../pages/profile";
import DroneEditPage from "../pages/drones/DroneEditPage";
import ListDetailPage from "../pages/lists/ListDetailPage";

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

    // List routes
    lists: {
        detail: {
            path: '/lists/:id',
            element: ListDetailPage,
            protected: true,
        }
    },

    // Component routes grouped by component type
    components: {
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
        frames: {
            list: {
                path: '/components/frames',
                element: FrameListPage,
            },
            detail: {
                path: '/components/frames/:id',
                element: FrameDetailPage,
            }
        },
        motors: {
            list: {
                path: '/components/motors',
                element: MotorListPage,
            },
            detail: {
                path: '/components/motors/:id',
                element: MotorDetailPage,
            }
        },
        propellers: {
            list: {
                path: '/components/propellers',
                element: PropellerListPage,
            },
            detail: {
                path: '/components/propellers/:id',
                element: PropellerDetailPage,
            }
        },
        receivers: {
            list: {
                path: '/components/receivers',
                element: ReceiverListPage,
            },
            detail: {
                path: '/components/receivers/:id',
                element: ReceiverDetailPage,
            }
        },
        flight_controllers: {
            list: {
                path: '/components/flight_controllers',
                element: FlightControllerListPage,
            },
            detail: {
                path: '/components/flight_controllers/:id',
                element: FlightControllerDetailPage,
            }
        },
        speed_controllers: {
            list: {
                path: '/components/speed_controllers',
                element: SpeedControllerListPage,
            },
            detail: {
                path: '/components/speed_controllers/:id',
                element: SpeedControllerDetailPage,
            }
        },
        transmitters: {
            list: {
                path: '/components/transmitters',
                element: TransmitterListPage,
            },
            detail: {
                path: '/components/transmitters/:id',
                element: TransmitterDetailPage,
            }
        }
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
            },
            create: {
                path: '/drones/create',
                element: DroneCreatePage,
                protected: true,
            },
            edit: {
                path: '/drones/edit/:id',
                element: DroneEditPage,
                protected: true,
            }
        }
    }
};

export default routesConfig;