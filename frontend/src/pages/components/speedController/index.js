import React from 'react';
import {createComponentPages} from "../../../utils/componentFactory";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {FilterSidebar} from "../../../components/filters";

const {ListPage, DetailPage} = createComponentPages({
    type: 'speed_controllers',
    title: 'Speed Controllers',
    fetchList: getComponentList,
    fetchDetail: getComponentById,
    filterSidebar: <FilterSidebar componentType="speed_controllers"/>
});

export const SpeedControllerListPage = ListPage;
export const SpeedControllerDetailPage = DetailPage;