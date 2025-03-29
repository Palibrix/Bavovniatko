import React from 'react';
import {createComponentPages} from "../../../utils/componentFactory";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {FilterSidebar} from "../../../components/filters";

const { ListPage, DetailPage } = createComponentPages({
  type: 'cameras',
  title: 'Cameras',
  fetchList: getComponentList,
  fetchDetail: getComponentById,
  filterSidebar: <FilterSidebar componentType="cameras" />
});

export const CameraListPage = ListPage;
export const CameraDetailPage = DetailPage;