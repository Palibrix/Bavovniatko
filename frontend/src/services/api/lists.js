import { get, post, put, del } from './base';

const ENDPOINTS = {
  lists: '/lists/',
  addComponent: (listId) => `/lists/${listId}/add_component/`,
  removeComponents: (listId) => `/lists/${listId}/remove_components/`,
  filterByType: (listId) => `/lists/${listId}/filter_by_type/`
};

/**
 * Get all lists belonging to the current user
 * 
 * @returns {Promise} Promise with lists data
 */
export const getUserLists = async () => {
  return get(ENDPOINTS.lists);
};

/**
 * Get a specific list by ID
 * 
 * @param {string|number} id List ID
 * @returns {Promise} Promise with list data
 */
export const getListById = async (id) => {
  return get(`${ENDPOINTS.lists}${id}/`);
};

/**
 * Create a new list
 * 
 * @param {Object} listData List data (name, description)
 * @returns {Promise} Promise with created list data
 */
export const createList = async (listData) => {
  return post(ENDPOINTS.lists, listData);
};

/**
 * Update an existing list
 * 
 * @param {string|number} id List ID
 * @param {Object} listData Updated list data
 * @returns {Promise} Promise with updated list data
 */
export const updateList = async (id, listData) => {
  return put(`${ENDPOINTS.lists}${id}/`, listData);
};

/**
 * Delete a list
 * 
 * @param {string|number} id List ID 
 * @returns {Promise} Promise with response
 */
export const deleteList = async (id) => {
  return del(`${ENDPOINTS.lists}${id}/`);
};

/**
 * Add a component to a list
 * 
 * @param {string|number} listId List ID
 * @param {string} componentType Component type
 * @param {string|number} componentId Component ID
 * @returns {Promise} Promise with response
 */
export const addComponentToList = async (listId, componentType, componentId) => {
  return post(ENDPOINTS.addComponent(listId), {
    component_type: componentType,
    component_id: componentId
  });
};

/**
 * Remove a component from a list
 * 
 * @param {string|number} listId List ID
 * @param {string} componentType Component type
 * @param {string|number} componentId Component ID
 * @returns {Promise} Promise with response
 */
export const removeComponentFromList = async (listId, componentType, componentId) => {
  return post(ENDPOINTS.removeComponents(listId), {
    component_type: componentType,
    component_id: componentId
  });
};

/**
 * Get list items filtered by component type
 * 
 * @param {string|number} listId List ID
 * @param {string} componentType Component type
 * @returns {Promise} Promise with filtered list items
 */
export const getListItemsByType = async (listId, componentType) => {
  return get(ENDPOINTS.filterByType(listId), { type: componentType });
};