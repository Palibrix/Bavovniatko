import React from 'react';
import { componentsApi } from '../../services/api';
import { createComponentPages } from '../../utils/componentFactory';
import FilterSidebarPlaceholder from '../../components/filters/FilterSidebarPlaceholder';
import * as dronesApi from "../../services/api/drones";

/**
 * Create Drone list and detail pages using the component factory
 * Uses placeholder filter sidebar until real implementation
 */
const { ListPage, DetailPage } = createComponentPages({
  type: 'drones',
  title: 'Drones',
  fetchList: dronesApi.getDrones,
  fetchDetail: dronesApi.getDroneById,
  // Using placeholder filter sidebar for now
  filterSidebar: <FilterSidebarPlaceholder componentType="drones" />
});

export const DroneListPage = ListPage;
export const DroneDetailPage = DetailPage;

/**
 * Additional drone-specific functions could be added here
 * For example, specialized add-to-list functions or other utility functions
 */