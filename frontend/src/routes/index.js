import routesConfig from './routesConfig';
import {generateRoutesFromConfig} from './routeUtils';

export const getRoutes = () => generateRoutesFromConfig(routesConfig);

export {routesConfig};


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
        CAMERAS: {
            LIST: routesConfig.components.cameras.list.path,
            DETAIL: routesConfig.components.cameras.detail.path,
        },
        FRAMES: {
            LIST: routesConfig.components.frames.list.path,
            DETAIL: routesConfig.components.frames.detail.path,
        },
        MOTORS: {
            LIST: routesConfig.components.motors.list.path,
            DETAIL: routesConfig.components.motors.detail.path,
        },
        PROPELLERS: {
            LIST: routesConfig.components.propellers.list.path,
            DETAIL: routesConfig.components.propellers.detail.path,
        },
        RECEIVERS: {
            LIST: routesConfig.components.receivers.list.path,
            DETAIL: routesConfig.components.receivers.detail.path,
        },
        FLIGHT_CONTROLLERS: {
            LIST: routesConfig.components.flight_controllers.list.path,
            DETAIL: routesConfig.components.flight_controllers.detail.path,
        },
        SPEED_CONTROLLERS: {
            LIST: routesConfig.components.speed_controllers.list.path,
            DETAIL: routesConfig.components.speed_controllers.detail.path,
        },
        TRANSMITTERS: {
            LIST: routesConfig.components.transmitters.list.path,
            DETAIL: routesConfig.components.transmitters.detail.path,
        }
    },
    BUILDS: {
        DRONES: {
            LIST: routesConfig.builds.drones.list.path,
            DETAIL: routesConfig.builds.drones.detail.path,
            CREATE: routesConfig.builds.drones.create.path,
            EDIT: routesConfig.builds.drones.edit.path,
        }
    }
};