import React from 'react';
import { componentsApi } from '../../services/api';
import { createComponentPages } from '../../utils/componentFactory';
import FilterSidebar from '../../components/filters/FilterSidebar';
import {getComponentById, getComponentList} from "../../services/api/components";

/**
 * Create Camera list and detail pages using the component factory
 */
const { ListPage, DetailPage } = createComponentPages({
  type: 'cameras',
  title: 'Cameras',
  fetchList: getComponentList,
  fetchDetail: getComponentById,
  // Using the filter sidebar component
  filterSidebar: <FilterSidebar componentType="cameras" />
});

export const CameraListPage = ListPage;
export const CameraDetailPage = DetailPage;

/**
 * Additional component-specific functions could be added here
 * For example, specialized add-to-list functions or other utility functions
 */