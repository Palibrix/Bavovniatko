import React from 'react';
import { componentsApi } from '../../services/api';
import { createComponentPages } from '../../utils/componentFactory';
import { antennaSpecs } from '../../config/componentSpecs';
import FilterSidebarPlaceholder from '../../components/filters/FilterSidebarPlaceholder';

/**
 * Create Antenna list and detail pages using the component factory
 */
const { ListPage, DetailPage } = createComponentPages({
  type: 'antennas',
  title: 'Antennas',
  fetchList: componentsApi.getAntennas,
  fetchDetail: componentsApi.getAntennaById,
  // Using placeholder filter sidebar for now
  filterSidebar: <FilterSidebarPlaceholder componentType="antennas" />
});

export const AntennaListPage = ListPage;
export const AntennaDetailPage = DetailPage;

/**
 * Additional component-specific functions could be added here
 * For example, specialized add-to-list functions or other utility functions
 */