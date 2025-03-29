import React from 'react';
import {createComponentPages} from "../../../utils/componentFactory";
import {getComponentById, getComponentList} from "../../../services/api/components";
import {FilterSidebar} from "../../../components/filters";


const {ListPage, DetailPage} = createComponentPages({
    type: 'propellers',
    title: 'Propellers',
    fetchList: getComponentList,
    fetchDetail: getComponentById,
    filterSidebar: <FilterSidebar componentType="propellers"/>
});

export const PropellerListPage = ListPage;
export const PropellerDetailPage = DetailPage;