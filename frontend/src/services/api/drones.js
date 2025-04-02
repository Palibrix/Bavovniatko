import {del, get, patch, post, put} from './base';

const ENDPOINTS = {
    drones: '/builds/drones/',
};


export function getDrones(params = {}) {
    return get(ENDPOINTS.drones, params);
}


export function getDroneById(id) {
    return get(`${ENDPOINTS.drones}${id}/`);
}

export function createDrone(droneData) {
    return post(ENDPOINTS.drones, droneData);
}


export function updateDrone(id, droneData) {
    return put(`${ENDPOINTS.drones}${id}/`, droneData);
}


export function patchDrone(id, droneData) {
    return patch(`${ENDPOINTS.drones}${id}/`, droneData);
}

export function deleteDrone(id, droneData) {
    return del(`${ENDPOINTS.drones}${id}/`, droneData);
}