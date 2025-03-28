import React from 'react';
import { createComponentPages } from '../../utils/componentFactory';
import FilterSidebar from '../../components/filters/FilterSidebar';
import {getComponentById, getComponentList} from "../../services/api/components";

/**
 * Create Antenna list and detail pages using the component factory
 * This now uses the real FilterSidebar component instead of the placeholder
 */
const { ListPage, DetailPage } = createComponentPages({
  type: 'antennas',
  title: 'Antennas',
  fetchList: getComponentList,
  fetchDetail: getComponentById,
  // Using our real filter sidebar component
  filterSidebar: <FilterSidebar componentType="antennas" />
});

export const AntennaListPage = ListPage;
export const AntennaDetailPage = DetailPage;

/**
 * Additional component-specific functions could be added here
 * For example, specialized add-to-list functions or other utility functions
 */