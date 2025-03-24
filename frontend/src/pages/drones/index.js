import React from 'react';
import { dronesApi } from '../../services/api';
import { createComponentPages } from '../../utils/componentFactory';
import FilterSidebarPlaceholder from '../../components/filters/FilterSidebarPlaceholder';
import DroneDetailTemplate from '../../components/templates/DroneDetailTemplate';

/**
 * Create Drone list and detail pages
 */
const { ListPage, DetailPage } = createComponentPages({
  type: 'drones',
  title: 'Drones',
  fetchList: dronesApi.getDrones,
  fetchDetail: dronesApi.getDroneById,
  DetailTemplate: DroneDetailTemplate, // Use custom template
  filterSidebar: <FilterSidebarPlaceholder componentType="drones" />
});

export const DroneListPage = ListPage;
export const DroneDetailPage = DetailPage;