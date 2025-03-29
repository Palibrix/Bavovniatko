import React from 'react';
import {createComponentPages} from "../../../utils/componentFactory";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {FilterSidebar} from "../../../components/filters";

const { ListPage, DetailPage } = createComponentPages({
  type: 'frames',
  title: 'Frames',
  fetchList: getComponentList,
  fetchDetail: getComponentById,
  filterSidebar: <FilterSidebar componentType="frames" />
});

export const FrameListPage = ListPage;
export const FrameDetailPage = DetailPage;