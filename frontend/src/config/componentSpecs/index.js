import {antennaSpecs, antennaKeySpecs} from "./antennaSpecs";
import {cameraKeySpecs, cameraSpecs} from "./cameraSpecs";
import {frameKeySpecs, frameSpecs} from "./frameSpecs";
import {motorKeySpecs, motorSpecs} from "./motorSpecs";
import {propellerKeySpecs, propellerSpecs} from "./propellerSpecs";
import {receiverKeySpecs, receiverSpecs} from "./receiverSpecs";
import {flightControllerKeySpecs, flightControllerSpecs} from "./flightControllerSpecs";
import {speedControllerKeySpecs, speedControllerSpecs} from "./speedControllerSpecs";
import {transmitterKeySpecs, transmitterSpecs} from "./transmitterSpecs";

import {batterySpecs, batteryKeySpecs} from "./batterySpecs";

import generateComponentTags from "./tagGenerator";
export {generateComponentTags}

export const getKeySpecsForComponentType = (type) => {
    const specsMap = {
        antennas: antennaKeySpecs,
        cameras: cameraKeySpecs,
        frames: frameKeySpecs,
        motors: motorKeySpecs,
        propellers: propellerKeySpecs,
        receivers: receiverKeySpecs,
        flight_controllers: flightControllerKeySpecs,
        speed_controllers: speedControllerKeySpecs,
        transmitters: transmitterKeySpecs,

        batteries: batteryKeySpecs,
    };

    return specsMap[type] || [];
};

export const getFullSpecsForComponentType = (type) => {
    const specsMap = {
        antennas: antennaSpecs,
        cameras: cameraSpecs,
        frames: frameSpecs,
        motors: motorSpecs,
        propellers: propellerSpecs,
        receivers: receiverSpecs,
        flight_controllers: flightControllerSpecs,
        speed_controllers: speedControllerSpecs,
        transmitters: transmitterSpecs,

        batteries: batterySpecs,
    };

    return specsMap[type] || [];
};