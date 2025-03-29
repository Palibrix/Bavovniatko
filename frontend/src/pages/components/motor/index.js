import React from 'react';
import {createComponentPages} from "../../../utils/componentFactory";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {FilterSidebar} from "../../../components/filters";

const {ListPage, DetailPage} = createComponentPages({
    type: 'motors',
    title: 'Motors',
    fetchList: getComponentList,
    fetchDetail: getComponentById,
    filterSidebar: <FilterSidebar componentType="motors"/>
});

export const MotorListPage = ListPage;
export const MotorDetailPage = DetailPage;